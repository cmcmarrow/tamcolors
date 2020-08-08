# tamcolors libraries
from . import io_tam
from . import uni_tam
from . import win_tam


""" 
AnyIO 
support all environments
does not have key input support
"""


class AnyIOError(Exception):
    pass


class AnyIO(io_tam.SingletonIO):
    def __init__(self):
        super().__init__()

    @classmethod
    def able_to_execute(cls):
        """
        info: will see if environment supported by AnyIO
        :return: bool
        """
        return True

    def _draw_2(self, tam_buffer):
        print(tam_buffer)

    def _draw_16(self, tam_buffer):
        print(tam_buffer)

    def start(self):
        pass

    def done(self):
        pass

    def get_key(self):
        """
        info: AnyIO can't get key input
        :return: False
        """
        return False

    def get_dimensions(self):
        return 85, 25

    def get_key_dict(self):
        return {}

    def printc(self, value, color, flush, stderr):
        """
        info: will print out user output with color
        :param value: str
        :param color: tuple: (int, int)
        :param flush: boolean
        :param stderr: boolean
        :return: None
            """
        self._write_to_output_stream(value, flush, stderr)

    def inputc(self, value, color):
        """
        info: will get user input with color
        :param value: str
        :param color: tuple: (int, int)
        :return: str
        """
        return input(value)

    def clear(self):
        pass


def get_io(io_list=None, any_os=False):
    """
    info: gets the right io for environment
    :param io_list: list, tuple, None: ios that can be used
    :param any_os: bool
    :return: IO or None
    """

    # if io_list use default ios
    if io_list is None:
        io_list = (win_tam.WinIO, uni_tam.UniIO)

    for io in io_list:
        io_object = io()
        if io_object is not None:
            return io_object

    if any_os:
        return AnyIO()
    return None
