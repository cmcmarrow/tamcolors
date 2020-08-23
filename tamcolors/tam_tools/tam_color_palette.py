# built in library
import itertools

from tamcolors.tam_io.tam_colors import *


"""
ColorPalette set and get colors
write rules that can update the color palette
"""


class TAMColorPaletteError(Exception):
    pass


class TAMColorPalette:
    def __init__(self, color_range=range(0, 16), color_rules=None):
        """
        info: makes a ColorPalette object
        :param color_range: range
        :param color_rules: dict
        """
        if color_rules is None:
            color_rules = {}

        self.__color_palette = {key: COLORS[key] for key in color_range}
        self.__color_rules = color_rules

    def __str__(self):
        """
        info: converts the color palette to a string
        :return: str
        """
        return str(self.__color_palette)

    def __getitem__(self, key):
        """
        info: gets a color from the color palette
        :param key: object
        :return: int
        """
        return self.get_color(key)

    def __setitem__(self, key, color):
        """
        info sets a color to the color palette
        :param key: object
        :param color: Color
        :return:
        """

        self.set_color(key, color)

    def get_color(self, key):
        """
        info: gets a color from the color palette
        :param key: object
        :return:
        """
        if self.key_present(key):
            return self.__color_palette[key]
        raise TAMColorPaletteError("{0} is not key in the color palette.".format(repr(key)))

    def set_color(self, key, color):
        """
        info sets a color to the color palette
        :param key: object
        :param color: Color
        :return:
        """

        try:
            self.__color_palette[key] = color
        except TypeError:
            raise TAMColorPaletteError("{0} can not be a key".format(repr(key)))

    def key_present(self, key):
        """
        info: checks if key is in color palette
        :param key: object
        :return: bool
        """
        try:
            return key in self.__color_palette
        except TypeError:
            return False

    def update(self):
        """
        info: updates color_palette rules
        :return:
        """
        # checks
        for key in self.__color_rules:
            self.__color_rules[key].update(self, key)

    def set_rule(self, key, rule):
        """
        info: sets a color rule
        :param key: object
        :param rule: instance of TAMColorPaletteRule
        :return:
        """
        try:
            self.__color_rules[key] = rule
        except TypeError:
            raise TAMColorPaletteError("{0} can not be a key".format(repr(key)))

    def get_rule(self, key):
        """
        info: gets a instance of TAMColorPaletteRule or None
        :param key: object
        :return: instance of TAMColorPaletteRule or None
        """
        try:
            return self.__color_rules.get(key)
        except TypeError:
            pass


class TAMColorPaletteRule:
    def __init__(self):
        pass

    def update(self, color_palette, key):
        raise NotImplementedError()


class TAMDefaultColor(TAMColorPaletteRule):
    def __init__(self, color):
        """
        info: will rest the color every time when updated
        :param color: Color
        """
        super().__init__()
        self.__color = color

    def get_color(self):
        """
        info: gets the default color
        :return: Color
        """
        return self.__color

    def set_color(self, color):
        """
        info: sets the default color
        :param color: Color
        :return:
        """
        self.__color = color

    def update(self, color_palette, key):
        """
        info: will update the color_palette color
        :param color_palette: TAMColorPalette
        :param key: object
        :return:
        """
        color_palette[key] = self.__color


class TAMCycleColor(TAMColorPaletteRule):
    def __init__(self, colors, clock=1):
        """
        info: will cycle colors
        :param colors: tuple or int: [Color, Color, Color, ...]
        :param clock: int: 1 - inf
        """
        super().__init__()
        self.__clock = clock
        self.__clock_at = clock
        self.__cycle_color = itertools.cycle(colors)

    def set_colors(self, colors):
        """
        info: sets all the colors
        :param colors: tuple or int: [Color, Color, Color, ...]
        :return:
        """
        self.__cycle_color = itertools.cycle(colors)

    def get_clock(self):
        """
        info: gets the clock rate
        :return: int
        """
        return self.__clock

    def set_clock(self, clock):
        """
        info: sets the clock
        :param clock: int
        :return: int: 1 - inf
        """
        self.__clock = clock

    def update(self, color_palette, key):
        """
        info: will update the color_palette color
        :param color_palette: TAMColorPalette
        :param key: object
        :return:
        """
        if self.__clock_at >= self.__clock:
            self.__clock_at = 0
            color_palette[key] = next(self.__cycle_color)
        self.__clock_at += 1
