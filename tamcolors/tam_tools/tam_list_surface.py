# tamcolors libraries
from tamcolors import tam_io


"""
tam_list_surface
A way to make a list into a surface
"""


def tam_list_surface(chars, foreground_colors, background_colors):
    """
    info: makes a list into a TAMSurface
    :param chars: list, tuple
    :param foreground_colors: list, tuple, Color
    :param background_colors: list, tuple, Color
    :return: TAMSurface
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

    # make surface
    try:
        surface = tam_io.tam_surface.TAMSurface(len(chars[0]),
                                               len(chars),
                                               default_char,
                                               default_foreground,
                                               default_background)
    except IndexError:
        surface = tam_io.tam_surface.TAMSurface(0,
                                               len(chars),
                                               default_char,
                                               default_foreground,
                                               default_background)

    # if surface is empty 0X? or ?X0
    if not any(surface.get_dimensions()):
        return surface

    for y in range(surface.get_dimensions()[1]):
        for x in range(surface.get_dimensions()[0]):
            foreground = foreground_colors
            background = background_colors

            if foreground_mode:
                foreground = foreground_colors[y][x]

            if background_mode:
                background = background_colors[y][x]

            surface.set_spot(x, y, chars[y][x], foreground, background)

    return surface
