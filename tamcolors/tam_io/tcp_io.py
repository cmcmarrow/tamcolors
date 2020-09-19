import socket
import json
from .io_tam import RawIO
from . import tam_identifier
from .tam_buffer import TAMBuffer
from threading import Lock

'''
class TCPIO:
    def __init__(self, address="127.0.0.1", port=4444, ipv6=False, encrypted=True, io=None):
        """
        info: Makes a TCP IO object
        :param address: str
        :param port: int
        :param ipv6: bool
        :param encrypted: bool
        """
        self._address = address
        self._port = port
        self._ipv6 = ipv6
        self._encrypted = encrypted

        if io is None:
            io = tam_identifier.IO
        self._io = io

        af_protocol = socket.AF_INET
        if self._ipv6:
            af_protocol = socket.AF_INET6
        self._socket = socket.socket(af_protocol, socket.SOCK_STREAM)
        print("lol")
        self._socket.connect((address, port))
        print("hi")
        self._run()

    def _run(self):
        while True:
            size = int.from_bytes(self._socket.recv(4), byteorder="big", signed=False)
            data = self._socket.recv(size)

            if data[0] == 0:
                buffer = TAMBuffer.from_bytes(data[1:])
                self._io.draw(buffer)
            else:
                data = json.loads(str(data[1:], encoding="utf-8"))
                ret = getattr(self._io, data["call"])(*data["args"])
                print(ret)
                if ret is not None:
                    ret = json.dumps(ret)
                    self._socket.send(len(ret).to_bytes(4, byteorder="big", signed=False))
                    self._socket.send(bytes(ret, encoding="utf-8"))


class TCPIOHost(RawIO):
    def __init__(self, address="127.0.0.1", port=4444, ipv6=False, encrypted=True):
        self._address = address
        self._port = port
        self._ipv6 = ipv6
        self._encrypted = encrypted

        af_protocol = socket.AF_INET
        if self._ipv6:
            af_protocol = socket.AF_INET6

        print(1)
        self._socket = socket.socket(af_protocol, socket.SOCK_STREAM)
        print(2)
        self._socket.bind((address, port))
        print(3)
        self._socket.listen(0)
        print(4)
        self._socket, _ = self._socket.accept()
        print(5)
        self._lock = Lock()

    def _send_no_ret(self, call, args):
        self._lock.acquire()
        data = json.dumps({"call": call, "args": args})
        data = bytes(data, encoding="utf-8")
        self._socket.send((len(data) + 1).to_bytes(4, byteorder="big", signed=False))
        self._socket.send(bytes((1,)))
        self._socket.send(data)
        self._lock.release()

    def _send_ret(self, call, args):
        self._lock.acquire()
        data = json.dumps({"call": call, "args": args})
        data = bytes(data, encoding="utf-8")
        self._socket.send((len(data) + 1).to_bytes(4, byteorder="big", signed=False))
        self._socket.send(bytes((1,)))
        self._socket.send(data)

        data_size = int.from_bytes(self._socket.recv(4), byteorder="big", signed=False)
        ret = json.loads(str(self._socket.recv(data_size), encoding="utf-8"))
        self._lock.release()
        return ret

    def __str__(self):
        return self._send_no_ret("__str__", ())

    def able_to_execute(self):
        """
        info: checks that io is stable in current environment
        :return: bool
        """
        return self._send_ret("able_to_execute", ())

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        return self._send_no_ret("set_mode", (mode,))

    def get_mode(self):
        """
        info: will return the current color mode
        :return: int
        """
        return self._send_ret("get_mode", ())

    def get_modes(self):
        """
        info: will return a tuple of all color modes
        :return: (int, int, ...)
        """
        return self._send_ret("get_modes", ())

    def draw(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console
        :param tam_buffer: TAMBuffer
        :return: None
        """
        pass

    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        return self._send_no_ret("start", ())

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        return self._send_no_ret("done", ())

    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
        """
        return self._send_ret("get_key", ())

    def get_dimensions(self):
        """
        info: Gets the dimensions of console
        :return: (int, int): (row, column)
        """
        return self._send_ret("get_dimensions", ())

    def printc(self, output, color, flush, stderr):
        """
        info: Will print to the console in color
        :param output: str
        :param color: COLOR
        :param flush: bool
        :param stderr: bool
        :return:
        """
        return self._send_no_ret("printc", (output, color, flush, stderr))

    def inputc(self, output, color):
        """
        info: Will get input from the console in color
        :param output: str
        :param color: COLOR
        :return: str
        """
        return self._send_ret("inputc", (output, color))

    def clear(self):
        """
        info: Will clear the console
        :return: None
        """
        return self._send_no_ret("clear", ())

    def show_console_cursor(self, show):
        """
        info: Will show or hide console cursor
        :param show: int
        :return: None
        """
        return self._send_no_ret("show_console_cursor", ())

    def utilities_driver_operational(self):
        """
        info: checks if the utilities driver is operational
        :return: bool
        """
        return self._send_ret("utilities_driver_operational", ())

    def color_change_driver_operational(self):
        """
        info: checks if the color changer driver is operational
        :return: bool
        """
        return self._send_ret("color_change_driver_operational", ())

    def color_driver_operational(self):
        """
        info: checks if the color driver is operational
        :return: bool
        """
        return self._send_ret("color_driver_operational", ())

    def key_driver_operational(self):
        """
        info: checks if the key driver is operational
        :return: bool
        """
        return self._send_ret("key_driver_operational", ())

    def get_key_dict(self):
        """
        info: Gets a dict of all the keys
        :return: {str: (str, str), ...}
        """
        return self._send_ret("get_key_dict", ())

    def reset_colors_to_console_defaults(self):
        """
        info: will reset colors to console defaults
        :return: None
        """
        return self._send_no_ret("reset_colors_to_console_defaults", ())

    def set_tam_color_defaults(self):
        """
        info: will set console colors to tam defaults
        :return: None
        """
        return self._send_no_ret("set_tam_color_defaults", ())

    def get_info_dict(self):
        """
        info: will get the identifier dict
        :return: dict
        """
        return self._send_ret("get_info_dict", ())

    def color_changer_driver_operational(self):
        """
        info: checks if the color changer driver is operational
        :return: bool
        """
        return self._send_ret("color_changer_driver_operational", ())

    def enable_console_keys(self, enable):
        """
        info: will enable console keys
        :param enable: boool
        :return: None
        """
        return self._send_no_ret("enable_console_keys", (enable,))

    def get_color_2(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: RGBA
        """
        raise NotImplementedError()

    def get_color_16(self, spot):
        """
        info: Will get color from color palette 16
        :param spot: int
        :return: RGBA
        """
        raise NotImplementedError()

    def get_color_256(self, spot):
        """
        info: Will get color from color palette 256
        :param spot: int
        :return: RGBA
        """
        raise NotImplementedError()

    def get_printc_mode(self):
        """
        Gets the modes used by printc and inputc
        :return: str
        """
        raise NotImplementedError()

    def is_console_cursor_enabled(self):
        """
        info: will check if console cursor is enabled
        :return: bool
        """
        raise NotImplementedError()

    def is_console_keys_enabled(self):
        """
        info: will check if console keys enabled
        :return: bool
        """
        raise NotImplementedError()

    def set_color_2(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        raise NotImplementedError()

    def set_color_16(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        raise NotImplementedError()

    def set_color_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        raise NotImplementedError()
'''
