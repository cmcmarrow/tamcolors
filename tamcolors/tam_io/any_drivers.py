# tamcolors libraries
from abc import ABC
from tamcolors.tam_io import tam_drivers
from tamcolors.tam_io import io_tam


class ANYKeyDriver(tam_drivers.KeyDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("key_driver_operational", False)
        super().__init__(*args, **kwargs)

    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
        """
        return False

    @staticmethod
    def get_key_dict():
        """
        info: Gets a dict of all the keys
        :return: {str: (str, str), ...}
        """
        raise {}


class ANYColorDriver(tam_drivers.ColorDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("color_driver_operational", False)
        kwargs.setdefault("mode_16", False)
        kwargs.setdefault("mode_256", False)
        kwargs.setdefault("mode_rgb", False)
        super().__init__(*args, **kwargs)

    def printc(self, output, color, flush, stderr):
        """
        info: will print out user output with color
        :param output: str
        :param color: tuple: (int, int)
        :param flush: boolean
        :param stderr: boolean
        :return: None
        """
        self._write_to_output_stream(output, flush, stderr)

    def inputc(self, value, color):
        """
        info: will get user input with color
        :param value: str
        :param color: tuple: (int, int)
        :return: str
        """
        return input(value)

    def get_printc_mode(self):
        """
        Gets the modes used by printc and inputc
        :return: str
        """
        return io_tam.MODE_2

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
        print(tam_buffer)


class ANYColorChangerDriver(tam_drivers.ColorChangerDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("color_changer_driver_operational", False)
        super().__init__(*args, **kwargs)

    def _get_console_color(self, spot):
        """
        info: Will get a console color
        :param spot: int
        :return: RGBA
        """
        pass

    def _set_console_color(self, spot, color):
        """
        info: Will set a console color
        :param spot: int
        :param color: RGBA
        :return: None
        """
        pass

    def _console_color_count(self):
        """
        info: Get console color
        :return: int
        """
        return 0


class ANYUtilitiesDriver(tam_drivers.UtilitiesDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("utilities_driver_operational", False)
        super().__init__(*args, **kwargs)

    def get_dimensions(self):
        """
        info: Gets the dimensions of console
        :return: (int, int): (row, column)
        """
        return 85, 25

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
