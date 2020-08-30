from tamcolors import tam, tam_tools, tam_io

OTHER_COLORS = (tam_io.tam_colors.RGBA(128, 0, 0),
                tam_io.tam_colors.RGBA(139, 0, 0),
                tam_io.tam_colors.RGBA(165, 42, 42),
                tam_io.tam_colors.RGBA(178, 34, 34),
                tam_io.tam_colors.RGBA(220, 20, 60),
                tam_io.tam_colors.RGBA(255, 0, 0),
                tam_io.tam_colors.RGBA(255, 99, 71),
                tam_io.tam_colors.RGBA(255, 127, 80),
                tam_io.tam_colors.RGBA(205, 92, 92),
                tam_io.tam_colors.RGBA(240, 128, 128),
                tam_io.tam_colors.RGBA(233, 150, 122),
                tam_io.tam_colors.RGBA(250, 128, 114),
                tam_io.tam_colors.RGBA(255, 160, 122),
                tam_io.tam_colors.RGBA(255, 69, 0),
                tam_io.tam_colors.RGBA(255, 140, 0),
                tam_io.tam_colors.RGBA(255, 165, 0))


class RGBCOLOR(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char="+",
                         foreground_color=tam_io.tam_colors.AQUA,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=70, max_width=70, min_height=40, max_height=40)

        self._key_manager = tam_tools.tam_key_manager.TAMKeyManager()

        self._timer = 0
        self._color = False

    def update(self, tam_loop, keys, loop_data):
        self._key_manager.update(keys)

        if self._key_manager.get_key_state("a"):
            tam_loop.set_tam_color_defaults()

        if self._key_manager.get_key_state("b"):
            for spot, color in enumerate(OTHER_COLORS):
                tam_loop.set_color_16(spot, color)
                tam_loop.set_color_256(spot, color)

        if self._key_manager.get_key_state("BACKSPACE"):
            tam_loop.done()

        self._timer += 1
        if self._timer == 10:
            self._timer = 0
            self._color = not self._color
            if self._color:
                tam_loop.set_color_16(1, tam_io.tam_colors.RGBA(55, 155, 155))
                tam_loop.set_color_256(1, tam_io.tam_colors.RGBA(55, 155, 155))
            else:
                tam_loop.set_color_16(1, tam_io.tam_colors.RGBA(155, 155, 55))
                tam_loop.set_color_256(1, tam_io.tam_colors.RGBA(155, 155, 55))

    def draw(self, tam_buffer, loop_data):
        tam_buffer.clear()

        for background_color in range(16):
            for foreground_color in range(16):
                tam_buffer.set_spot(foreground_color,
                                    background_color,
                                    "@",
                                    tam_io.tam_colors.COLORS[foreground_color],
                                    tam_io.tam_colors.COLORS[background_color])

        tam_tools.tam_print.tam_print(tam_buffer,
                                      0,
                                      20,
                                      text="Press backspace to quit.",
                                      foreground_color=tam_io.tam_colors.LIGHT_AQUA,
                                      background_color=tam_io.tam_colors.BLACK)

        tam_tools.tam_print.tam_print(tam_buffer,
                                      0,
                                      21,
                                      text="Press a or b to change colors",
                                      foreground_color=tam_io.tam_colors.LIGHT_AQUA,
                                      background_color=tam_io.tam_colors.BLACK)


def run():
    tam.tam_loop.TAMLoop(RGBCOLOR()).run()
