# tamcolors libraries
from . import io_tma
from . import uni_tma
from . import win_tma


""" 
AnyIO 
support all environments
does not have key input support
"""


class AnyIOError(Exception):
    pass

asdf
class AnyIO(io_tma.IO):
    def __init__(self):
        super().__init__()
        self.__mode = 16

    @classmethod
    def get_io(cls):
        """
        info: will see if environment supported by AnyIO
        :return: AnyIO object or None
        """
        if hasattr(cls, 'any_io'):
            return cls.any_io
        cls.any_io = AnyIO()
        return cls.any_io

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        self.__mode = mode

    def get_mode(self):
        """
        info: will return the current color mode
        :return: int
        """
        return self.__mode

    def get_modes(self):
        return 2, 16

    def draw(self, tma_buffer):
        """
        info: draws tma_buffer to terminal
        :param tma_buffer:
        :return:
        """

        print(tma_buffer)

    def _draw_2(self, tma_buffer):
        pass

    def _draw_16(self, tma_buffer):
        pass

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


def get_io(io_list=None, any_os=False):
    """
    info: gets the right io for environment
    :param io_list: list, tuple, None: ios that can be used
    :param any_os: bool
    :return: IO or None
    """

    # if io_list use default ios
    if io_list is None:
        io_list = (win_tma.WinIO, uni_tma.UniIO)

    for io in io_list:
        io_object = io.get_io()
        if io_object is not None:
            return io_object

    if any_os:
        return AnyIO.get_io()
    return None
