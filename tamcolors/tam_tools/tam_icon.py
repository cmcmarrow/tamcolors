from . import tam_list_buffer
from tamcolors.tam_io.tam_colors import *


def get_icon():
    c = "c"
    n = "4"
    s = " "

    icon_chars = ((c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, s, s, s, s, s, s, s, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, s, s, s, s, s, s, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, s, s, s, s, s, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, s, s, s, s, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, s, s, s, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, s, s, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, s, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, s, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, n, n, n, n, n, n, n),
                  (c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, n, n, n, n, n, n, n))

    char_to_color = {c: LIGHT_BLUE, n: LIGHT_RED, s: LIGHT_YELLOW}
    icon_background = []
    for row in icon_chars:
        new_row = []
        for item in row:
            new_row.append(char_to_color[item])

        icon_background.append(new_row)

    return tam_list_buffer.tam_list_buffer(icon_chars, BLACK, icon_background)
