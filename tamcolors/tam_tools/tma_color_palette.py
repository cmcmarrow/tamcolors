# built in library
import itertools

# Charles McMarrow library
from tamcolors import checks

# Charles McMarrow

"""
ColorPalette set and get colors
write rules that can update the color palette
"""


class TMAColorPaletteError(Exception):
    pass


class TMAColorPalette:
    def __init__(self, color_range=range(0, 16), color_rules=None):
        """
        info: makes a ColorPalette object
        :param color_range: range
        :param color_rules: dict
        """
        if color_rules is None:
            color_rules = {}

        # checks
        checks.checks.instance_check(color_range, range, TMAColorPaletteError)
        checks.checks.instance_check(color_rules, dict, TMAColorPaletteError)
        for key in color_rules:
            checks.checks.instance_check(key, int, TMAColorPaletteError)
            checks.checks.instance_check(color_rules[key], TMAColorPaletteRule, TMAColorPaletteError)

        self.__color_palette = {key: key for key in color_range}
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
        :param color: int
        :return:
        """
        # checks
        checks.checks.instance_check(color, int, TMAColorPaletteError)

        self.set_color(key, color)

    def get_color(self, key):
        """
        info: gets a color from the color palette
        :param key: object
        :return:
        """
        if self.key_present(key):
            return self.__color_palette[key]
        raise TMAColorPaletteError("{0} is not key in the color palette.".format(repr(key)))

    def set_color(self, key, color):
        """
        info sets a color to the color palette
        :param key: object
        :param color: int
        :return:
        """
        # checks
        checks.checks.instance_check(color, int, TMAColorPaletteError)

        try:
            self.__color_palette[key] = color
        except TypeError:
            raise TMAColorPaletteError("{0} can not be a key".format(repr(key)))

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
        info: upsdates color_palette rules
        :return:
        """
        # checks
        for key in self.__color_rules:
            self.__color_rules[key].update(self, key)

    def set_rule(self, key, rule):
        """
        info: sets a color rule
        :param key: object
        :param rule: instance of TMAColorPaletteRule
        :return:
        """
        # checks
        checks.checks.instance_check(rule, TMAColorPaletteRule, TMAColorPaletteError)

        try:
            self.__color_rules[key] = rule
        except TypeError:
            raise TMAColorPaletteError("{0} can not be a key".format(repr(key)))

    def get_rule(self, key):
        """
        info: gets a instance of TMAColorPaletteRule or None
        :param key: object
        :return: instance of TMAColorPaletteRule or None
        """
        try:
            return self.__color_rules.get(key)
        except TypeError:
            pass


class TMAColorPaletteRule:
    def __init__(self):
        pass

    def update(self, color_palette, key):
        raise NotImplementedError()


class TMADefaultColor(TMAColorPaletteRule):
    def __init__(self, color):
        """
        info: will rest the color every time when updated
        :param color: int
        """
        # checks
        checks.checks.instance_check(color, int, TMAColorPaletteError)
        super().__init__()
        self.__color = color

    def get_color(self):
        """
        info: gets the default color
        :return: int
        """
        return self.__color

    def set_color(self, color):
        """
        info: sets the default color
        :param color: int
        :return:
        """
        # checks
        checks.checks.instance_check(color, int, TMAColorPaletteError)
        self.__color = color

    def update(self, color_palette, key):
        """
        info: will update the color_palette color
        :param color_palette: TMAColorPalette
        :param key: object
        :return:
        """
        # checks
        checks.checks.instance_check(color_palette, TMAColorPalette, TMAColorPaletteError)

        color_palette[key] = self.__color


class TMACycleColor(TMAColorPaletteRule):
    def __init__(self, colors, clock=1):
        """
        info: will cycle colors
        :param colors: tuple or int: [int, int, int, ...]
        :param clock: int: 1 - inf
        """
        checks.checks.in_instances_check(colors, (tuple, list), TMAColorPaletteError)
        checks.checks.range_check(clock, 1, None, TMAColorPaletteError)
        for color in colors:
            checks.checks.instance_check(color, int, TMAColorPaletteError)
        super().__init__()
        self.__clock = clock
        self.__clock_at = clock
        self.__cycle_color = itertools.cycle(colors)

    def set_colors(self, colors):
        """
        info: sets all the colors
        :param colors: tuple or int: [int, int, int, ...]
        :return:
        """
        checks.checks.in_instances_check(colors, (tuple, list), TMAColorPaletteError)
        for color in colors:
            checks.checks.instance_check(color, int, TMAColorPaletteError)
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
        checks.checks.range_check(clock, 1, None, TMAColorPaletteError)
        self.__clock = clock

    def update(self, color_palette, key):
        """
        info: will update the color_palette color
        :param color_palette: TMAColorPalette
        :param key: object
        :return:
        """
        checks.checks.instance_check(color_palette, TMAColorPalette, TMAColorPaletteError)

        if self.__clock_at >= self.__clock:
            self.__clock_at = 0
            color_palette[key] = next(self.__cycle_color)
        self.__clock_at += 1
