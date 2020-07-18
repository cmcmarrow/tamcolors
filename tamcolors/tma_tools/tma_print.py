# built in library
import string

# Charles McMarrow libraries
from tamcolors import checks
from tamcolors import tma
from . import tma_str

# Charles McMarrow

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

    # checks
    checks.checks.instance_check(tma_buffer, tma.tma_buffer.TMABuffer, TMAPrintError)
    checks.checks.instance_check(x, int, TMAPrintError)
    checks.checks.instance_check(y, int, TMAPrintError)
    checks.checks.has_method_check(text, "__str__", TMAPrintError)
    checks.checks.range_check(foreground_color, -1, None, TMAPrintError)
    checks.checks.range_check(background_color, -1, None, TMAPrintError)
    checks.checks.instance_check(error_bad_char, bool, TMAPrintError)
    checks.checks.instance_check(bad_char, str, TMAPrintError)

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
