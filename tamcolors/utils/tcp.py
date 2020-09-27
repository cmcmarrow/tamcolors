from threading import Thread, Lock
import socket
from tamcolors.utils.encryption import Encryption
from tamcolors.utils import compress
from tamcolors.utils.object_packer import DEFAULT_OBJECT_PACKER_JSON
from hashlib import sha3_512


class TCPError(Exception):
    pass


class TCPReceiver:
    def __init__(self,
                 host="127.0.0.1",
                 port=4444,
                 ipv6=False,
                 listen_count=10,
                 connection_password="",
                 address_white_list=None,
                 address_black_list=None,
                 encryption=None,
                 object_packer=None,
                 our_information=None):
        self._open = True

        af_type = socket.AF_INET
        if ipv6:
            af_type = socket.AF_INET6

        self._socket = socket.socket(af_type, socket.SOCK_STREAM)
        self._socket.bind((host, port))
        self._socket.listen(listen_count)

        self._connection_password = sha3_512(bytes(connection_password, encoding="utf-8")).hexdigest()
        self._address_white_list = address_white_list

        if isinstance(self._address_white_list, (tuple, list)):
            self._address_white_list = set(self._address_white_list)

        self._address_black_list = address_black_list
        if self._address_black_list is None:
            self._address_black_list = set()
        elif isinstance(self._address_black_list, (tuple, list)):
            self._address_black_list = set(self._address_black_list)

        self._encryption = encryption
        self._object_packer = object_packer
        self._our_information = our_information

        self._new_connections = []
        self._lock = Lock()
        Thread(target=self._connection_finder, daemon=True).start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self._open:
            self._open = False
            self._socket.close()

    def get_host_connection(self, wait=False):
        while True:
            try:
                self._lock.acquire()
                if len(self._new_connections):
                    connection = self._new_connections[0]
                    del self._new_connections[0]
                    return connection
            finally:
                self._lock.release()
            if not wait:
                break

    def _connection_finder(self):
        while self._open:
            try:
                connection, address = self._socket.accept()
                address, port = address

                if self._address_white_list is not None and address not in self._address_white_list:
                    raise TCPError("{} is not on white list".format(address))

                if address in self._address_black_list:
                    raise TCPError("{} is on black list".format(address))
                Thread(self._new_connection_handler(connection, address, port)).start()
            except:
                pass

    def _new_connection_handler(self, connection, address, port):
        try:
            new_connection = TCPHost(connection,
                                     address,
                                     port,
                                     self._connection_password,
                                     self._encryption,
                                     self._object_packer,
                                     self._our_information)
            try:
                self._lock.acquire()
                self._new_connections.append(new_connection)
            finally:
                self._lock.release()
        except:
            pass


class TCPBase:
    def __init__(self,
                 connection,
                 address,
                 port,
                 connection_password,
                 encryption=None,
                 object_packer=None,
                 our_information=None):

        self._open = True
        self._send_lock = Lock()
        self._get_lock = Lock()

        self._connection = connection
        self._address = address
        self._port = port
        self._connection_password = connection_password
        self._encryption = encryption

        if self._encryption is None:
            self._encryption = Encryption()
        self._object_packer = object_packer

        if self._object_packer is None:
            self._object_packer = DEFAULT_OBJECT_PACKER_JSON

        self._our_information = our_information

        self._connection_public_key = None
        self._connection_information = None

    def __del__(self):
        self.close()

    def get_address(self):
        return self._address

    def close(self):
        if self._open:
            self._open = False
            self._connection.shutdown(0)
            self._connection.close()

    def get_data(self):
        try:
            self._get_lock.acquire()
            ret_data = self._get_block()
            if self._encryption:
                ret_data = self._encryption.decrypt(ret_data)
            return compress.decompress(ret_data)
        finally:
            self._get_lock.release()

    def send_data(self, data):
        try:
            self._send_lock.acquire()
            data = compress.compress(data)
            if self._encryption:
                data = self._encryption.encrypt_with_public_key(self._connection_public_key, data)
            self._send_block(data)
        finally:
            self._send_lock.release()

    def is_open(self):
        return self._open

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


class TCPHost(TCPBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_name = None
        self._user_id = None
        self._other_information = None
        self._handshake()

    def _handshake(self):
        if self._encryption:
            # send our public key
            self._send_block(self._encryption.get_raw_public_key())
            # get connection public key
            self._connection_public_key = self._get_block()

        # send our information
        self.send_data(self._object_packer.dumps(self._our_information))
        # get connection information
        self._connection_information = self._object_packer.loads(self.get_data())

        if self._connection_information["password"] != self._connection_password:
            raise TCPError("Password was Wrong!")

        self._user_name = self._connection_information["name"]
        self._user_id = self._connection_information["id"]
        self._other_information = self._connection_information["other"]

    def __str__(self):
        return "<{}: {}, {}, {}>".format(self.__class__.__name__,
                                         self._user_name,
                                         self._address,
                                         self._port)

    def get_user_name(self):
        return self._user_name

    def get_user_id(self):
        return self._user_id

    def get_other_data(self):
        return self._other_information


class TCPConnection(TCPBase):
    def __init__(self,
                 host="127.0.0.1",
                 port=4444,
                 ipv6=False,
                 connection_password="",
                 user_name=None,
                 user_id=None,
                 encryption=None,
                 object_packer=None,
                 our_information=None):

        af_mode = socket.AF_INET
        if ipv6:
            af_mode = socket.AF_INET6

        connection = socket.socket(af_mode, socket.SOCK_STREAM)
        connection.connect((host, port))

        connection_password = sha3_512(bytes(connection_password, encoding="utf-8")).hexdigest()

        our_information = {"name": user_name,
                           "id": user_id,
                           "password": connection_password,
                           "other": our_information}
        super().__init__(connection=connection,
                         address=host,
                         port=port,
                         connection_password=connection_password,
                         encryption=encryption,
                         object_packer=object_packer,
                         our_information=our_information)
        self._handshake()

    def _handshake(self):
        if self._encryption:
            # get connection public key
            self._connection_public_key = self._get_block()
            # send our public key
            self._send_block(self._encryption.get_raw_public_key())

        # send our information
        self._connection_information = self._object_packer.loads(self.get_data())
        # get connection information
        self.send_data(self._object_packer.dumps(self._our_information))

    def __str__(self):
        return "<{}: {}, {}>".format(self.__class__.__name__,
                                     self._address,
                                     self._port)
