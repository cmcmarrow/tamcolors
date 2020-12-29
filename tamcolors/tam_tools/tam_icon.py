from . import tam_list_surface
from tamcolors.tam_io.tam_colors import *


def get_icon():
    s = " "
    l = "S"
    r = "R"
    o = "O"
    i = "L"
    c = "C"
    m = "M"
    a = "A"
    t = "T"

    icon_chars = ((t, t, t, t, t, t, s, s, a, a, a, a, s, s, m, m, s, s, s, m, m, s, c, c, c, c, s, o, o, o, o, o, o, s, i, i, s, s, s, o, o, o, o, o, o, s, r, r, r, r, r, r, s, l, l, l, l),
                  (t, t, t, t, t, t, s, a, a, a, a, a, a, s, m, m, m, s, m, m, m, s, c, c, c, c, s, o, o, o, o, o, o, s, i, i, s, s, s, o, o, o, o, o, o, s, r, r, r, r, r, r, s, l, l, l, l),
                  (s, s, t, t, s, s, s, a, a, s, s, a, a, s, m, m, m, m, m, m, m, s, c, c, s, s, s, o, o, s, s, o, o, s, i, i, s, s, s, o, o, s, s, o, o, s, r, r, s, s, r, r, s, l, l, s, s),
                  (s, s, t, t, s, s, s, a, a, s, s, a, a, s, m, m, s, m, s, m, m, s, c, c, s, s, s, o, o, s, s, o, o, s, i, i, s, s, s, o, o, s, s, o, o, s, r, r, s, s, r, r, s, l, l, s, s),
                  (s, s, t, t, s, s, s, a, a, a, a, a, a, s, m, m, s, s, s, m, m, s, c, c, s, s, s, o, o, s, s, o, o, s, i, i, s, s, s, o, o, s, s, o, o, s, r, r, r, r, r, r, s, l, l, l, l),
                  (s, s, t, t, s, s, s, a, a, a, a, a, a, s, m, m, s, s, s, m, m, s, c, c, s, s, s, o, o, s, s, o, o, s, i, i, s, s, s, o, o, s, s, o, o, s, r, r, r, r, r, s, s, l, l, l, l),
                  (s, s, t, t, s, s, s, a, a, s, s, a, a, s, m, m, s, s, s, m, m, s, c, c, s, s, s, o, o, s, s, o, o, s, i, i, s, s, s, o, o, s, s, o, o, s, r, r, r, r, s, s, s, s, s, l, l),
                  (s, s, t, t, s, s, s, a, a, s, s, a, a, s, m, m, s, s, s, m, m, s, c, c, s, s, s, o, o, s, s, o, o, s, i, i, s, s, s, o, o, s, s, o, o, s, r, r, s, r, r, s, s, s, s, l, l),
                  (s, s, t, t, s, s, s, a, a, s, s, a, a, s, m, m, s, s, s, m, m, s, c, c, c, c, s, o, o, o, o, o, o, s, i, i, i, i, s, o, o, o, o, o, o, s, r, r, s, s, r, r, s, l, l, l, l),
                  (s, s, t, t, s, s, s, a, a, s, s, a, a, s, m, m, s, s, s, m, m, s, c, c, c, c, s, o, o, o, o, o, o, s, i, i, i, i, s, o, o, o, o, o, o, s, r, r, s, s, s, r, s, l, l, l, l))

    char_to_color = {s: BLACK,
                     l: LIGHT_YELLOW,
                     r: LIGHT_RED,
                     o: LIGHT_PURPLE,
                     i: LIGHT_YELLOW,
                     c: LIGHT_GREEN,
                     m: LIGHT_BLUE,
                     a: LIGHT_YELLOW,
                     t: LIGHT_RED}

    icon_foreground = []
    for row in icon_chars:
        foreground_row = []
        for item in row:
            foreground_row.append(char_to_color[item])
        icon_foreground.append(foreground_row)

    return tam_list_surface.tam_list_surface(icon_chars, icon_foreground, BLACK)
