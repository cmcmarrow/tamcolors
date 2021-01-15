from tamcolors import tam, tam_tools, tam_io


class TAMAlpha(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char="+",
                         foreground_color=tam_io.tam_colors.GRAY,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=70, max_width=70, min_height=40, max_height=40)
        self._red_surface = tam_io.tam_surface.TAMSurface(7, 17, "&", tam_io.tam_colors.WHITE, tam_io.tam_colors.RED)
        self._box = tam_tools.tam_text_box.TAMTextBox("Hello!\nThis is{}a text box!".format(tam_io.tam_surface.ALPHA_CHAR),
                                                      26,
                                                      9,
                                                      "@",
                                                      tam_io.tam_colors.ALPHA,
                                                      tam_io.tam_colors.ALPHA,
                                                      clock=1,
                                                      center_horizontal=True,
                                                      center_vertical=True,
                                                      char_background=tam_io.tam_surface.ALPHA_CHAR)

    def update(self, tam_loop, keys, loop_data, *args):
        if keys:
            tam_loop.done()

        self._box.update()

    def draw(self, tam_surface, loop_data, *args):
        tam_surface.clear()

        tam_surface.draw_onto(self._red_surface, 0, 0)
        self._box.draw(tam_surface, 5, 10)

        tam_tools.tam_print.tam_print(tam_surface,
                                      0,
                                      0,
                                      text="Hello" + tam_io.tam_surface.ALPHA_CHAR + "World!",
                                      foreground_color=tam_io.tam_colors.LIGHT_AQUA,
                                      background_color=tam_io.tam_colors.ALPHA)


def run():
    tam.tam_loop.TAMLoop(TAMAlpha()).run()
