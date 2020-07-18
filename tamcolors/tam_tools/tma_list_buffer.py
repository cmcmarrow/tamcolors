# Charles McMarrow libraries
from tamcolors import checks
from tamcolors import tam

# Charles McMarrow

"""
tma_list_buffer
A way to make a list into a buffer
"""


class TMAListBufferError(Exception):
    pass


def _list_buffer_check(list_buffer, check, *args):
    checks.checks.in_instances_check(list_buffer, (list, tuple), TMAListBufferError)
    for row in list_buffer:
        checks.checks.in_instances_check(row, (list, tuple), TMAListBufferError)
        for item in row:
            check(item, *args)


def tma_list_buffer(chars, foreground_colors, background_colors):
    """
    info: makes a list into a TMABuffer
    :param chars: list, tuple
    :param foreground_colors: list, tuple, int
    :param background_colors: list, tuple, int
    :return: TMABuffer
    """
    # checks
    _list_buffer_check(chars, checks.checks.single_block_char_check, TMAListBufferError)

    checks.checks.in_instances_check(foreground_colors, (list, tuple, int), TMAListBufferError)
    if isinstance(foreground_colors, int):
        foreground_mode = False
        checks.checks.range_check(foreground_colors, 0, None, TMAListBufferError)
    else:
        foreground_mode = True
        _list_buffer_check(foreground_colors, checks.checks.range_check, 0, None, TMAListBufferError)

    checks.checks.in_instances_check(background_colors, (list, tuple, int), TMAListBufferError)
    if isinstance(background_colors, int):
        background_mode = False
        checks.checks.range_check(background_colors, 0, None, TMAListBufferError)
    else:
        background_mode = True
        _list_buffer_check(background_colors, checks.checks.range_check, 0, None, TMAListBufferError)

    # get default parts
    default_char = " "
    if len(chars) != 0 and len(chars[0]) != 0:
        default_char = chars[0][0]

    default_background = background_colors
    if background_mode:
        if len(background_colors) != 0 and len(background_colors[0]) != 0:
            default_background = background_colors[0][0]
        else:
            default_background = 0

    default_foreground = foreground_colors
    if foreground_mode:
        if len(foreground_colors) != 0 and len(foreground_colors[0]) != 0:
            default_foreground = foreground_colors[0][0]
        else:
            default_foreground = 0

    # make buffer
    try:
        buffer = tam.tma_buffer.TMABuffer(len(chars[0]),
                                          len(chars),
                                          default_char,
                                          default_foreground,
                                          default_background)
    except IndexError:
        buffer = tam.tma_buffer.TMABuffer(0,
                                          len(chars),
                                          default_char,
                                          default_foreground,
                                          default_background)

    # checks
    # check chars has same row length for every row
    for row in chars:
        checks.checks.is_equal_check(len(row), buffer.get_dimensions()[0], TMAListBufferError)

    if foreground_mode:
        # checks foreground_colors dimensions
        checks.checks.is_equal_check(len(foreground_colors), buffer.get_dimensions()[1])
        for row in foreground_colors:
            checks.checks.is_equal_check(len(row), buffer.get_dimensions()[0], TMAListBufferError)

    if background_mode:
        # checks background_colors dimensions
        checks.checks.is_equal_check(len(background_colors), buffer.get_dimensions()[1])
        for row in background_colors:
            checks.checks.is_equal_check(len(row), buffer.get_dimensions()[0], TMAListBufferError)

    # if buffer is empty 0X? or ?X0
    if not any(buffer.get_dimensions()):
        return buffer

    for y in range(buffer.get_dimensions()[1]):
        for x in range(buffer.get_dimensions()[0]):
            foreground = foreground_colors
            background = background_colors

            if foreground_mode:
                foreground = foreground_colors[y][x]

            if background_mode:
                background = background_colors[y][x]

            buffer.set_spot(x, y, chars[y][x], foreground, background)

    return buffer
