# tamcolors libraries
from abc import ABC
from tamcolors.tam_io import tam_drivers


class ANYKeyDriver(tam_drivers.KeyDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("key_driver_operational", False)
        super().__init__(*args, **kwargs)

    def get_key(self):
        return False

    @staticmethod
    def get_key_dict():
        raise {}


class ANYColorDriver(tam_drivers.ColorDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("color_driver_operational", False)
        kwargs.setdefault("mode_16", False)
        kwargs.setdefault("mode_256", False)
        kwargs.setdefault("mode_rgb", False)
        super().__init__(*args, **kwargs)

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

    def draw(self, tam_buffer):
        super().draw(tam_buffer)

    def _draw_2(self, tam_buffer):
        print(tam_buffer)


class ANYColorChangerDriver(tam_drivers.ColorChangerDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("color_changer_driver_operational", False)
        super().__init__(*args, **kwargs)

    def get_color(self, spot):
        return self._color_palette[spot]

    def set_color(self, spot, color):
        super().set_color(spot, color)

    def _get_console_color(self, spot):
        pass

    def _set_console_color(self, spot, color):
        pass

    def _console_color_count(self):
        return 0


class ANYUtilitiesDriver(tam_drivers.UtilitiesDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("utilities_driver_operational", False)
        super().__init__(*args, **kwargs)

    def get_dimensions(self):
        return 85, 25

    def clear(self):
        pass

    def show_console_cursor(self, show):
        pass
