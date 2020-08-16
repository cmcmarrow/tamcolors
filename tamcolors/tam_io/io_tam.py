from abc import ABC
import sys


"""
IO
defines standards for all terminal IO
"""

IO_DEFAULT_COLORS = {0: (12, 12, 12),
                     1: (0, 55, 218),
                     2: (19, 161, 14),
                     3: (58, 150, 221),
                     4: (197, 15, 31),
                     5: (136, 23, 152),
                     6: (193, 156, 0),
                     7: (204, 204, 204),
                     8: (118, 118, 118),
                     9: (59, 120, 255),
                     10: (22, 198, 12),
                     11: (97, 214, 214),
                     12: (231, 72, 86),
                     13: (180, 0, 158),
                     14: (249, 241, 165),
                     15: (242, 242, 242)}


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
        self._colors = IO_DEFAULT_COLORS.copy()
        self._default_colors = self._colors.copy()
        self._set_defaults()

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
        self._colors[spot] = color

    def reset_colors_to_console_defaults(self):
        """
        info: will reset colors to consoloe defaults
        :return: None
        """
        for spot in self._default_colors:
            self.set_color(spot, self._default_colors[spot])

    def set_tam_color_defaults(self):
        """
        info: will set console colors to tam defaults
        :return: None
        """
        for spot in IO_DEFAULT_COLORS:
            self.set_color(spot, IO_DEFAULT_COLORS[spot])

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
