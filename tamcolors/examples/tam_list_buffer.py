from tamcolors import tam, tam_tools, tam_io

S = " "
D = "$"
L = tam_io.tam_colors.LIGHT_AQUA
W = tam_io.tam_colors.WHITE

BUFFER = ((S, S, S, D, S, S, S),
          (S, S, S, D, S, S, S),
          (S, S, S, D, S, S, S),
          (S, S, S, S, S, S, S),
          (S, S, S, D, S, S, S),
          (S, S, S, S, S, S, S))

BUFFER_BACKGROUND = ((W, W, W, L, W, W, W),
                     (W, W, W, L, W, W, W),
                     (W, W, W, L, W, W, W),
                     (W, W, W, W, W, W, W),
                     (W, W, W, L, W, W, W),
                     (W, W, W, W, W, W, W))


class TAMListBuffer(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char="+",
                         foreground_color=tam_io.tam_colors.GRAY,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=70, max_width=70, min_height=40, max_height=40)

        self._buffer = tam_tools.tam_list_buffer.tam_list_buffer(BUFFER,
                                                                 tam_io.tam_colors.WHITE,
                                                                 BUFFER_BACKGROUND)

    def update(self, tam_loop, keys, loop_data):
        if keys:
            tam_loop.done()

    def draw(self, tam_buffer, loop_data):
        tam_buffer.clear()

        tam_buffer.draw_onto(self._buffer, 5, 9)


def run():
    tam.tam_loop.TAMLoop(TAMListBuffer()).run()

