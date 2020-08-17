from collections import namedtuple


"""
terminal colors supported on all platforms
"""

COLOR = namedtuple("COLOR", ("mode_2", "mode_16", "mode_256", "mode_rgb", "has_alpha"))
RGBA = namedtuple("RGBA", ("R", "G", "B", "A", "is_default"))


def build_color(mode_16=None, mode_256=None, mode_rgb=None, mode_2=None):
    if mode_2 is None:
        mode_2 = mode_16
    has_alpha = mode_16 == -2 or mode_2 == -2
    return COLOR(mode_2, mode_16, mode_256, mode_rgb, has_alpha)


def build_rgba(r, g, b, a=255, default=False):
    return RGBA(r, g, b, a, default)


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


ALPHA = build_color(-2, -2, build_rgba(0, 0, 0, 0))
DEFAULT = build_color(-1, -1, build_rgba(0, 0, 0, 255, True))

BLACK = build_color(0, 0, build_rgba(0, 0, 0))
RED = build_color(1, 1, build_rgba(128, 0, 0))
GREEN = build_color(2, 2, build_rgba(0, 128, 0))
YELLOW = build_color(3, 3, build_rgba(128, 128, 0))
BLUE = build_color(4, 4, build_rgba(0, 0, 128))
PURPLE = build_color(5, 5, build_rgba(128, 0, 128))
AQUA = build_color(6, 6, build_rgba(0, 128, 128))
WHITE = build_color(7, 7, build_rgba(192, 192, 192))
GRAY = build_color(8, 8, build_rgba(128, 128, 128))
LIGHT_RED = build_color(9, 9, build_rgba(255, 0, 0))
LIGHT_GREEN = build_color(10, 10, build_rgba(0, 255, 0))
LIGHT_YELLOW = build_color(11, 11, build_rgba(255, 255, 0))
LIGHT_BLUE = build_color(12, 12, build_rgba(0, 0, 255))
LIGHT_PURPLE = build_color(13, 13, build_rgba(255, 0, 255))
LIGHT_AQUA = build_color(14, 14, build_rgba(0, 255, 255))
LIGHT_WHITE = build_color(15, 15, build_rgba(255, 255, 255))

COLOR_LIST = [BLACK,
              RED,
              GREEN,
              YELLOW,
              BLUE,
              PURPLE,
              AQUA,
              WHITE,
              GRAY,
              LIGHT_RED,
              LIGHT_GREEN,
              LIGHT_YELLOW,
              LIGHT_BLUE,
              LIGHT_PURPLE,
              LIGHT_AQUA,
              LIGHT_WHITE]
