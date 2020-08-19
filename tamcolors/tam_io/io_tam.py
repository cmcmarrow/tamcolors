from abc import ABC
import sys
from tamcolors.tam_io import tam_colors


"""
IO
defines standards for all terminal IO
"""


class IO(ABC):
    def __init__(self, identifier, mode_2=True, mode_16=True):
        """
        Makes a IO object
        :param mode_2: bool
        :param mode_16: bool
        """
        self._modes = []
        if mode_2:
            self._modes.append(2)
        if mode_16:
            self._modes.append(16)

        if 16 in self._modes:
            self._mode = 16
        else:
            self._mode = self._modes[0]

        self._identifier = identifier
        self._modes = tuple(self._modes)
        self._color_palette = [color.mode_rgb for color in tam_colors.COLOR_LIST]
        self._default_colors = self._color_palette.copy()
        self._set_defaults()

    def __str__(self):
        return str(self._identifier)

    @classmethod
    def able_to_execute(cls):
        raise NotImplementedError()

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        self._mode = mode

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
        tam_buffer.replace_alpha_chars()
        self._get_mode_draw()(tam_buffer)

    def _draw_2(self, tam_buffer):
        raise NotImplementedError()

    def _draw_16(self, tam_buffer):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def done(self):
        raise NotImplementedError()

    def get_key(self):
        raise NotImplementedError()

    def get_dimensions(self):
        raise NotImplementedError()

    def printc(self, value, color, flush, stderr):
        raise NotImplementedError()

    def inputc(self, output, color):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def get_color(self, spot):
        raise NotImplementedError()

    def show_console_cursor(self, show):
        raise NotImplementedError()

    def utilities_driver_operational(self):
        raise NotImplementedError()

    def color_change_driver_operational(self):
        return NotImplementedError()

    def color_driver_operational(self):
        return NotImplementedError()

    def key_driver_operational(self):
        return NotImplementedError()

    @staticmethod
    def get_key_dict():
        raise NotImplementedError()

    def set_color(self, spot, color):
        """
        info: sets a color value
        :param spot: int: 0 - 15
        :param color: tuple: (int, int, int)
        :return: None
        """
        self._color_palette[spot] = color

    def reset_colors_to_console_defaults(self):
        """
        info: will reset colors to consoloe defaults
        :return: None
        """
        for spot, color in enumerate(self._default_colors):
            self.set_color(spot, color)

    def set_tam_color_defaults(self):
        """
        info: will set console colors to tam defaults
        :return: None
        """
        for spot, color in enumerate(tam_colors.COLOR_LIST):
            self.set_color(spot, color.mode_rgb)

    def get_info_dict(self):
        return self._identifier.get_info_dict()

    def _set_defaults(self):
        """
        info: will save console defaults
        :return: None
        """
        for spot in range(16):
            self._default_colors[spot] = self.get_color(spot)

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
