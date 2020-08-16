# tamcolors libraries
from abc import ABC
from tamcolors.tam_io import tam_drivers


class ANYKeyDriver(tam_drivers.KeyDriver, ABC):
    def get_key(self):
        raise False

    @staticmethod
    def get_key_dict():
        raise {}


class ANYColorDriver(tam_drivers.ColorDriver, ABC):
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

    def _draw_16(self, tam_buffer):
        print(tam_buffer)


class ANYColorChangedDriver(tam_drivers.ColorChangedDriver, ABC):
    def get_color(self, spot):
        return self._colors[spot]

    def set_color(self, spot, color):
        super().set_color(spot, color)


class ANYUtilitiesDriver(tam_drivers.UtilitiesDriver, ABC):
    def get_dimensions(self):
        return 85, 25

    def clear(self):
        pass

    def show_console_cursor(self, show):
        pass
