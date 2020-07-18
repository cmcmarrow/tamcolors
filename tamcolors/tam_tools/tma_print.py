# tamcolors libraries
from . import tma_str

"""
tma_print will draw string on a tma_buffer
"""


class TMAPrintError(Exception):
    pass


def tma_print(tma_buffer, x, y, text, foreground_color, background_color, error_bad_char=False, bad_char=""):
    """
    info: tma_print will draw string on a tma_buffer
    :param tma_buffer: TMABuffer
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
        text = tma_str.make_tma_str(text)
    else:
        text = tma_str.make_tma_str(text, bad_char=bad_char)

    at_x = x
    for char in str(text):
        if char == "\n":
            at_x = x
            y += 1
        else:
            tma_buffer.set_spot(at_x, y, char, foreground_color, background_color)
            at_x += 1
