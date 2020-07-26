from tamcolors import tam, tam_tools, tam_io


class TAMPrint(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char="+",
                         foreground_color=tam_io.tam_colors.GRAY,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=70, max_width=70, min_height=40, max_height=40)

        self._box_1 = tam_tools.tam_text_box.TAMTextBox("Hello!\nThis is a text box!",
                                                        23,
                                                        6,
                                                        "#",
                                                        tam_io.tam_colors.LIGHT_AQUA,
                                                        tam_io.tam_colors.GRAY,
                                                        center_horizontal=True)
        self._box_2 = tam_tools.tam_text_box.TAMTextBox("Hello!\nThis is a text box!",
                                                        26,
                                                        9,
                                                        "@",
                                                        tam_io.tam_colors.RED,
                                                        tam_io.tam_colors.WHITE,
                                                        clock=1,
                                                        center_horizontal=True,
                                                        center_vertical=True,
                                                        char_background="-")

        self._box_3 = tam_tools.tam_text_box.TAMTextBox("tamcolors",
                                                        23,
                                                        5,
                                                        "+",
                                                        tam_io.tam_colors.BLACK,
                                                        tam_io.tam_colors.RED,
                                                        clock=1,
                                                        center_horizontal=False,
                                                        center_vertical=True,
                                                        char_background="0")

    def update(self, tam_loop, keys, loop_data):
        if keys:
            tam_loop.done()

        if self._box_2.done():
            self._box_2 = tam_tools.tam_text_box.TAMTextBox("Hello!\nThis is a text box!",
                                                            26,
                                                            9,
                                                            "@",
                                                            tam_io.tam_colors.RED,
                                                            tam_io.tam_colors.WHITE,
                                                            clock=1,
                                                            center_horizontal=True,
                                                            center_vertical=True,
                                                            char_background="-")

        self._box_1.update()
        self._box_2.update()
        self._box_3.update()

    def draw(self, tam_buffer, loop_data):
        tam_buffer.clear()

        self._box_1.draw(tam_buffer, 0, 0)
        self._box_2.draw(tam_buffer, 5, 10)
        self._box_3.draw(tam_buffer, 12, 30)


def run():
    tam.tam_loop.TAMLoop(TAMPrint()).run()
