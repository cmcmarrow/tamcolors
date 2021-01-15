from tamcolors import tam, tam_io, tam_tools


class TAMCOLORS(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char="+",
                         foreground_color=tam_io.tam_colors.GRAY,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=70, max_width=70, min_height=40, max_height=40)

    def update(self, tam_loop, keys, loop_data, *args):
        if keys:
            tam_loop.done()

    def draw(self, tam_surface, loop_data, *args):
        tam_surface.clear()

        mode_16_color = [[] for _ in range(16)]
        for color in tam_io.tam_colors.COLORS:
            mode_16_color[color.mode_16].append(color)
        at = 25

        for x, colors in enumerate(mode_16_color):
            for y, color in enumerate(colors):
                tam_surface.set_spot(x, y, "A", color, color)
                if y == 0:
                    tam_surface.set_spot(x, y, str(x)[-1], tam_io.tam_colors.WHITE, color)
                if y == at:
                    tam_tools.tam_print.tam_print(tam_surface, 18, x, color.mode_256, color, tam_io.tam_colors.BLACK)
                    tam_tools.tam_print.tam_print(tam_surface, 23, x, color.mode_256, tam_io.tam_colors.WHITE, tam_io.tam_colors.BLACK)
                    tam_tools.tam_print.tam_print(tam_surface, 28, x, x, tam_io.tam_colors.WHITE, tam_io.tam_colors.BLACK)
        tam_surface.set_spot(16, at, "#", tam_io.tam_colors.YELLOW, tam_io.tam_colors.YELLOW)


def run():
    tam.tam_loop.TAMLoop(TAMCOLORS()).run()
