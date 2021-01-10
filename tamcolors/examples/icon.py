from tamcolors import tam, tam_tools, tam_io


class BootLogo(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char=" ",
                         foreground_color=tam_io.tam_colors.GREEN,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=57, max_width=57, min_height=10, max_height=10)

        self.icon = tam_tools.tam_fade.tam_fade_in(surface=tam_tools.tam_icon.get_icon(),
                                                   char=" ",
                                                   foreground_color=tam_io.tam_colors.BLACK,
                                                   background_color=tam_io.tam_colors.BLACK)
        self.wait = 10

    def update(self, tam_loop, keys, loop_data):

        if not self.icon.done():
            self.icon.slide()
        else:
            self.wait -= 1

        if self.wait == 0 or len(keys):
            tam_loop.done()

    def draw(self, tam_surface, loop_data):
        tam_surface.clear()

        tam_surface.draw_onto(self.icon.peak(), 0, 0)


def run():
    tam.tam_loop.TAMLoop(BootLogo()).run()
