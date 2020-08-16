import sys
from abc import ABC

from tamcolors.tam_io.io_tam import IO


class TAMDriver(IO, ABC):
    def start(self):
        pass

    def done(self):
        pass

    @classmethod
    def able_to_execute(cls):
        return True


class KeyDriver(TAMDriver, ABC):
    def get_key(self):
        raise NotImplementedError()

    @staticmethod
    def get_key_dict():
        raise NotImplementedError()


class ColorDriver(TAMDriver, ABC):
    def printc(self, output, color, flush, stderr):
        raise NotImplementedError()

    def inputc(self, output, color):
        raise NotImplementedError()

    def draw(self, tam_buffer):
        super().draw(tam_buffer)

    def _draw_2(self, tam_buffer):
        raise NotImplementedError()

    def _draw_16(self, tam_buffer):
        raise NotImplementedError()


class ColorChangedDriver(TAMDriver, ABC):
    def get_color(self, spot):
        raise NotImplementedError()

    def set_color(self, spot, color):
        super().set_color(spot, color)


class UtilitiesDriver(TAMDriver, ABC):
    def get_dimensions(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def show_console_cursor(self, show):
        raise NotImplementedError()
