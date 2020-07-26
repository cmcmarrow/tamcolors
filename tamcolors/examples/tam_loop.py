from tamcolors import tam, tam_tools, tam_io


class TAMLoopHelloWorld(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char="+",
                         foreground_color=tam_io.tam_colors.GRAY,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=70, max_width=70, min_height=40, max_height=40)

    def update(self, tam_loop, keys, loop_data):
        if keys:
            tam_loop.done()

    def draw(self, tam_buffer, loop_data):
        tam_buffer.clear()

        tam_tools.tam_print.tam_print(tam_buffer,
                                      0,
                                      0,
                                      text="Hello World!",
                                      foreground_color=tam_io.tam_colors.LIGHT_AQUA,
                                      background_color=tam_io.tam_colors.BLACK)


def run():
    tam.tam_loop.TAMLoop(TAMLoopHelloWorld()).run()
