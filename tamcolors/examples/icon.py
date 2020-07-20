from tamcolors import tam, tam_tools


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

    char_to_color = {c: 3, n: 4, s: 6}
    icon_background = []
    for row in icon_chars:
        new_row = []
        for item in row:
            new_row.append(char_to_color[item])

        icon_background.append(new_row)

    return tam_tools.tam_list_buffer.tam_list_buffer(icon_chars, 0, icon_background)


class BootLogo(tam.tam_loop.TAMFrame):
    def __init__(self):
        """
        info: Makes a BootLogo Object. Will display the logo and author's name
        """
        super().__init__(10,
                         " ",
                         2,
                         0,
                         70, 70, 40, 40)

        self.icon = tam_tools.tam_fade.tam_fade_in(get_icon(),
                                                   " ",
                                                   0,
                                                   0)
        self.wait = 10

    def update(self, tam_loop, keys, loop_data):

        if not self.icon.done():
            self.icon.slide()
        else:
            self.wait -= 1

        if self.wait == 0:
            tam_loop.done()

    def draw(self, tam_buffer, loop_data):
        tam_buffer.clear()

        tam_buffer.draw_onto(self.icon.peak(),
                             *tam_tools.tam_placing.center(35, 15, buffer=self.icon.peak()))

        tam_tools.tam_print.tam_print(tam_buffer, *tam_tools.tam_placing.center(35, 28, len("tamcolors"), 1),
                                      "tamcolors",
                                      15,
                                      0)


def run():
    loop = tam.tam_loop.TAMLoop(BootLogo())
    loop.run()
