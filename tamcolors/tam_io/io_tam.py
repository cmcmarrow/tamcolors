from abc import ABC
import sys
from threading import Lock
from tamcolors.tam_io import tam_colors
from time import sleep

from tamcolors.utils import log


"""
IO
defines standards for all terminal IO
"""


MODE_2 = "2"
MODE_16_PAL_256 = "16_pal_256"
MODE_16 = "16"
MODE_256 = "256"
MODE_RGB = "rgb"


EVENT_START = 0
EVENT_DONE = 1
EVENT_DIMENSIONS = 2
EVENT_KEY_STATE_MODE = 3
EVENT_SET_MODE_2_COLOR = 4
EVENT_SET_MODE_16_PAL_256_COLOR = 5
EVENT_SET_MODE_16_COLOR = 6
EVENT_SET_MODE_256_COLOR = 7
EVENT_SET_ALL_COLORS = 8
EVENT_KEY = 9


class TAMSoundError(Exception):
    pass


class RawIO(ABC):
    def __str__(self):
        raise NotImplementedError()

    @classmethod
    def able_to_execute(cls):
        """
        info: checks that io is stable in current environment
        :return: bool
        """
        raise NotImplementedError()

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        raise NotImplementedError()

    def get_mode(self):
        """
        info: will return the current color mode
        :return: int
        """
        raise NotImplementedError()

    def get_modes(self):
        """
        info: will return a tuple of all color modes
        :return: (str, str, ...)
        """
        raise NotImplementedError()

    def draw(self, tam_surface):
        """
        info: Will draw TAMSurface to console
        :param tam_surface: TAMSurface
        :return: None
        """
        raise NotImplementedError()

    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        raise NotImplementedError()

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    def get_keyboard_name(self, default_to_us_english=True):
        """
        info: Will get the keyboard language name
        :param default_to_us_english: bool
        :return: str
        """
        raise NotImplementedError()

    def get_dimensions(self):
        """
        info: Gets the dimensions of console
        :return: (int, int): (row, column)
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    def color_change_driver_operational(self):
        """
        info: checks if the color changer driver is operational
        :return: bool
        """
        raise NotImplementedError()

    def color_driver_operational(self):
        """
        info: checks if the color driver is operational
        :return: bool
        """
        raise NotImplementedError()

    def key_driver_operational(self):
        """
        info: checks if the key driver is operational
        :return: bool
        """
        raise NotImplementedError()

    def sound_driver_operational(self):
        """
        info: checks if the sound driver is operational
        :return: bool
        """
        raise NotImplementedError()

    def get_key_dict(self, language=None):
        """
        info: Gets a dict of all the keys
        :param language: str or None
        :return: dict
        """
        raise NotImplementedError()

    def reset_colors_to_console_defaults(self):
        """
        info: will reset colors to console defaults
        :return: None
        """
        raise NotImplementedError()

    def set_tam_color_defaults(self):
        """
        info: will set console colors to tam defaults
        :return: None
        """
        raise NotImplementedError()

    def get_info_dict(self):
        """
        info: will get the identifier dict
        :return: dict
        """
        raise NotImplementedError()

    def color_changer_driver_operational(self):
        """
        info: checks if the color changer driver is operational
        :return: bool
        """
        raise NotImplementedError()

    def enable_console_keys(self, enable):
        """
        info: will enable console keys
        :param enable: boool
        :return: None
        """
        raise NotImplementedError()

    def enable_key_state_mode(self, enable=True):
        """
        info: Will enable or disable key state mode
        :param enable: bool
        :return: None
        """
        raise NotImplementedError()

    def is_key_state_mode_enabled(self):
        """
        info: Will get the status of key_state
        :return: bool
        """
        raise NotImplementedError()

    def get_color_2(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: RGBA
        """
        raise NotImplementedError()

    def get_color_16_pal_256(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: int
        """
        raise NotImplementedError()

    def get_color_16(self, spot):
        """
        info: Will get color from color palette 16
        :param spot: int
        :return: RGBA
        """
        raise NotImplementedError()

    def get_color_256(self, spot):
        """
        info: Will get color from color palette 256
        :param spot: int
        :return: RGBA
        """
        raise NotImplementedError()

    def get_printc_mode(self):
        """
        Gets the modes used by printc and inputc
        :return: str
        """
        raise NotImplementedError()

    def is_console_cursor_enabled(self):
        """
        info: will check if console cursor is enabled
        :return: bool
        """
        raise NotImplementedError()

    def is_console_keys_enabled(self):
        """
        info: will check if console keys enabled
        :return: bool
        """
        raise NotImplementedError()

    def set_color_2(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        raise NotImplementedError()

    def set_color_16_pal_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: int
        :return: None
        """
        raise NotImplementedError()

    def set_color_16(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        raise NotImplementedError()

    def set_color_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        raise NotImplementedError()

    def get_snapshot(self):
        """
        info: get snapshot of IO
        :return: dict
        """
        raise NotImplementedError()

    def apply_snapshot(self, snapshot):
        """
        info: apply snapshot state to IO
        :param snapshot: dict
        :return: None
        """
        raise NotImplementedError()

    def prime_event_bus(self):
        """
        info: will repeat the last event for every type other than keys
        :return: None
        """
        raise NotImplementedError()

    def enable_event_bus(self, bus=True):
        """
        info: will enable the event bus
        :param bus: bool
        :return: None
        """
        raise NotImplementedError()

    def is_event_bus_enabled(self):
        """
        info: will check if event bus is enabled
        :return: bool
        """
        raise NotImplementedError()

    def get_event(self):
        """
        info: will get event
        :yield: tuple
        """
        raise NotImplementedError()

    def open_sound(self, file, sound_id):
        """
        info: will open .wav sound
        :param file: str
        :param sound_id: int
        :return: None
        """
        raise NotImplementedError()

    def play_sound(self, sound_id, reset_sound=True):
        """
        info: will play sound
        :param sound_id: int
        :param reset_sound: bool
        :return: None
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    def get_sound_length(self, sound_id):
        """
        info: will get sound length
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

    def rest_sound(self, sound_id):
        """
        info: will reset sound
        :param sound_id: int
        :return: None
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


class IO(RawIO, ABC):
    def __init__(self,
                 identifier,
                 mode_2=True,
                 mode_16_pal_256=True,
                 mode_16=True,
                 mode_256=True,
                 mode_rgb=True,
                 key_driver_operational=True,
                 color_driver_operational=True,
                 color_changer_driver_operational=True,
                 utilities_driver_operational=True,
                 sound_driver_operational=True):
        """
        Makes a IO object
        :param identifier: TAMIdentifier
        :param mode_2: bool
        :param mode_16_pal_256: bool
        :param mode_16: bool
        :param mode_256: bool
        :param mode_rgb: bool
        :param color_changer_driver_operational: bool
        :param utilities_driver_operational: bool
        :param sound_driver_operational: bool
        """

        self._modes = []
        if mode_rgb:
            self._modes.append(MODE_RGB)
        if mode_256:
            self._modes.append(MODE_256)
        if mode_16:
            self._modes.append(MODE_16)
        if mode_16_pal_256:
            self._modes.append(MODE_16_PAL_256)
        if mode_2:
            self._modes.append(MODE_2)

        self._key_driver_operational = key_driver_operational
        self._color_driver_operational = color_driver_operational
        self._color_changer_driver_operational = color_changer_driver_operational
        self._utilities_driver_operational = utilities_driver_operational
        self._sound_driver_operational = sound_driver_operational

        self._is_console_cursor_enabled = True
        self._is_console_keys_enabled = False

        self._identifier = identifier
        self._modes = tuple(self._modes)

        self._color_palette_2 = [tam_colors.COLORS[spot].mode_rgb for spot in range(16)]
        self._color_palette_16_pal_256 = [spot for spot in range(16)]
        self._color_palette_16 = [tam_colors.COLORS[spot].mode_rgb for spot in range(16)]
        self._color_palette_256 = [tam_colors.COLORS[spot].mode_rgb for spot in range(256)]

        self._default_console_colors = []
        self._set_defaults()

        self._key_state_mode = False

        self._mode = None

        self._event_bus = False
        self._event_queue = []

        self._last_draw_dimensions = None

        self.set_mode(self._modes[-1])

        self._sound_lock_handler = Lock()
        self._active_sound_ids = set()

    def __new__(cls, *args, **kwargs):
        if cls.able_to_execute():
            return super(IO, cls).__new__(cls)

    def __str__(self):
        return str(self._identifier)

    @classmethod
    def able_to_execute(cls):
        """
        info: checks that io is stable in current environment
        :return: bool
        """
        return True

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return: None
        """
        self._mode = mode

        if mode == MODE_2:
            for spot, color in enumerate(self._color_palette_2):
                self.set_color_2(spot, color)
        if mode == MODE_16_PAL_256:
            for spot, color in enumerate(self._color_palette_16_pal_256):
                self.set_color_16_pal_256(spot, color)
        elif mode == MODE_16:
            for spot, color in enumerate(self._color_palette_16):
                self.set_color_16(spot, color)
        elif mode == MODE_256:
            for spot, color in enumerate(self._color_palette_256):
                self.set_color_256(spot, color)

    def get_mode(self):
        """
        info: will return the current color mode
        :return: int
        """
        return self._mode

    def get_modes(self):
        """
        info: will return a tuple of all color modes
        :return: (int, int, ...)
        """
        return self._modes

    def draw(self, tam_surface):
        """
        info: Will draw TAMSurface to console
        :param tam_surface: TAMSurface
        :return: None
        """
        if self._last_draw_dimensions != self.get_dimensions():
            self._last_draw_dimensions = self.get_dimensions()
            self._fire_dimensions_event()

        tam_surface.replace_alpha_chars()
        self._get_mode_draw()(tam_surface)

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

    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        self._fire_start_event()
        self.clear()
        self.show_console_cursor(False)
        self.enable_console_keys(True)

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        self._fire_done_event()
        self.clear()
        self.show_console_cursor(True)
        self.enable_console_keys(False)

    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
        """
        raise NotImplementedError()

    def wait_key(self, rest_time=0.0001, attempts=None):
        """
        info: Get an input from the terminal
        :param: rest_time: float: rest time from checking if a key is down
        :param: attempts: int or None: number of attempts to get a key
        :return: tuple or false
        """
        if attempts is None:
            while self.is_console_keys_enabled():
                key = self.get_key()
                if key is not False:
                    return key
                sleep(rest_time)
        else:
            for _ in range(attempts):
                if not self.is_console_keys_enabled():
                    break
                key = self.get_key()
                if key is not False:
                    return key
                sleep(rest_time)
        return False

    def enable_key_state_mode(self, enable=True):
        """
        info: Will enable or disable key state mode
        :param enable: bool
        :return: None
        """
        self._key_state_mode = enable
        self._fire_key_state_mode_event()

    def is_key_state_mode_enabled(self):
        """
        info: Will get the status of key_state
        :return: bool
        """
        return self._key_state_mode

    def get_keyboard_name(self, default_to_us_english=True):
        """
        info: Will get the keyboard language name
        :param default_to_us_english: bool
        :return: str
        """
        raise NotImplementedError()

    def get_dimensions(self):
        """
        info: Gets the dimensions of console
        :return: (int, int): (row, column)
        """
        raise NotImplementedError()

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

    def clear(self):
        """
        info: Will clear the console
        :return: None
        """
        # Most console will show cursor and disable keys on clear
        self.show_console_cursor(self.is_console_cursor_enabled())
        self.enable_console_keys(self.is_console_keys_enabled())

    def get_color_2(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: RGBA
        """
        return self._color_palette_2[spot]

    def get_color_16_pal_256(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: int
        """
        return self._color_palette_16_pal_256[spot]

    def get_color_16(self, spot):
        """
        info: Will get color from color palette 16
        :param spot: int
        :return: RGBA
        """
        return self._color_palette_16[spot]

    def get_color_256(self, spot):
        """
        info: Will get color from color palette 256
        :param spot: int
        :return: RGBA
        """
        return self._color_palette_256[spot]

    def show_console_cursor(self, show):
        """
        info: Will show or hide console cursor
        :param show: bool
        :return: None
        """
        self._is_console_cursor_enabled = show

    def utilities_driver_operational(self):
        """
        info: checks if the utilities driver is operational
        :return: bool
        """
        return self._utilities_driver_operational

    def color_changer_driver_operational(self):
        """
        info: checks if the color changer driver is operational
        :return: bool
        """
        return self._color_changer_driver_operational

    def sound_driver_operational(self):
        """
        info: checks if the sound driver is operational
        :return: bool
        """
        return self._sound_driver_operational

    def color_driver_operational(self):
        """
        info: checks if the color driver is operational
        :return: bool
        """
        return self._color_driver_operational

    def key_driver_operational(self):
        """
        info: checks if the key driver is operational
        :return: bool
        """
        return self._key_driver_operational

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

    def get_key_dict(self, language=None):
        """
        info: Gets a dict of all the keys
        :param language: str or None
        :return: dict
        """
        raise NotImplementedError()

    def set_color_2(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        if self._console_color_count() > spot and self.get_mode() == MODE_2:
            self._set_console_color(spot, color)
        self._color_palette_2[spot] = color
        self._fire_color_set_event(EVENT_SET_MODE_2_COLOR, spot, self.get_color_2(spot))

    def set_color_16_pal_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: int
        :return: None
        """
        if self._console_color_count() > spot and self.get_mode() == MODE_16_PAL_256:
            self._set_console_color(spot, tam_colors.COLORS[color].mode_rgb)
        self._color_palette_16_pal_256[spot] = color
        self._fire_color_set_event(EVENT_SET_MODE_16_PAL_256_COLOR, spot, self.get_color_16_pal_256(spot))

    def set_color_16(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        if self._console_color_count() > spot and self.get_mode() == MODE_16:
            self._set_console_color(spot, color)
        self._color_palette_16[spot] = color
        self._fire_color_set_event(EVENT_SET_MODE_16_COLOR, spot, self.get_color_16(spot))

    def set_color_256(self, spot, color):
        """
        info: sets a color value
        :param spot: int
        :param color: RGBA
        :return: None
        """
        if self._console_color_count() > spot and self.get_mode() == MODE_256:
            self._set_console_color(spot, color)
        self._color_palette_256[spot] = color
        self._fire_color_set_event(EVENT_SET_MODE_256_COLOR, spot, self.get_color_256(spot))

    def reset_colors_to_console_defaults(self):
        """
        info: will reset colors to console defaults
        :return: None
        """
        # reset colors to console defaults
        for spot, color in enumerate(self._default_console_colors):
            if spot < 16:
                self.set_color_16_pal_256(spot, spot)
                self.set_color_2(spot, color)
                self.set_color_16(spot, color)
            if spot < 256:
                self.set_color_256(spot, color)
            self._set_console_color(spot, color)

        # reset of the colors
        for spot in range(self._console_color_count(), 256):
            if spot < 16:
                self.set_color_2(spot, tam_colors.COLORS[spot].mode_rgb)
                self.set_color_16_pal_256(spot, spot)
                self.set_color_16(spot, tam_colors.COLORS[spot].mode_rgb)
            if spot < 256:
                self.set_color_256(spot, tam_colors.COLORS[spot].mode_rgb)

    def set_tam_color_defaults(self):
        """
        info: will set console colors to tam defaults
        :return: None
        """
        for spot, color in enumerate(tam_colors.COLORS):
            if spot < 16:
                self.set_color_2(spot, color.mode_rgb)
                self.set_color_16_pal_256(spot, spot)
                self.set_color_16(spot, color.mode_rgb)
            if spot < 256:
                self.set_color_256(spot, color.mode_rgb)

            if self._console_color_count() > spot:
                self._set_console_color(spot, color.mode_rgb)

    def get_info_dict(self):
        """
        info: will get the identifier dict
        :return: dict
        """
        return self._identifier.get_info_dict()

    def _set_defaults(self):
        """
        info: will save console defaults
        :return: None
        """
        self._default_console_colors = []
        for spot in range(self._console_color_count()):
            color = self._get_console_color(spot)
            self._default_console_colors.append(color)
            if spot < 16:
                self._color_palette_2[spot] = color
                self._color_palette_16[spot] = color
            if spot < 256:
                self._color_palette_256[spot] = color

    def is_console_cursor_enabled(self):
        """
        info: will check if console cursor is enabled
        :return: bool
        """
        return self._is_console_cursor_enabled

    def enable_console_keys(self, enable):
        """
        info: will enable console keys
        :param enable: boool
        :return: None
        """
        self._is_console_keys_enabled = enable

    def is_console_keys_enabled(self):
        """
        info: will check if console keys enabled
        :return: bool
        """
        return self._is_console_keys_enabled

    def get_snapshot(self):
        """
        info: get snapshot of IO
        :return: dict
        """
        mode_2 = [self.get_color_2(color) for color in range(2)]
        mode_16_pal_256 = [self.get_color_16_pal_256(color) for color in range(16)]
        mode_16 = [self.get_color_16(color) for color in range(16)]
        mode_256 = [self.get_color_256(color) for color in range(256)]

        snapshot = {"console_cursor": self.is_console_cursor_enabled(),
                    "console_keys": self.is_console_keys_enabled(),
                    "key_state_mode": self.is_key_state_mode_enabled(),
                    "mode_2": mode_2,
                    "mode_16_pal_256": mode_16_pal_256,
                    "mode_16": mode_16,
                    "mode_256": mode_256}

        return snapshot

    def apply_snapshot(self, snapshot):
        """
        info: apply snapshot state to IO
        :param snapshot: dict
        :return: None
        """
        if "console_cursor" in snapshot:
            self.show_console_cursor(snapshot["console_cursor"])

        if "console_keys" in snapshot:
            self.enable_console_keys(snapshot["console_keys"])

        if "key_state_mode" in snapshot:
            self.enable_key_state_mode(snapshot["key_state_mode"])

        if "mode_2" in snapshot:
            for spot, color in enumerate(snapshot["mode_2"]):
                self.set_color_2(spot, color)

        if "mode_16_pal_256" in snapshot:
            for spot, color in enumerate(snapshot["mode_16_pal_256"]):
                self.set_color_16_pal_256(spot, color)

        if "mode_16" in snapshot:
            for spot, color in enumerate(snapshot["mode_16"]):
                self.set_color_16(spot, color)

        if "mode_256" in snapshot:
            for spot, color in enumerate(snapshot["mode_256"]):
                self.set_color_256(spot, color)

    def _get_mode_draw(self):
        """
        info: will get the current draw mode function
        :return: func
        """
        return getattr(self, "_draw_{}".format(self._mode))

    @staticmethod
    def _draw_onto(tam_surface, tam_surface2):
        """
        info: will draw tam_surface2 in the center of tam_surface
        :param tam_surface: TAMSurface
        :param tam_surface2: TAMSurface
        :return:
        """
        surface_size_x, surface_size_y = tam_surface.get_dimensions()
        width, height = tam_surface2.get_dimensions()
        start_x = (surface_size_x // 2) - (width // 2)
        start_y = (surface_size_y // 2) - (height // 2)
        tam_surface.draw_onto(tam_surface2, max(start_x, 0), max(start_y, 0))

    @staticmethod
    def _write_to_output_stream(output, flush, stderr):
        """
        info: will write to the right stream
        :param stderr: bool
        :return: stdout or stderr
        """
        file = sys.stdout
        if stderr:
            file = sys.stderr

        file.write(output)

        if flush:
            file.flush()

    def prime_event_bus(self):
        """
        info: will repeat the last event for every type other than keys
        :return: None
        """
        if self.is_event_bus_enabled():
            self._fire_dimensions_event()
            self._fire_key_state_mode_event()
            self._fire_set_all_color_event()

    def enable_event_bus(self, bus=True):
        """
        info: will enable the event bus
        :param bus: bool
        :return: None
        """
        self._event_bus = bus

    def is_event_bus_enabled(self):
        """
        info: will check if event bus is enabled
        :return: bool
        """
        return self._event_bus

    def get_event(self):
        """
        info: will get event
        :yield: tuple
        """
        check_key = False
        while self.is_event_bus_enabled():
            if self._event_queue and not check_key:
                check_key = True
                yield self._event_queue.pop(0)
            else:
                check_key = False
                key = self.get_key()
                if key is not False:
                    yield EVENT_KEY, key
                else:
                    yield None

    def _fire_event(self, event_type, data=None):
        if len(self._event_queue) <= 1000:
            self._event_queue.append((event_type, data))
        else:
            log.warning("Lost Event : ({}, {})".format(event_type, data))

    def _fire_start_event(self):
        self._fire_event(EVENT_START)

    def _fire_done_event(self):
        self._fire_event(EVENT_DONE)

    def _fire_dimensions_event(self):
        self._fire_event(EVENT_DIMENSIONS, self.get_dimensions())

    def _fire_color_set_event(self, mode, spot, color):
        self._fire_event(mode, (spot, color))

    def _fire_key_state_mode_event(self):
        self._fire_event(EVENT_KEY_STATE_MODE, self.is_key_state_mode_enabled())

    def _fire_set_all_color_event(self):
        self._fire_event(EVENT_SET_ALL_COLORS, {EVENT_SET_MODE_2_COLOR: self._color_palette_2,
                                                EVENT_SET_MODE_16_PAL_256_COLOR: self._color_palette_16_pal_256,
                                                EVENT_SET_MODE_16_COLOR: self._color_palette_16,
                                                EVENT_SET_MODE_256_COLOR: self._color_palette_256})

    def open_sound(self, file, sound_id):
        """
        info: will open .wav sound
        :param file: str
        :param sound_id: int
        :return: None
        """
        if sound_id in self._active_sound_ids:
            log.critical("Sound ID \"{}\" all ready in use!".format(sound_id))
            raise TAMSoundError("Sound ID \"{}\" all ready in use!".format(sound_id))

        if not file.lower().endswith(".wav"):
            raise TAMSoundError("File \"{0}\" must end with \".wav\"".format(file))
        self._active_sound_ids.add(sound_id)

    def play_sound(self, sound_id, reset_sound=True):
        """
        info: will play sound
        :param sound_id: int
        :param reset_sound: bool
        :return: None
        """
        if reset_sound:
            self.rest_sound(sound_id)

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
        if sound_id in self._active_sound_ids:
            self._active_sound_ids.remove(sound_id)
        else:
            log.warning("Sound ID \"{}\" all ready closed".format(sound_id))

    def get_sound_length(self, sound_id):
        """
        info: will get sound length
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

    def rest_sound(self, sound_id):
        """
        info: will reset sound
        :param sound_id: int
        :return: None
        """
        if self.is_sound_playing(sound_id):
            self.pause_sound(sound_id)
        self.set_sound_position(sound_id, 0)

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

    def _sound_lock(self):
        """
        info: will lock sound thread lock
        :return: None
        """
        self._sound_lock_handler.acquire()

    def _sound_lock_release(self):
        """
        info: will release the sound thread lock
        :return: None
        """
        self._sound_lock_handler.release()
