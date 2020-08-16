from collections import namedtuple


"""
terminal colors supported on all platforms
"""

COLOR = namedtuple("COLOR", ("mode_2", "mode_16", "has_alpha"))


def build_color(mode_16, mode_2=None):
    if mode_2 is None:
        mode_2 = mode_16
    has_alpha = mode_16 == -2 or mode_2 == -2
    return COLOR(mode_2, mode_16, has_alpha)


def place_color_over(new_color, old_color, override_alpha):
    if override_alpha:
        return old_color

    mode_2 = new_color.mode_2
    if new_color.mode_2 == -2:
        mode_2 = old_color.mode_2

    mode_16 = new_color.mode_16
    if new_color.mode_16 == -2:
        mode_16 = old_color.mode_16

    return build_color(mode_16, mode_2)


ALPHA = build_color(-2)
DEFAULT = build_color(-1)
BLACK = build_color(0)
BLUE = build_color(1)
GREEN = build_color(2)
AQUA = build_color(3)
RED = build_color(4)
PURPLE = build_color(5)
YELLOW = build_color(6)
WHITE = build_color(7)
GRAY = build_color(8)
LIGHT_BLUE = build_color(9)
LIGHT_GREEN = build_color(10)
LIGHT_AQUA = build_color(11)
LIGHT_RED = build_color(12)
LIGHT_PURPLE = build_color(13)
LIGHT_YELLOW = build_color(14)
LIGHT_WHITE = build_color(15)

COLOR_LIST = [BLACK,
              BLUE,
              GREEN,
              AQUA,
              RED,
              PURPLE,
              YELLOW,
              WHITE,
              GRAY,
              LIGHT_BLUE,
              LIGHT_GREEN,
              LIGHT_AQUA,
              LIGHT_RED,
              LIGHT_PURPLE,
              LIGHT_YELLOW,
              LIGHT_WHITE]
