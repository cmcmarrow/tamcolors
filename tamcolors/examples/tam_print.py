from tamcolors import tam, tam_tools, tam_io


EXAMPLE_STR = """This is an example of how to use tam print!
Not that hard right?"""


class TAMPrint(tam.tam_loop.TAMFrame):
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

        tam_tools.tam_print.tam_print(tam_buffer,
                                      5,
                                      6,
                                      text="cats:\t5\ndogs:\t0\r\r",
                                      foreground_color=tam_io.tam_colors.LIGHT_AQUA,
                                      background_color=tam_io.tam_colors.RED,
                                      bad_char="?")

        tam_tools.tam_print.tam_print(tam_buffer,
                                      12,
                                      9,
                                      text="High Score!\n1. Chad:\t4506\n2. Alia:\t4002\n3. Roy:\t3991",
                                      foreground_color=tam_io.tam_colors.DEFAULT,
                                      background_color=tam_io.tam_colors.DEFAULT)

        tam_tools.tam_print.tam_print(tam_buffer,
                                      12,
                                      16,
                                      text=EXAMPLE_STR,
                                      foreground_color=tam_io.tam_colors.GREEN,
                                      background_color=tam_io.tam_colors.GRAY)


def run():
    tam.tam_loop.TAMLoop(TAMPrint()).run()
