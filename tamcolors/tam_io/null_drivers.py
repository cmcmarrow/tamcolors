# built in library
from abc import ABC

# tamcolors library
from tamcolors.tam_io import tam_drivers, tam_keys, io_tam


class NULLKeyDriver(tam_drivers.KeyDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("key_driver_operational", False)
        super().__init__(*args, **kwargs)

    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
        """
        return False

    def wait_key(self, rest_time=0.0001, attempts=300000):
        """
        info: Get an input from the terminal
        :param: rest_time: float: rest time from checking if a key is down
        :param: attempts: int: number of attempts to get a key
        :return: tuple or false
        """
        return False

    @classmethod
    def get_key_dict(self, language=None):
        """
        info: Gets a dict of all the keys
        :param language: str or None
        :return: dict
        """
        return {}

    def get_keyboard_name(self, default_to_us_english=True):
        """
        info: Will get the keyboard language name
        :param default_to_us_english: bool
        :return: str
        """
        if default_to_us_english:
            return tam_keys.LANGUAGE_US_ENGLISH
        return tam_keys.LANGUAGE_UNKNOWN


class NULLFullColorDriver(tam_drivers.FullColorDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("color_driver_operational", False)
        kwargs.setdefault("color_changer_driver_operational", False)
        kwargs.setdefault("mode_rgb", False)
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
        pass

    def inputc(self, output, color):
        """
        info: Will get input from the console in color
        :param output: str
        :param color: COLOR
        :return: str
        """
        pass

    def get_printc_mode(self):
        """
        Gets the modes used by printc and inputc
        :return: str
        """
        return io_tam.MODE_2

    def _draw_2(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 2
        :param tam_surface: TAMSurface
        :return: None
        """
        pass

    def _draw_16_pal_256(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 16_pal_256
        :param tam_surface: TAMSurface
        :return: None
        """
        pass

    def _draw_16(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 16
        :param tam_surface: TAMSurface
        :return: None
        """
        pass

    def _draw_256(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 256
        :param tam_surface: TAMSurface
        :return: None
        """
        pass

    def _draw_rgb(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode rgb
        :param tam_surface: TAMSurface
        :return: None
        """
        pass

    def _console_color_count(self):
        """
        info: Get console color
        :return: int
        """
        return 0


class NULLUtilitiesDriver(tam_drivers.UtilitiesDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("utilities_driver_operational", False)
        super().__init__(*args, **kwargs)

    def get_dimensions(self):
        """
        info: Gets the dimensions of console
        :return: (int, int): (row, column)
        """
        return 0, 0
