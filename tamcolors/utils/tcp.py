from threading import Thread, Lock
import socket
from tamcolors.utils.encryption import Encryption
from time import sleep
from tamcolors.utils import compress
from tamcolors.utils.object_packer import DEFAULT_OBJECT_PACKER_JSON
from hashlib import sha3_512


class TCPReceiverError(Exception):
    pass


class TCPReceiver:
    _sockets = {}
    _socket_connections = {}
    _lock = Lock()

    @classmethod
    def start(cls, host, port=4444, ipv6=False, listen_count=10, raise_receiver_error=True):
        try:
            cls._lock.acquire()
            if (host, port) in cls._sockets:
                if not raise_receiver_error:
                    return
                raise TCPReceiverError("({}, {}) is all ready running!".format(host, port))

            af_type = socket.AF_INET
            if ipv6:
                af_type = socket.AF_INET6

            this_socket = socket.socket(af_type, socket.SOCK_STREAM)
            this_socket.bind((host, port))
            this_socket.listen(listen_count)

            cls._sockets[(host, port)] = this_socket
            cls._socket_connections[(host, port)] = []

            Thread(target=cls._connection_handler, args=(host, port), daemon=True).start()
        finally:
            cls._lock.release()

    @classmethod
    def stop(cls, host, port, raise_receiver_error=True):
        try:
            cls._lock.acquire()
            if (host, port) in cls._sockets:
                for connections in cls._socket_connections[(host, port)]:
                    connections.close()

                cls._sockets[(host, port)].close()
                del cls._sockets[(host, port)]
                del cls._socket_connections[(host, port)]
            elif raise_receiver_error:
                raise TCPReceiverError("({}, {}) is not running!".format(host, port))
        finally:
            cls._lock.release()

    @classmethod
    def is_running(cls, host, port):
        try:
            cls._lock.acquire()
            return (host, port) in cls._sockets
        finally:
            cls._lock.release()

    @classmethod
    def get_connection(cls, host, port, connection_address=None, wait=False):
        while wait:
            try:
                cls._lock.acquire()
                if connection_address is None and len(cls._socket_connections[(host, port)]):
                    connection, address = cls._socket_connections[(host, port)][0]
                    del cls._socket_connections[(host, port)][0]
                    return connection, address
            finally:
                cls._lock.release()
            sleep(0.0001)

    @classmethod
    def _connection_handler(cls, host, port):
        try:
            this_socket = cls._sockets[(host, port)]
            while True:
                connection, address = this_socket.accept()
                address = address[0]
                try:
                    cls._lock.acquire()
                    cls._socket_connections[(host, port)].append((connection, address))
                finally:
                    cls._lock.release()
        except:
            pass
        finally:
            cls.stop(host, port, raise_receiver_error=False)


class TCPHostError(Exception):
    pass


class TCPHost:
    def __init__(self, connection, address, password="", encryption=None):
        self._lock = Lock()
        self._connection = connection
        self._open = True
        self._address = address
        self._encryption = encryption
        self._password = sha3_512(bytes(password, encoding="utf-8")).hexdigest()
        if self._encryption is None:
            self._encryption = Encryption()
        self._connection_public_key = None
        self._name = None
        self._handshake()

    def __del__(self):
        self.close()

    def close(self):
        if self._open:
            self._open = False
            self._connection.close()

    def get_data(self):
        try:
            self._lock.acquire()
            ret_data = self._get_block()
            if self._encryption:
                ret_data = self._encryption.decrypt(ret_data)
            return compress.decompress(ret_data)
        finally:
            self._lock.release()

    def send_data(self, data):
        try:
            self._lock.acquire()
            data = compress.compress(data)
            if self._encryption:
                data = self._encryption.encrypt_with_public_key(self._connection_public_key, data)
            self._send_block(data)
        finally:
            self._lock.release()

    def _handshake(self):
        if self._encryption:
            self._send_block(self._encryption.get_raw_public_key())
            self._connection_public_key = self._get_block()

        data = DEFAULT_OBJECT_PACKER_JSON.loads(self.get_data())
        self._name = data["name"]
        if self._password != data["password"]:
            raise TCPHostError("Wrong Password!")

    def _send_block(self, data):
        data_size = len(data)
        data_size_in_bytes = data_size.to_bytes(data_size.bit_length() // 8 + min(data_size.bit_length() % 8, 1),
                                                byteorder="big")
        number_size = len(data_size_in_bytes)
        self._connection.send(bytes((number_size,)) + data_size_in_bytes + data)

    def _get_block(self):
        number_size = self._connection.recv(1)[0]
        data_size = int.from_bytes(self._connection.recv(number_size), "big")
        return self._connection.recv(data_size)

    def get_name(self):
        return self._name


class TCPConnectionError(Exception):
    pass


class TCPConnection:
    def __init__(self, host, port, name="", password="", ipv6=False, encryption=None):
        self._lock = Lock()
        self._open = True
        self._host = host
        self._port = port
        self._name = name
        self._password = sha3_512(bytes(password, encoding="utf-8")).hexdigest()

        self._encryption = encryption
        if self._encryption is None:
            self._encryption = Encryption()

        af_mode = socket.AF_INET
        if ipv6:
            af_mode = socket.AF_INET6

        self._host_connection = socket.socket(af_mode, socket.SOCK_STREAM)
        self._host_connection.connect((self._host, self._port))
        self._host_public_key = None
        self._handshake()

    def __del__(self):
        self.close()

    def close(self):
        if self._open:
            self._open = False
            self._host_connection.close()

    def _send_block(self, data):
        data_size = len(data)
        data_size_in_bytes = data_size.to_bytes(data_size.bit_length() // 8 + min(data_size.bit_length() % 8, 1),
                                                byteorder="big")
        number_size = len(data_size_in_bytes)
        self._host_connection.send(bytes((number_size,)) + data_size_in_bytes + data)

    def _get_block(self):
        number_size = self._host_connection.recv(1)[0]
        data_size = int.from_bytes(self._host_connection.recv(number_size), "big")
        return self._host_connection.recv(data_size)

    def _handshake(self):
        if self._encryption:
            self._host_public_key = self._get_block()
            self._send_block(self._encryption.get_raw_public_key())
            self.send_data(DEFAULT_OBJECT_PACKER_JSON.dumps({"name": self._name, "password": self._password}))

    def get_data(self):
        try:
            self._lock.acquire()
            ret_data = self._get_block()
            if self._encryption:
                ret_data = self._encryption.decrypt(ret_data)
            return compress.decompress(ret_data)
        finally:
            self._lock.release()

    def send_data(self, data):
        try:
            self._lock.acquire()
            data = compress.compress(data)
            if self._encryption:
                data = self._encryption.encrypt_with_public_key(self._host_public_key, data)
            self._send_block(data)
        finally:
            self._lock.release()
