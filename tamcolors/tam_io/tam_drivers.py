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
    def __init__(self, key_driver_operational=True, *args, **kwargs):
        self._key_driver_operational = key_driver_operational
        super().__init__(*args, **kwargs)

    def get_key(self):
        raise NotImplementedError()

    @staticmethod
    def get_key_dict():
        raise NotImplementedError()

    def key_driver_operational(self):
        return self._key_driver_operational


class ColorDriver(TAMDriver, ABC):
    def __init__(self, color_driver_operational=True, *args, **kwargs):
        self._color_driver_operational = color_driver_operational
        super().__init__(*args, **kwargs)

    def printc(self, output, color, flush, stderr):
        raise NotImplementedError()

    def inputc(self, output, color):
        raise NotImplementedError()

    def set_mode(self, mode):
        super().set_mode(mode)

    def draw(self, tam_buffer):
        super().draw(tam_buffer)

    def _draw_2(self, tam_buffer):
        raise NotImplementedError()

    def _draw_16(self, tam_buffer):
        raise NotImplementedError()

    def _draw_256(self, tam_buffer):
        raise NotImplementedError()

    def _draw_rgb(self, tam_buffer):
        raise NotImplementedError()

    def color_driver_operational(self):
        return self._color_driver_operational


class ColorChangerDriver(TAMDriver, ABC):
    def __init__(self, color_change_driver_operational=True, *args, **kwargs):
        self._color_change_driver_operational = color_change_driver_operational
        super().__init__(*args, **kwargs)

    def get_color(self, spot):
        raise NotImplementedError()

    def set_color(self, spot, color):
        super().set_color(spot, color)

    def _get_console_color(self, spot):
        raise NotImplementedError()

    def _set_console_color(self, spot, color):
        raise NotImplementedError()

    def console_color_count(self):
        raise NotImplementedError()

    def color_change_driver_operational(self):
        return self._color_change_driver_operational


class UtilitiesDriver(TAMDriver, ABC):
    def __init__(self, utilities_driver_operational=True, *args, **kwargs):
        self._utilities_driver_operational = utilities_driver_operational
        super().__init__(*args, **kwargs)

    def get_dimensions(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def show_console_cursor(self, show):
        raise NotImplementedError()

    def utilities_driver_operational(self):
        return self._utilities_driver_operational
