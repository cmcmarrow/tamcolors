# built in library
import copy

from tamcolors.tam_io.tam_colors import Color
from tamcolors.utils import object_packer


"""
TAMBuffer
stores char and colors for spot
can get/set spots
can clear
can format to be outputted
"""


ALPHA_CHAR = "\u0000"


class TAMBuffer(object_packer.FastHandObjectPacker):
    def __init__(self,
                 width,
                 height,
                 char,
                 foreground_color,
                 background_color):
        """
        info: makes a TAMBuffer object
        :param width: int: 0 - inf
        :param height: int: 0 - inf
        :param char: str: len of 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        """

        # save data
        self._width = width
        self._height = height
        self._char = char
        self._foreground_color = foreground_color
        self._background_color = background_color

        # setup buffers
        length = width * height
        self._char_buffer = [char] * length
        self._foreground_buffer = [foreground_color] * length
        self._background_buffer = [background_color] * length

    def __str__(self):
        """
        info: formats TAMBuffer to string to be printed
        :return: str: TAMBuffer as string
        """
        rows = []
        for y in range(self._height):
            row = []
            for spot in range(y * self._width, (y + 1) * self._width):
                spot_char = self._char_buffer[spot]
                if spot_char == ALPHA_CHAR:
                    if self._char == ALPHA_CHAR:
                        row.append(" ")
                    else:
                        row.append(self._char)
                else:
                    row.append(spot_char)
            rows.append("".join(row))

        return "\n".join(rows)

    def __len__(self):
        """
        info: gets the number of spot in the buffer
        :return:
        """
        return len(self._char_buffer)

    def __eq__(self, other):
        """
        info: self == other
        :param other: Object
        :return: bool
        """
        if isinstance(other, TAMBuffer):
            return self.get_raw_buffers() == other.get_raw_buffers()
        return False

    def __ne__(self, other):
        """
        info: self != other
        :param other: Object
        :return: bool
        """
        return not self.__eq__(other)

    def to_bytes(self):
        tam_buffer_bytes = bytearray()
        tam_buffer_bytes.extend(object_packer.save_int(self._width))
        tam_buffer_bytes.extend(object_packer.save_int(self._height))
        tam_buffer_bytes.extend(object_packer.save_data(bytes(self._char, encoding="utf-8")))
        tam_buffer_bytes.extend(self._foreground_color.to_bytes())
        tam_buffer_bytes.extend(self._background_color.to_bytes())
        tam_buffer_bytes.extend(object_packer.save_data(bytes("".join(self._char_buffer), encoding="utf-8")))

        for color in self._foreground_buffer:
            tam_buffer_bytes += color.to_bytes()

        for color in self._background_buffer:
            tam_buffer_bytes += color.to_bytes()

        return bytes(tam_buffer_bytes)

    @classmethod
    def from_bytes(cls, object_byte_array):
        buffer = cls.__new__(cls)
        buffer._width = object_packer.load_int(object_byte_array)
        buffer._height = object_packer.load_int(object_byte_array)
        buffer._char = str(object_packer.load_data(object_byte_array), encoding="utf-8")
        buffer._foreground_color = Color.from_bytes(object_byte_array)
        buffer._background_color = Color.from_bytes(object_byte_array)
        buffer._char_buffer = list(str(object_packer.load_data(object_byte_array), encoding="utf-8"))
        buffer._foreground_buffer = [Color.from_bytes(object_byte_array) for _ in range(buffer._width*buffer._height)]
        buffer._background_buffer = [Color.from_bytes(object_byte_array) for _ in range(buffer._width*buffer._height)]
        return buffer

    def clear(self):
        """
        info: clears TAMBuffer
        :return:
        """
        length = self._width * self._height
        self._char_buffer = [self._char] * length
        self._foreground_buffer = [self._foreground_color] * length
        self._background_buffer = [self._background_color] * length

    def get_dimensions(self):
        """
        info: gets buffer dimensions
        :return: (int, int)
        """
        return self._width, self._height

    def set_dimensions_and_clear(self, width, height):
        """
        info: clears and resizes TAMBuffer
        :param width: int: 0 - inf
        :param height: int: 0 - inf
        :return:
        """
        self._width = width
        self._height = height

        length = width * height
        self._char_buffer = [self._char] * length
        self._foreground_buffer = [self._foreground_color] * length
        self._background_buffer = [self._background_color] * length

    def get_defaults(self):
        """
        info: gets defaults
        :return: (str, int, int)
        """
        return self._char, self._foreground_color, self._background_color

    def set_defaults_and_clear(self, char, foreground_color, background_color):
        """
        info: clears buffer and resets defaults
        :param char: str: len of 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        :return:
        """
        self._char = char
        self._foreground_color = foreground_color
        self._background_color = background_color

        length = self._width * self._height
        self._char_buffer = [self._char] * length
        self._foreground_buffer = [self._foreground_color] * length
        self._background_buffer = [self._background_color] * length

    def get_raw_buffers(self):
        """
        info: gets raw buffers
        :return: (list, list, list)
        """
        return self._char_buffer, self._foreground_buffer, self._background_buffer

    def copy(self):
        """
        info: copy's TAMBuffer
        :return: TAMBuffer
        """
        return copy.deepcopy(self)

    def get_raw_spot(self, x, y):
        """
        info: return -1 if not a spot
        :param x: int
        :param y: int
        :return: int
        """
        if x < 0 or x >= self._width:
            return -1
        if y < 0 or y >= self._height:
            return -1
        return x + y * self._width

    def set_spot(self, x, y, char, foreground_color, background_color, override_alpha=False):
        """
        info: sets a single spot on the buffer
        :param x: int
        :param y: int
        :param char: str: len of 1
        :param foreground_color: int
        :param background_color: int
        :param override_alpha: bool
        :return:
        """

        spot = self.get_raw_spot(x, y)
        if spot != -1:
            if override_alpha or not char == ALPHA_CHAR:
                self._char_buffer[spot] = char
            if foreground_color.has_alpha:
                self._foreground_buffer[spot] = foreground_color.place_color_over(self._foreground_buffer[spot],
                                                                                  override_alpha)
            else:
                self._foreground_buffer[spot] = foreground_color
            if background_color.has_alpha:
                self._background_buffer[spot] = background_color.place_color_over(self._background_buffer[spot],
                                                                                  override_alpha)
            else:
                self._background_buffer[spot] = background_color

    def get_spot(self, x, y):
        """
        info: gets spot info
        :param x: int
        :param y: int
        :return: (int, int, int) or None
        """

        spot = self.get_raw_spot(x, y)
        if spot != -1:
            return self._char_buffer[spot], self._foreground_buffer[spot], self._background_buffer[spot]
        return None

    def get_from_raw_spot(self, spot):
        """
        info: gets spot info
        :param spot: x: int: 0 - (len(tam_buffer) - 1)
        :return: (int, int, int) or None
        """
        if 0 <= spot < len(self._char_buffer):
            return self._char_buffer[spot], self._foreground_buffer[spot], self._background_buffer[spot]
        return None

    def draw_onto(self,
                  tam_buffer,
                  start_x=0,
                  start_y=0,
                  buffer_start_x=0,
                  buffer_start_y=0,
                  buffer_size_x=-1,
                  buffer_size_y=-1,
                  override_alpha=False):
        """
        info: will draw tam_buffer or part of a TAMBuffer onto another TAMBuffer
        :param tam_buffer: TAMBuffer
        :param start_x: int
        :param start_y: int
        :param buffer_start_x: int
        :param buffer_start_y: int
        :param buffer_size_x: int: 0 - inf
        :param buffer_size_y: int: 0 - inf
        :param override_alpha: bool
        :return:
        """

        start_x, \
        start_y, \
        buffer_start_x, \
        buffer_start_y, \
        buffer_size_x, \
        buffer_size_y = self.get_cross_rect(tam_buffer,
                                            start_x,
                                            start_y,
                                            buffer_start_x,
                                            buffer_start_y,
                                            buffer_size_x,
                                            buffer_size_y)

        char_buffer, foreground_buffer, background_buffer = tam_buffer.get_raw_buffers()
        this_char_buffer, this_foreground_buffer, this_background_buffer = self.get_raw_buffers()
        for y in range(buffer_size_y):
            to_spot = self.get_raw_spot(start_x, start_y + y)
            draw_spot = tam_buffer.get_raw_spot(buffer_start_x, buffer_start_y + y)
            for ts, ds in zip(range(to_spot, to_spot + buffer_size_x), range(draw_spot, draw_spot + buffer_size_x)):
                if override_alpha or not isinstance(char_buffer[ds], TAMBuffer):
                    this_char_buffer[ts] = char_buffer[ds]
                if foreground_buffer[ds].has_alpha:
                    this_foreground_buffer[ts] = foreground_buffer[ds].place_color_over(this_foreground_buffer[ts],
                                                                                        override_alpha)
                else:
                    this_foreground_buffer[ts] = foreground_buffer[ds]
                if background_buffer[ds].has_alpha:
                    this_background_buffer[ts] = background_buffer[ds].place_color_over(this_background_buffer[ts],
                                                                                        override_alpha)
                else:
                    this_background_buffer[ts] = background_buffer[ds]

    def get_cross_rect(self,
                       tam_buffer,
                       start_x=0,
                       start_y=0,
                       buffer_start_x=0,
                       buffer_start_y=0,
                       buffer_size_x=-1,
                       buffer_size_y=-1):
        """
        info: will draw tam_buffer or part of a TAMBuffer onto another TAMBuffer
        :param tam_buffer: TAMBuffer
        :param start_x: int
        :param start_y: int
        :param buffer_start_x: int
        :param buffer_start_y: int
        :param buffer_size_x: int: 0 - inf
        :param buffer_size_y: int: 0 - inf
        :return:
        """
        width, height = tam_buffer.get_dimensions()
        if buffer_size_x == -1:
            buffer_size_x = width
        if buffer_size_y == -1:
            buffer_size_y = height

        if start_x < 0:
            buffer_start_x += abs(start_x)
            buffer_size_x = max(buffer_size_x + start_x, 0)
            start_x = 0

        if start_y < 0:
            buffer_start_y += abs(start_y)
            buffer_size_y = max(buffer_size_y + start_y, 0)
            start_y = 0

        if buffer_start_x < 0:
            start_x += abs(buffer_start_x)
            buffer_size_x = max(buffer_size_x + buffer_start_x, 0)
            buffer_start_x = 0

        if buffer_start_y < 0:
            start_y += abs(buffer_start_y)
            buffer_size_y = max(buffer_size_y + buffer_start_y, 0)
            buffer_start_y = 0

        buffer_size_x = max(min(buffer_size_x, width - buffer_start_x, self._width - start_x), 0)
        buffer_size_y = max(min(buffer_size_y, height - buffer_start_y, self._height - start_y), 0)

        return start_x, start_y, buffer_start_x, buffer_start_y, buffer_size_x, buffer_size_y

    def replace_alpha_chars(self, alpha_replacement=None):
        """
        :param alpha_replacement: None or str
        :return:
        """
        if alpha_replacement is None:
            alpha_replacement = self._char

        if alpha_replacement == ALPHA_CHAR:
            alpha_replacement = " "

        for spot, char in enumerate(self._char_buffer):
            if char == ALPHA_CHAR:
                self._char_buffer[spot] = alpha_replacement
