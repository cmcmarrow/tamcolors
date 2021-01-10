# built in library
import copy

from tamcolors.tam_io.tam_colors import Color
from tamcolors.utils import object_packer


"""
TAMSurface
stores char and colors for spot
can get/set spots
can clear
can format to be outputted
"""


ALPHA_CHAR = "\u0000"


class TAMSurface(object_packer.FastHandObjectPacker):
    def __init__(self,
                 width,
                 height,
                 char,
                 foreground_color,
                 background_color):
        """
        info: makes a TAMSurface object
        :param width: int: 0 - inf
        :param height: int: 0 - inf
        :param char: str: len of 1
        :param foreground_color: Color
        :param background_color: Color
        """

        # save data
        self._width = width
        self._height = height
        self._char = char
        self._foreground_color = foreground_color
        self._background_color = background_color

        # setup surface
        length = width * height
        self._char_surface = [char] * length
        self._foreground_surface = [foreground_color] * length
        self._background_surface = [background_color] * length

    def __str__(self):
        """
        info: formats TAMSurface to string to be printed
        :return: str: TAMSurface as string
        """
        rows = []
        for y in range(self._height):
            row = []
            for spot in range(y * self._width, (y + 1) * self._width):
                spot_char = self._char_surface[spot]
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
        info: gets the number of spot in the surface
        :return:
        """
        return len(self._char_surface)

    def __eq__(self, other):
        """
        info: self == other
        :param other: Object
        :return: bool
        """
        if isinstance(other, TAMSurface):
            return self.get_raw_surface() == other.get_raw_surface()
        return False

    def __ne__(self, other):
        """
        info: self != other
        :param other: Object
        :return: bool
        """
        return not self.__eq__(other)

    def to_bytes(self):
        tam_surface_bytes = bytearray()
        tam_surface_bytes.extend(object_packer.save_int(self._width))
        tam_surface_bytes.extend(object_packer.save_int(self._height))
        tam_surface_bytes.extend(object_packer.save_data(bytes(self._char, encoding="utf-8")))
        tam_surface_bytes.extend(self._foreground_color.to_bytes())
        tam_surface_bytes.extend(self._background_color.to_bytes())
        tam_surface_bytes.extend(object_packer.save_data(bytes("".join(self._char_surface), encoding="utf-8")))

        for color in self._foreground_surface:
            tam_surface_bytes += color.to_bytes()

        for color in self._background_surface:
            tam_surface_bytes += color.to_bytes()

        return bytes(tam_surface_bytes)

    @classmethod
    def from_bytes(cls, object_byte_array):
        surface = cls.__new__(cls)
        surface._width = object_packer.load_int(object_byte_array)
        surface._height = object_packer.load_int(object_byte_array)
        surface._char = str(object_packer.load_data(object_byte_array), encoding="utf-8")
        surface._foreground_color = Color.from_bytes(object_byte_array)
        surface._background_color = Color.from_bytes(object_byte_array)
        surface._char_surface = list(str(object_packer.load_data(object_byte_array), encoding="utf-8"))
        surface._foreground_surface = [Color.from_bytes(object_byte_array) for _ in range(surface._width * surface._height)]
        surface._background_surface = [Color.from_bytes(object_byte_array) for _ in range(surface._width * surface._height)]
        return surface

    def clear(self):
        """
        info: clears TAMSurface
        :return:
        """
        length = self._width * self._height
        self._char_surface = [self._char] * length
        self._foreground_surface = [self._foreground_color] * length
        self._background_surface = [self._background_color] * length

    def get_dimensions(self):
        """
        info: gets surface dimensions
        :return: (int, int)
        """
        return self._width, self._height

    def set_dimensions_and_clear(self, width, height):
        """
        info: clears and resizes TAMSurface
        :param width: int: 0 - inf
        :param height: int: 0 - inf
        :return:
        """
        self._width = width
        self._height = height

        length = width * height
        self._char_surface = [self._char] * length
        self._foreground_surface = [self._foreground_color] * length
        self._background_surface = [self._background_color] * length

    def get_defaults(self):
        """
        info: gets defaults
        :return: (str, int, int)
        """
        return self._char, self._foreground_color, self._background_color

    def set_defaults_and_clear(self, char, foreground_color, background_color):
        """
        info: clears surface and resets defaults
        :param char: str: len of 1
        :param foreground_color: int: 0 - inf
        :param background_color: int: 0 - inf
        :return:
        """
        self._char = char
        self._foreground_color = foreground_color
        self._background_color = background_color

        length = self._width * self._height
        self._char_surface = [self._char] * length
        self._foreground_surface = [self._foreground_color] * length
        self._background_surface = [self._background_color] * length

    def get_raw_surface(self):
        """
        info: gets raw surface
        :return: (list, list, list)
        """
        return self._char_surface, self._foreground_surface, self._background_surface

    def copy(self):
        """
        info: copy's TAMSurface
        :return: TAMSurface
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
        info: sets a single spot on the surface
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
                self._char_surface[spot] = char
            if foreground_color.has_alpha:
                self._foreground_surface[spot] = foreground_color.place_color_over(self._foreground_surface[spot],
                                                                                   override_alpha)
            else:
                self._foreground_surface[spot] = foreground_color
            if background_color.has_alpha:
                self._background_surface[spot] = background_color.place_color_over(self._background_surface[spot],
                                                                                   override_alpha)
            else:
                self._background_surface[spot] = background_color

    def get_spot(self, x, y):
        """
        info: gets spot info
        :param x: int
        :param y: int
        :return: (int, int, int) or None
        """

        spot = self.get_raw_spot(x, y)
        if spot != -1:
            return self._char_surface[spot], self._foreground_surface[spot], self._background_surface[spot]
        return None

    def get_from_raw_spot(self, spot):
        """
        info: gets spot info
        :param spot: x: int: 0 - (len(tam_surface) - 1)
        :return: (int, int, int) or None
        """
        if 0 <= spot < len(self._char_surface):
            return self._char_surface[spot], self._foreground_surface[spot], self._background_surface[spot]
        return None

    def draw_onto(self,
                  tam_surface,
                  start_x=0,
                  start_y=0,
                  surface_start_x=0,
                  surface_start_y=0,
                  surface_size_x=-1,
                  surface_size_y=-1,
                  override_alpha=False):
        """
        info: will draw tam_surface or part of a TAMSurface onto another TAMSurface
        :param tam_surface: TAMSurface
        :param start_x: int
        :param start_y: int
        :param surface_start_x: int
        :param surface_start_y: int
        :param surface_size_x: int: 0 - inf
        :param surface_size_y: int: 0 - inf
        :param override_alpha: bool
        :return:
        """

        start_x, \
        start_y, \
        surface_start_x, \
        surface_start_y, \
        surface_size_x, \
        surface_size_y = self.get_cross_rect(tam_surface,
                                             start_x,
                                             start_y,
                                             surface_start_x,
                                             surface_start_y,
                                             surface_size_x,
                                             surface_size_y)

        char_surface, foreground_surface, background_surface = tam_surface.get_raw_surface()
        this_char_surface, this_foreground_surface, this_background_surface = self.get_raw_surface()
        for y in range(surface_size_y):
            to_spot = self.get_raw_spot(start_x, start_y + y)
            draw_spot = tam_surface.get_raw_spot(surface_start_x, surface_start_y + y)
            for ts, ds in zip(range(to_spot, to_spot + surface_size_x), range(draw_spot, draw_spot + surface_size_x)):
                if override_alpha or not isinstance(char_surface[ds], TAMSurface):
                    this_char_surface[ts] = char_surface[ds]
                if foreground_surface[ds].has_alpha:
                    this_foreground_surface[ts] = foreground_surface[ds].place_color_over(this_foreground_surface[ts],
                                                                                        override_alpha)
                else:
                    this_foreground_surface[ts] = foreground_surface[ds]
                if background_surface[ds].has_alpha:
                    this_background_surface[ts] = background_surface[ds].place_color_over(this_background_surface[ts],
                                                                                        override_alpha)
                else:
                    this_background_surface[ts] = background_surface[ds]

    def get_cross_rect(self,
                       tam_surface,
                       start_x=0,
                       start_y=0,
                       surface_start_x=0,
                       surface_start_y=0,
                       surface_size_x=-1,
                       surface_size_y=-1):
        """
        info: will draw tam_surface or part of a TAMSurface onto another TAMSurface
        :param tam_surface: TAMSurface
        :param start_x: int
        :param start_y: int
        :param surface_start_x: int
        :param surface_start_y: int
        :param surface_size_x: int: 0 - inf
        :param surface_size_y: int: 0 - inf
        :return:
        """
        width, height = tam_surface.get_dimensions()
        if surface_size_x == -1:
            surface_size_x = width
        if surface_size_y == -1:
            surface_size_y = height

        if start_x < 0:
            surface_start_x += abs(start_x)
            surface_size_x = max(surface_size_x + start_x, 0)
            start_x = 0

        if start_y < 0:
            surface_start_y += abs(start_y)
            surface_size_y = max(surface_size_y + start_y, 0)
            start_y = 0

        if surface_start_x < 0:
            start_x += abs(surface_start_x)
            surface_size_x = max(surface_size_x + surface_start_x, 0)
            surface_start_x = 0

        if surface_start_y < 0:
            start_y += abs(surface_start_y)
            surface_size_y = max(surface_size_y + surface_start_y, 0)
            surface_start_y = 0

        surface_size_x = max(min(surface_size_x, width - surface_start_x, self._width - start_x), 0)
        surface_size_y = max(min(surface_size_y, height - surface_start_y, self._height - start_y), 0)

        return start_x, start_y, surface_start_x, surface_start_y, surface_size_x, surface_size_y

    def replace_alpha_chars(self, alpha_replacement=None):
        """
        :param alpha_replacement: None or str
        :return:
        """
        if alpha_replacement is None:
            alpha_replacement = self._char

        if alpha_replacement == ALPHA_CHAR:
            alpha_replacement = " "

        for spot, char in enumerate(self._char_surface):
            if char == ALPHA_CHAR:
                self._char_surface[spot] = alpha_replacement
