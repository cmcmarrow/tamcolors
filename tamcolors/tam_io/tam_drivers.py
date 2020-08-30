# built in library
from abc import ABC

# tamcolors library
from tamcolors.tam_io.io_tam import IO


"""
Holds all the core drivers to build an IO
"""


class TAMDriver(IO, ABC):
    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        super().start()

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        super().done()

    @classmethod
    def able_to_execute(cls):
        """
        info: checks that io is stable in current environment
        :return: bool
        """
        return super().able_to_execute()


class KeyDriver(TAMDriver, ABC):
    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
        """
        raise NotImplementedError()

    @staticmethod
    def get_key_dict():
        """
        info: Gets a dict of all the keys
        :return: {str: (str, str), ...}
        """
        raise NotImplementedError()

    def enable_console_keys(self, enable):
        super().enable_console_keys(enable)


class ColorDriver(TAMDriver, ABC):
    def printc(self, output, color, flush, stderr):
        """
        info: Will print to the console in color
        :param output: str
        :param color: COLOR
        :param flush: bool
        :param stderr: std
        :return:
        """
        raise NotImplementedError()

    def inputc(self, output, color):
        """
        info: Will get input from the console in color
        :param output: str
        :param color: COLOR
        :return: str
        """
        raise NotImplementedError()

    def get_printc_mode(self):
        """
        Gets the modes used by printc and inputc
        :return: str
        """
        raise NotImplementedError()

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        super().set_mode(mode)

    def draw(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console
        :param tam_buffer: TAMBuffer
        :return: None
        """
        super().draw(tam_buffer)

    def _draw_2(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 2
        :param tam_buffer: TAMBuffer
        :return: None
        """
        raise NotImplementedError()

    def _draw_16(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 16
        :param tam_buffer: TAMBuffer
        :return: None
        """
        raise NotImplementedError()

    def _draw_256(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 256
        :param tam_buffer: TAMBuffer
        :return: None
        """
        raise NotImplementedError()

    def _draw_rgb(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode rgb
        :param tam_buffer: TAMBuffer
        :return: None
        """
        raise NotImplementedError()


class ColorChangerDriver(TAMDriver, ABC):
    def get_color_2(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: RGBA
        """
        return super().get_color_2(spot)

    def get_color_16(self, spot):
        """
        info: Will get color from color palette 16
        :param spot: int
        :return: RGBA
        """
        return super().get_color_16(spot)

    def get_color_256(self, spot):
        """
        info: Will get color from color palette 256
        :param spot: int
        :return: RGBA
        """
        return super().get_color_256(spot)

    def set_color_2(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        super().set_color_2(spot, color)

    def set_color_16(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        super().set_color_16(spot, color)

    def set_color_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        super().set_color_256(spot, color)

    def _get_console_color(self, spot):
        """
        info: Will get a console color
        :param spot: int
        :return: RGBA
        """
        raise NotImplementedError()

    def _set_console_color(self, spot, color):
        """
        info: Will set a console color
        :param spot: int
        :param color: RGBA
        :return: None
        """
        raise NotImplementedError()

    def _console_color_count(self):
        """
        info: Get console color
        :return: int
        """
        raise NotImplementedError()

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        super().set_mode(mode)


class UtilitiesDriver(TAMDriver, ABC):
    def get_dimensions(self):
        """
        info: Gets the dimensions of console
        :return: (int, int): (row, column)
        """
        raise NotImplementedError()

    def clear(self):
        """
        info: Will clear the console
        :return: None
        """
        super().clear()

    def show_console_cursor(self, show):
        """
        info: Will show or hide console cursor
        :param show: int
        :return: None
        """
        super().show_console_cursor(show)


class FullColorDriver(ColorDriver, ColorChangerDriver, ABC):
    pass

