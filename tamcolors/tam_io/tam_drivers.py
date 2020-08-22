from abc import ABC

from tamcolors.tam_io.io_tam import IO


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
        return True


class KeyDriver(TAMDriver, ABC):
    def __init__(self, key_driver_operational=True, *args, **kwargs):
        """
        info: Makes part of IO
        :param key_driver_operational: bool
        :param args: *args
        :param kwargs: **kwargs
        """
        self._key_driver_operational = key_driver_operational
        super().__init__(*args, **kwargs)

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

    def key_driver_operational(self):
        """
        info: checks if the key driver is operational
        :return: bool
        """
        return self._key_driver_operational


class ColorDriver(TAMDriver, ABC):
    def __init__(self, color_driver_operational=True, *args, **kwargs):
        """
        info: Makes part of IO
        :param color_driver_operational: bool
        :param args: *args
        :param kwargs: **kwargs
        """
        self._color_driver_operational = color_driver_operational
        super().__init__(*args, **kwargs)

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

    def color_driver_operational(self):
        """
        info: checks if the color driver is operational
        :return: bool
        """
        return self._color_driver_operational


class ColorChangerDriver(TAMDriver, ABC):
    def __init__(self, color_changer_driver_operational=True, *args, **kwargs):
        """
        info: Makes part of IO
        :param color_changer_driver_operational: bool
        :param args: *args
        :param kwargs: **kwargs
        """
        self._color_changer_driver_operational = color_changer_driver_operational
        super().__init__(*args, **kwargs)

    def get_color(self, spot):
        """
        info: Will get color from color palette
        :param spot: int
        :return: RGBA
        """
        return super().get_color(spot)

    def set_color(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        super().set_color(spot, color)

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

    def color_changer_driver_operational(self):
        """
        info: checks if the color changer driver is operational
        :return: bool
        """
        return self._color_changer_driver_operational

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        super().set_mode(mode)


class FullColorDriver(ColorDriver, ColorChangerDriver, ABC):
    pass


class UtilitiesDriver(TAMDriver, ABC):
    def __init__(self, utilities_driver_operational=True, *args, **kwargs):
        """
        info: Makes part of IO
        :param utilities_driver_operational: bool
        :param args: *args
        :param kwargs: **kwargs
        """
        self._utilities_driver_operational = utilities_driver_operational
        super().__init__(*args, **kwargs)

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
        raise NotImplementedError()

    def show_console_cursor(self, show):
        """
        info: Will show or hide console cursor
        :param show: int
        :return: None
        """
        raise NotImplementedError()

    def utilities_driver_operational(self):
        """
        info: checks if the utilities driver is operational
        :return: bool
        """
        return self._utilities_driver_operational
