# tamcolors libraries
from . import tam_str

"""
tam_print will draw string on a tam_surface
"""


def tam_print(tam_surface, x, y, text, foreground_color, background_color, error_bad_char=False, bad_char=""):
    """
    info: tam_print will draw string on a tam_surface
    :param tam_surface: TAMSurface
    :param x: int
    :param y: int
    :param text: object with __str__
    :param foreground_color: int: -1 - inf: use current foreground_color
    :param background_color: int: -1 - inf: use current background_color
    :param error_bad_char: bool
    :param bad_char: str
    :return:
    """
    if error_bad_char:
        text = tam_str.make_tam_str(text)
    else:
        text = tam_str.make_tam_str(text, bad_char=bad_char)

    at_x = x
    for char in str(text):
        if char == "\n":
            at_x = x
            y += 1
        else:
            tam_surface.set_spot(at_x, y, char, foreground_color, background_color)
            at_x += 1
