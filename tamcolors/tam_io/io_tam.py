from abc import ABC
import sys
from tamcolors.tam_io import tam_colors


"""
IO
defines standards for all terminal IO
"""


MODE_2 = "2"
MODE_16 = "16"
MODE_256 = "256"
MODE_RGB = "rgb"


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
        :return: (int, int, ...)
        """
        raise NotImplementedError()

    def draw(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console
        :param tam_buffer: TAMBuffer
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

    @staticmethod
    def get_key_dict():
        """
        info: Gets a dict of all the keys
        :return: {str: (str, str), ...}
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

    def get_color_2(self, spot):
        """
        info: Will get color from color palette 2
        :param spot: int
        :return: RGBA
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


class IO(RawIO, ABC):
    def __init__(self,
                 identifier,
                 mode_2=True,
                 mode_16=True,
                 mode_256=True,
                 mode_rgb=True,
                 key_driver_operational=True,
                 color_driver_operational=True,
                 color_changer_driver_operational=True,
                 utilities_driver_operational=True):
        """
        Makes a IO object
        :param identifier: TAMIdentifier
        :param mode_2: bool
        :param mode_16: bool
        :param mode_256: bool
        :param mode_rgb: bool
        :param color_changer_driver_operational: bool
        :param utilities_driver_operational: bool
        """

        self._modes = []
        if mode_2:
            self._modes.append(MODE_2)
        if mode_16:
            self._modes.append(MODE_16)
        if mode_256:
            self._modes.append(MODE_256)
        if mode_rgb:
            self._modes.append(MODE_RGB)

        self._key_driver_operational = key_driver_operational
        self._color_driver_operational = color_driver_operational
        self._color_changer_driver_operational = color_changer_driver_operational
        self._utilities_driver_operational = utilities_driver_operational

        self._is_console_cursor_enabled = True
        self._is_console_keys_enabled = False

        self._identifier = identifier
        self._modes = tuple(self._modes)

        self._color_palette_2 = [tam_colors.COLORS[spot].mode_rgb for spot in range(16)]
        self._color_palette_16 = [tam_colors.COLORS[spot].mode_rgb for spot in range(16)]
        self._color_palette_256 = [tam_colors.COLORS[spot].mode_rgb for spot in range(256)]

        self._default_console_colors = []
        self._set_defaults()

        self._mode = None
        self.set_mode(self._modes[-1])

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
        :return:
        """
        self._mode = mode

        if mode == MODE_2:
            for spot, color in enumerate(self._color_palette_2):
                self.set_color_2(spot, color)
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

    def draw(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console
        :param tam_buffer: TAMBuffer
        :return: None
        """
        tam_buffer.replace_alpha_chars()
        self._get_mode_draw()(tam_buffer)

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

    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        self.clear()
        self.show_console_cursor(False)
        self.enable_console_keys(True)

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        self.clear()
        self.show_console_cursor(True)
        self.enable_console_keys(False)

    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
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

    @staticmethod
    def get_key_dict():
        """
        info: Gets a dict of all the keys
        :return: {str: (str, str), ...}
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

    def reset_colors_to_console_defaults(self):
        """
        info: will reset colors to console defaults
        :return: None
        """
        for spot, color in enumerate(self._default_console_colors):
            if spot < 16:
                self.set_color_2(spot, color)
                self.set_color_16(spot, color)
            if spot < 256:
                self.set_color_256(spot, color)
            self._set_console_color(spot, color)

        for spot in range(self._console_color_count(), 256):
            if spot < 16:
                self.set_color_2(spot, tam_colors.COLORS[spot].mode_rgb)
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

    def _get_mode_draw(self):
        """
        info: will get the current draw mode function
        :return: func
        """
        return getattr(self, "_draw_{}".format(self._mode))

    @staticmethod
    def _draw_onto(tam_buffer, tam_buffer2):
        """
        info: will draw tam_buffer2 in the center of tam_buffer
        :param tam_buffer: TAMBuffer
        :param tam_buffer2: TAMBuffer
        :return:
        """
        buffer_size_x, buffer_size_y = tam_buffer.get_dimensions()
        width, height = tam_buffer2.get_dimensions()
        start_x = (buffer_size_x // 2) - (width // 2)
        start_y = (buffer_size_y // 2) - (height // 2)
        tam_buffer.draw_onto(tam_buffer2, max(start_x, 0), max(start_y, 0))

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
