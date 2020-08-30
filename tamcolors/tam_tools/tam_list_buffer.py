# tamcolors libraries
from tamcolors import tam_io


"""
tam_list_buffer
A way to make a list into a buffer
"""


def tam_list_buffer(chars, foreground_colors, background_colors):
    """
    info: makes a list into a TAMBuffer
    :param chars: list, tuple
    :param foreground_colors: list, tuple, int
    :param background_colors: list, tuple, int
    :return: TAMBuffer
    """
    foreground_mode = not isinstance(foreground_colors, tam_io.tam_colors.Color)
    background_mode = not isinstance(background_colors, tam_io.tam_colors.Color)

    # get default parts
    default_char = " "
    if len(chars) != 0 and len(chars[0]) != 0:
        default_char = chars[0][0]

    default_background = background_colors
    if background_mode:
        if len(background_colors) != 0 and len(background_colors[0]) != 0:
            default_background = background_colors[0][0]
        else:
            default_background = background_colors

    default_foreground = foreground_colors
    if foreground_mode:
        if len(foreground_colors) != 0 and len(foreground_colors[0]) != 0:
            default_foreground = foreground_colors[0][0]
        else:
            default_foreground = foreground_colors

    # make buffer
    try:
        buffer = tam_io.tam_buffer.TAMBuffer(len(chars[0]),
                                             len(chars),
                                             default_char,
                                             default_foreground,
                                             default_background)
    except IndexError:
        buffer = tam_io.tam_buffer.TAMBuffer(0,
                                             len(chars),
                                             default_char,
                                             default_foreground,
                                             default_background)

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
