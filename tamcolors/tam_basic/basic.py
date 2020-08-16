from tamcolors.tam_io import identifier
from tamcolors.tam_io import tam_colors


IO = identifier.IO


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
    foreground, background = color

    if isinstance(foreground, str):
        foreground = _COLOR_NAME_TO_CODE.get(foreground.lower(), foreground)

    if isinstance(background, str):
        background = _COLOR_NAME_TO_CODE.get(background.lower(), background)

    return foreground, background


def printc(*value, same_color=False, sep=" ", end="\n", flush=True, stderr=False):
    if same_color:
        color = value[-1]
        value = sep.join(value[:-1]) + end
        IO.printc(value, _get_color_code(color), flush, stderr)
    else:
        for spot, value_and_color in enumerate(zip(value[::2], value[1::2])):
            this_value, this_color = value_and_color
            if (spot+1)*2 == len(value):
                this_value += end
            else:
                this_value += sep
            IO.printc(this_value, _get_color_code(this_color), flush, stderr)


def inputc(value, color):
    return IO.inputc(value, _get_color_code(color))


def clear():
    IO.clear()
