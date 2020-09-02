# tamcolors libraries
from tamcolors.tam_io import tam_colors
from tamcolors.tam_io import tam_identifier

IO = tam_identifier.IO

_COLOR_NAME_TO_CODE = {"default": tam_colors.DEFAULT,
                       "black": tam_colors.BLACK,
                       "blue": tam_colors.BLUE,
                       "green": tam_colors.GREEN,
                       "aqua": tam_colors.AQUA,
                       "red": tam_colors.RED,
                       "purple": tam_colors.PURPLE,
                       "yellow": tam_colors.YELLOW,
                       "white": tam_colors.WHITE,
                       "gray": tam_colors.GRAY,
                       "light blue": tam_colors.LIGHT_BLUE,
                       "light green": tam_colors.LIGHT_GREEN,
                       "light aqua": tam_colors.LIGHT_AQUA,
                       "light red": tam_colors.LIGHT_RED,
                       "light purple": tam_colors.LIGHT_PURPLE,
                       "light yellow": tam_colors.LIGHT_YELLOW,
                       "light white": tam_colors.LIGHT_WHITE}


def _get_color_code(color):
    """
    info: Get console color
    :param color: tuple
    :return: tuple
    """
    foreground, background = color

    if isinstance(foreground, str):
        foreground = _COLOR_NAME_TO_CODE.get(foreground.lower(), foreground)

    if isinstance(background, str):
        background = _COLOR_NAME_TO_CODE.get(background.lower(), background)

    return foreground, background


def printc(*output, same_color=False, sep=" ", end="\n", flush=True, stderr=False):
    """
    info: Prints color output to the console
    :param output:
    :param same_color: bool
    :param sep: str
    :param end: str
    :param flush: bool
    :param stderr: std
    :return: None
    """
    if same_color:
        color = output[-1]
        output = sep.join(output[:-1]) + end
        IO.printc(output, _get_color_code(color), flush, stderr)
    else:
        for spot, value_and_color in enumerate(zip(output[::2], output[1::2])):
            this_value, this_color = value_and_color
            if (spot + 1) * 2 == len(output):
                this_value += end
            else:
                this_value += sep
            IO.printc(this_value, _get_color_code(this_color), flush, stderr)


def inputc(output, color):
    """
    info: Will get color input from console
    :param output: str
    :param color: tuple
    :return: str
    """
    return IO.inputc(output, _get_color_code(color))


def clear():
    """
    info: Clears the console
    :return: None
    """
    IO.clear()


def reset_colors_to_console_defaults():
    """
    info: will reset colors to console defaults
    :return: None
    """
    IO.reset_colors_to_console_defaults()


def set_tam_color_defaults():
    """
    info: will set console colors to tam defaults
    :return: None
    """
    IO.set_tam_color_defaults()
