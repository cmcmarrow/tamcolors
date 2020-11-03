from threading import Thread, Lock
import socket
from functools import partial
from tamcolors.utils.encryption import Encryption
from tamcolors.utils import compress
from tamcolors.utils.object_packer import DEFAULT_OBJECT_PACKER_JSON
from tamcolors.utils import log
from tamcolors.utils import transport_optimizer
from hashlib import sha512
from time import sleep


TCP_TIMEOUT = 60


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
        """
        info: will receive a TCP connection
        :param host: str: ipv4 or ipv6
        :param port: int
        :param ipv6: bool
        :param listen_count: int: max number of connections that can be received at once
        :param connection_password: str: password that all connections most have
        :param address_white_list: tuple, list, set: addresses that are allowed
        :param address_black_list: tuple, list, set: addresses that are not allowed
        :param encryption: None, False, Encryption
        :param object_packer: None, ObjectPacker
        :param our_information: object: that can be dumped by the passed object packer
        """
        try:
            self._host = host
            self._port = port
            self._open = False

            af_type = socket.AF_INET
            if ipv6:
                af_type = socket.AF_INET6

            self._socket = socket.socket(af_type, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self._host, self._port))
            self._open = True
            self._socket.listen(listen_count)

            self._connection_password = sha512(bytes(connection_password, encoding="utf-8")).hexdigest()
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

            # start connection finder daemon thread
            Thread(target=self._connection_finder, daemon=True).start()
        except Exception as e:
            raise TCPError(str(e))

    def __enter__(self):
        """
        info: will make a TCPReceiver object
        :return: TCPReceiver
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        info: will make sure tcp receiver connection is closed
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: None
        """
        self.close()

    def __del__(self):
        """
        info: last ditch effort to try and close tcp receiver connection
        :return:
        """
        self.close()

    def close(self):
        """
        info: will close tcp receiver connection
        :return: None
        """
        if self._open:
            self._open = False
            try:
                self._socket.shutdown(0)
            except OSError as e:
                log.warning("tcp shutdown error: %s", str(e))
            self._socket.close()

    def get_host_connection(self, wait=True):
        """
        info: will get a new host connection
        :param wait: bool: if true will wait for a connection
        :return: None or TCPHost
        """
        while True:
            try:
                self._lock.acquire()
                if len(self._new_connections):
                    # new connections are present
                    connection = self._new_connections[0]
                    # remove new connection from connection queue
                    del self._new_connections[0]
                    return connection
            finally:
                self._lock.release()
            # if wait == false return None
            if not wait:
                break

    def _connection_finder(self):
        """
        info: will receive and new connection and start a new daemon thread to handle it
        :return: None
        """
        while self._open:
            try:
                # get new raw tcp connection
                connection, address = self._socket.accept()
                address, port = address[0], address[1]

                # check if new connection is in white list
                if self._address_white_list is not None and address not in self._address_white_list:
                    raise TCPError("{} is not on white list".format(address))
                # check if new connection is in not in black list
                if address in self._address_black_list:
                    raise TCPError("{} is on black list".format(address))

                # hand new connection over to new connection handler
                Thread(target=self._new_connection_handler, args=(connection, address, port), daemon=True).start()
            except Exception as error:
                log.warning("_connection_finder error %s %s: %s",
                            self._host,
                            self._port,
                            error)

    def _new_connection_handler(self, connection, address, port):
        """
        info: will setup a TCPHost connection
        :param connection: socket connection
        :param address: str
        :param port: int
        :return: None
        """
        try:
            connection.settimeout(TCP_TIMEOUT)
            new_connection = TCPHost(connection,
                                     address,
                                     port,
                                     self._connection_password,
                                     self._encryption,
                                     self._object_packer,
                                     self._our_information)
            try:
                self._lock.acquire()
                # TCPHost connection init has no error
                # TCPHost is ready to be placed int the new connections queue
                self._new_connections.append(new_connection)
            finally:
                self._lock.release()
        except Exception as error:
            log.warning("_new_connection_handler error %s %s: %s",
                        self._host,
                        self._port,
                        error)


class TCPBase:
    def __init__(self,
                 connection,
                 address,
                 port,
                 connection_password,
                 encryption=None,
                 object_packer=None,
                 our_information=None):
        """
        info: is the base class for TCP connections
        :param connection: socket connection
        :param address: str
        :param port: int
        :param connection_password: str
        :param encryption: None, False, Encryption
        :param object_packer: ObjectPacker
        :param our_information: object
        """

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
        """
        info: will try to close the connection
        :return: None
        """
        self.close()

    def get_address(self):
        """
        info: will get the address
        :return: str
        """
        return self._address

    def close(self):
        """
        info: will close the connection
        :return: None
        """
        if hasattr(self, "_open") and self._open:
            self._open = False
            try:
                self._connection.shutdown(0)
            except OSError as e:
                log.warning("tcp shutdown error: %s", str(e))
            self._connection.close()

    def get_data(self):
        """
        info: will compress and encrypt data if encryption is enabled
        :return: bytes
        """
        try:
            self._get_lock.acquire()
            ret_data = self._get_block()
            if self._encryption:
                ret_data = self._encryption.decrypt(ret_data)
            return compress.decompress(ret_data)
        except Exception as e:
            raise TCPError(str(e))
        finally:
            self._get_lock.release()

    def send_data(self, data):
        """
        info: will compress and decrypt if encryption is enabled
        :param data: bytes
        :return: None
        """
        try:
            self._send_lock.acquire()
            data = compress.compress(data)
            if self._encryption:
                data = self._encryption.encrypt_with_public_key(self._connection_public_key, data)
            self._send_block(data)
        except Exception as e:
            raise TCPError(str(e))
        finally:
            self._send_lock.release()

    def is_open(self):
        """
        info: will check if connection is open
        :return: bool
        """
        return self._open

    def _send_block(self, data):
        """
        info: will send bytes to the connection
        :param data: bytes
        :return: None
        """
        data_size = len(data)
        data_size_in_bytes = data_size.to_bytes(data_size.bit_length() // 8 + min(data_size.bit_length() % 8, 1),
                                                byteorder="big")
        number_size = len(data_size_in_bytes)
        self._connection.send(bytes((number_size,)) + data_size_in_bytes + data)

    def _get_block(self):
        """
        info: will get bytes from the connection
        :return: bytes
        """
        number_size = self._connection.recv(1)[0]
        data_size = int.from_bytes(self._connection.recv(number_size), "big")
        return self._connection.recv(data_size)


class TCPHost(TCPBase):
    def __init__(self, *args, **kwargs):
        """
        info: is a connection handler for the host
        :param args: *args
        :param kwargs: **kwargs
        """
        try:
            super().__init__(*args, **kwargs)
            self._user_name = None
            self._user_id = None
            self._other_information = None
            self._handshake()
        except Exception as e:
            raise TCPError(str(e))

    def _handshake(self):
        """
        info: will verify connection
        :return: None
        """
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
        """
        info: get connection name
        :return: str
        """
        return self._user_name

    def get_user_id(self):
        """
        info: get connection id
        :return: bytes
        """
        return self._user_id

    def get_other_data(self):
        """
        info: will get other data
        :return: object
        """
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
        """
        info: is a connection handler for the connection
        :param host: str
        :param port: int
        :param ipv6: bool
        :param connection_password: str
        :param user_name: str
        :param user_id: None, bytes
        :param encryption: None, False, Encryption
        :param object_packer: ObjectPacker
        :param our_information: object
        """

        try:
            af_mode = socket.AF_INET
            if ipv6:
                af_mode = socket.AF_INET6

            connection = socket.socket(af_mode, socket.SOCK_STREAM)
            connection.settimeout(TCP_TIMEOUT)
            connection.connect((host, port))

            connection_password = sha512(bytes(connection_password, encoding="utf-8")).hexdigest()

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
        except Exception as e:
            raise TCPError(str(e))

    def _handshake(self):
        """
        info: will verify connection
        :return: None
        """
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

    def get_other_data(self):
        """
        info: will get other data
        :return: object
        """
        return self._connection_information


class TCPObjectWrapper:
    def __init__(self, tcp_connection, obj, object_packer=None):
        """
        info: Makes a TCPObjectWrapper object
        :param tcp_connection: TCPBase
        :param obj: object
        :param object_packer: ObjectPacker or None
        """
        self._tcp_connection = tcp_connection
        self._obj = obj

        # use default object packer if none is given
        if object_packer is None:
            object_packer = DEFAULT_OBJECT_PACKER_JSON
        self._object_packer = object_packer
        self._transport_optimizers = {}

        self._open = True

    def __call__(self):
        """
        info: let other program call object methods
        :return:
        """
        while self.is_open():
            action = self._tcp_connection.get_data()
            Thread(target=self._action_thread, args=(action,), daemon=True).start()

    def __del__(self):
        """
        info: last try to close object
        :return:
        """
        self.close()

    def is_open(self):
        """
        info: will check if object is still open
        :return: bool
        """
        return self._open

    def close(self):
        """
        info: will close the object
        :return:
        """
        if self._open:
            self._open = False
            self._tcp_connection.close()

    def get_connection(self):
        """
        info: will get connection
        :return: TCPBase
        """
        return self._tcp_connection

    def _action_thread(self, action):
        """
        info: will run an action
        :param action: bytes
        :return:
        """
        try:
            # unpack action
            action_dict = self._object_packer.loads(action)

            # uncompress data
            if "optimizer" in action_dict:
                # init lase received cache if target does not have one
                if action_dict["target"] not in self._transport_optimizers:
                    self._transport_optimizers[action_dict["target"]] = transport_optimizer.LastReceivedCache()
                action_dict = self._transport_optimizers[action_dict["target"]](action_dict["optimizer"])
                action_dict = self._object_packer.loads(action_dict)

            # get action id
            action_id = action_dict.get("id")
            try:
                func = getattr(self._obj, action_dict["target"])
                # call func
                ret = func(*action_dict.get("args", ()), **action_dict.get("kwargs", {}))
                # return data
                if action_id is not None:
                    self._tcp_connection.send_data(self._object_packer.dumps({"id": action_id, "return": ret}))
            except Exception as e:
                # return error
                if action_id is not None:
                    self._tcp_connection.send_data(self._object_packer.dumps({"id": action_id, "error": str(e)}))
                raise e
        except Exception as e:
            log.critical("_action_thread error: %s data: %s", e, action)


class TCPObjectConnector:
    def __init__(self, tcp_connection, object_packer=None, no_return=None, optimizer=None):
        """
        info: Makes a TCPObjectConnector
        :param tcp_connection: TCPBase
        :param object_packer: ObjectPacker or None
        :param no_return: set or None: {func: str, ...}
        :param optimizer: set or None: {func: str, ...}
        """
        self._tcp_connection = tcp_connection

        # use default object packer if none is given
        if object_packer is None:
            object_packer = DEFAULT_OBJECT_PACKER_JSON
        self._object_packer = object_packer

        if no_return is None:
            no_return = set()
        self._no_return = no_return

        if optimizer is None:
            optimizer = set()
        self._transport_optimizers = {func: transport_optimizer.LastSentCache() for func in optimizer}

        self._open = True

        self._id_lock = Lock()
        self._allocated_ids = set()
        self._free_ids = []

        self._call_cache = {}

        self._return_data = {}
        Thread(target=self._return_collector, daemon=True).start()

    def __call__(self, func, *args, **kwargs):
        """
        info: will call an object method in the other program
        :param func: str: name of method
        :param args: *args
        :param kwargs: **kwargs
        :return: object
        """
        if self._open:
            action_id = None
            # don't give action an id if func is in no return
            # this is so __call__ does not wait for a return
            if func not in self._no_return:
                action_id = self._get_id()

            # make action dict
            action = {"id": action_id,
                      "target": func,
                      "args": args,
                      "kwargs": kwargs}

            # call object method
            if func not in self._transport_optimizers:
                self._tcp_connection.send_data(self._object_packer.dumps(action))
            else:   # compress data being sent with transport optimizers
                compress_data = {"optimizer": self._transport_optimizers[func](self._object_packer.dumps(action)),
                                 "target": func}
                self._tcp_connection.send_data(self._object_packer.dumps(compress_data))

            # if action has an id wait for return data
            if action_id is not None:
                while self._open:
                    if action_id in self._return_data:
                        ret = self._return_data[action_id]
                        break
                    elif "error" in self._return_data:
                        raise self._return_data["error"]
                    sleep(0.0001)
                del self._return_data[action_id]
                self._free_id(action_id)
                # check for error
                if "error" in ret:
                    raise TCPError(ret["error"])
                return ret["return"]

    def __del__(self):
        """
        info: last try to close object
        :return:
        """
        self.close()

    def __getattribute__(self, item):
        """
        info: will get object attribute
        :param item: str
        :return: object
        """
        try:
            return super().__getattribute__(item)
        except AttributeError:
            # if object is missing attribute assume programs wants to call that func
            p = self._call_cache.get(item)
            if p is not None:
                return p
            p = partial(self.__call__, item)
            self._call_cache[item] = p
            return p

    def is_open(self):
        """
        info: will check if object is still open
        :return: bool
        """
        return self._open

    def close(self):
        """
        info: will close the object
        :return:
        """
        if self._open:
            self._open = False
            self._tcp_connection.close()

    def _return_collector(self):
        try:
            while self._open:
                try:
                    ret = self._object_packer.loads(self._tcp_connection.get_data())
                    self._return_data[ret["id"]] = ret
                except Exception as e:
                    self._return_data["error"] = e
        except Exception as e:
            log.critical("_return_collector error: %s", str(e))

    def get_connection(self):
        """
        info: will get connection
        :return: TCPBase
        """
        return self._tcp_connection

    def _get_id(self):
        """
        info: will get a free id
        :return: int
        """
        try:
            self._id_lock.acquire()
            action_id = len(self._allocated_ids)
            if self._free_ids:
                action_id = self._free_ids.pop()
            self._allocated_ids.add(action_id)
            return action_id
        finally:
            self._id_lock.release()

    def _free_id(self, action_id):
        """
        info: will free an id
        :param action_id: int
        :return:
        """
        try:
            self._id_lock.acquire()
            self._allocated_ids.remove(action_id)
            self._free_ids.append(action_id)
            # no ids are being used
            # it is safe to remove all free ids
            if not len(self._allocated_ids):
                self._free_ids.clear()
        finally:
            self._id_lock.release()
