from tamcolors import tam, tam_tools, tam_io


class TAMKeyManager(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char="@",
                         foreground_color=tam_io.tam_colors.GRAY,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=70, max_width=70, min_height=40, max_height=40)

        self._key_manager = tam_tools.tam_key_manager.TAMKeyManager()
        self._output = ""
        self._keyboard_name = ""

    def update(self, tam_loop, keys, loop_data):
        self._key_manager.update(keys)

        if len(self._output) >= 20:
            self._output = ""

        if self._key_manager.get_key_state("a"):
            self._output += "a"

        if self._key_manager.get_key_state("b"):
            self._output += "b"

        if self._key_manager.get_key_state("c"):
            self._output += "c"

        if self._key_manager.get_key_state("BACKSPACE"):
            tam_loop.done()

        self._keyboard_name = tam_loop.get_keyboard_name()

    def draw(self, tam_surface, loop_data):
        tam_surface.clear()

        tam_tools.tam_print.tam_print(tam_surface,
                                      0,
                                      0,
                                      text=self._output,
                                      foreground_color=tam_io.tam_colors.LIGHT_GREEN,
                                      background_color=tam_io.tam_colors.ALPHA)

        tam_tools.tam_print.tam_print(tam_surface,
                                      0,
                                      30,
                                      text="Try a, b and c.\nbackspace to quit.",
                                      foreground_color=tam_io.tam_colors.RED,
                                      background_color=tam_io.tam_colors.ALPHA)

        tam_tools.tam_print.tam_print(tam_surface,
                                      0,
                                      32,
                                      text=self._keyboard_name,
                                      foreground_color=tam_io.tam_colors.LIGHT_BLUE,
                                      background_color=tam_io.tam_colors.ALPHA)


def run():
    tam.tam_loop.TAMLoop(TAMKeyManager()).run()
