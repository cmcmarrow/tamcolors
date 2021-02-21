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

    def wait_key(self, rest_time=0.0001, attempts=300000):
        """
        info: Get an input from the terminal
        :param: rest_time: float: rest time from checking if a key is down
        :param: attempts: int: number of attempts to get a key
        :return: tuple or false
        """
        return super().wait_key(rest_time)

    def get_key_dict(self, language=None):
        """
        info: Gets a dict of all the keys
        :param language: str or None
        :return: dict
        """
        raise NotImplementedError()

    def enable_console_keys(self, enable):
        super().enable_console_keys(enable)

    def get_keyboard_name(self, default_to_us_english=True):
        """
        info: Will get the keyboard language name
        :param default_to_us_english: bool
        :return: str
        """
        raise NotImplementedError()


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

    def draw(self, tam_surface):
        """
        info: Will draw TAMSurface to console
        :param tam_surface: TAMSurface
        :return: None
        """
        super().draw(tam_surface)

    def _draw_2(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 2
        :param tam_surface: TAMSurface
        :return: None
        """
        raise NotImplementedError()

    def _draw_16_pal_256(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 16_pal_256
        :param tam_surface: TAMSurface
        :return: None
        """
        raise NotImplementedError()

    def _draw_16(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 16
        :param tam_surface: TAMSurface
        :return: None
        """
        raise NotImplementedError()

    def _draw_256(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 256
        :param tam_surface: TAMSurface
        :return: None
        """
        raise NotImplementedError()

    def _draw_rgb(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode rgb
        :param tam_surface: TAMSurface
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

    def get_color_16_pal_256(self, spot):
        """
        info: Will get color from color palette 16
        :param spot: int
        :return: int
        """
        return super().get_color_16_pal_256(spot)

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

    def set_color_16_pal_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: int
        :return: None
        """
        super().set_color_16_pal_256(spot, color)

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


class SoundDriver(TAMDriver, ABC):
    def open_sound(self, file, sound_id):
        """
        info: will open .wav sound
        :param file: str
        :param sound_id: int
        :return: None
        """
        super(SoundDriver, self).open_sound(file, sound_id)

    def play_sound(self, sound_id, reset_sound=True):
        """
        info: will play sound
        :param sound_id: int
        :param reset_sound: bool
        :return: None
        """
        super(SoundDriver, self).play_sound(sound_id, reset_sound)

    def pause_sound(self, sound_id):
        """
        info: will pause sound
        :param sound_id: int
        :return: None
        """
        raise NotImplementedError()

    def close_sound(self, sound_id):
        """
        info: will close sound
        :param sound_id: int
        :return: None
        """
        super(SoundDriver, self).close_sound(sound_id)

    def get_sound_length(self, sound_id):
        """
        info: will get sound lenght
        :param sound_id: int
        :return: int
        """
        raise NotImplementedError()

    def is_sound_playing(self, sound_id):
        """
        info: will check if sound is playing
        :param sound_id: int
        :return: bool
        """
        raise NotImplementedError()

    def get_sound_position(self, sound_id):
        """
        info: will get the time spot of the song
        :param sound_id: int
        :return: int
        """
        raise NotImplementedError()

    def set_sound_position(self, sound_id, spot):
        """
        info: will set the spot of the sound
        :param sound_id: int
        :param spot: int
        :return: None
        """
        raise NotImplementedError()

