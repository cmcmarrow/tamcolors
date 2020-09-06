from tamcolors import tam, tam_io


CLOUD_COLOR = tam_io.tam_colors.Color(7, 7, tam_io.tam_colors.RGBA(55, 55, 55, 77))


class Clouds(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=2,
                         char=".",
                         foreground_color=tam_io.tam_colors.WHITE,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=70, max_width=70, min_height=40, max_height=40)

        self._ground = tam_io.tam_buffer.TAMBuffer(70, 70, ".", tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.GREEN)

        self._ground.set_spot(3, 4, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.GREEN, tam_io.tam_colors.YELLOW)
        self._ground.set_spot(5, 4, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.GREEN, tam_io.tam_colors.YELLOW)
        self._ground.set_spot(4, 4, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.GREEN, tam_io.tam_colors.YELLOW)
        self._ground.set_spot(4, 3, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.GREEN, tam_io.tam_colors.YELLOW)
        self._ground.set_spot(4, 5, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.GREEN, tam_io.tam_colors.YELLOW)
        self._ground.set_spot(5, 5, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.GREEN, tam_io.tam_colors.YELLOW)

        self._ground.set_spot(13, 14, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)
        self._ground.set_spot(15, 14, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.LIGHT_YELLOW, tam_io.tam_colors.GREEN)
        self._ground.set_spot(14, 14, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.PURPLE, tam_io.tam_colors.GREEN)
        self._ground.set_spot(14, 13, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.LIGHT_AQUA, tam_io.tam_colors.GREEN)
        self._ground.set_spot(14, 15, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)
        self._ground.set_spot(15, 15, tam_io.tam_buffer.ALPHA_CHAR, tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)

        self._clouds = [[66, 4],
                        [5, 9],
                        [55, 14],
                        [20, 20],
                        [55, 33], [54, 33]]

    def update(self, tam_loop, keys, loop_data):
        if keys:
            tam_loop.done()

    def draw(self, tam_buffer, loop_data):
        tam_buffer.clear()
        tam_buffer.draw_onto(self._ground)

        for cloud in self._clouds:
            cloud[0] += 1
            if cloud[0] == 70:
                cloud[0] = -5
            tam_buffer.set_spot(*cloud, tam_io.tam_buffer.ALPHA_CHAR, CLOUD_COLOR, CLOUD_COLOR)


def run():
    tam.tam_loop.TAMLoop(Clouds()).run()
