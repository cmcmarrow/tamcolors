from tamcolors import tam, tam_io, tam_tools


class TAMKeys(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char="+",
                         foreground_color=tam_io.tam_colors.WHITE,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=57, max_width=57, min_height=10, max_height=10)
        self._keys = None
        self._key_mode_cool_down = 0
        self._key_state_mode = False

    def update(self, tam_loop, keys, loop_data, *args):
        if tam_io.tam_keys.KEY_ENTER in keys and self._key_mode_cool_down == 0:
            self._key_state_mode = not tam_loop.is_key_state_mode_enabled()
            tam_loop.set_key_state_mode(self._key_state_mode)
            self._key_mode_cool_down = 5
        elif self._key_mode_cool_down != 0:
            self._key_mode_cool_down -= 1

        if len(keys) != 0:
            self._keys = keys[0]

        if tam_io.tam_keys.KEY_BACKSPACE in keys:
            tam_loop.done()

    def draw(self, tam_surface, loop_data, *args):
        if self._keys is not None:
            tam_surface.clear()
            key = self._keys[0]
            if self._keys[1] == tam_io.tam_keys.KEY_TYPE_WHITE_SPACE:
                key = str(ord(self._keys[0]))

            tam_tools.tam_print.tam_print(tam_surface,
                                          0,
                                          0,
                                          key,
                                          tam_io.tam_colors.WHITE,
                                          tam_io.tam_colors.BLACK)

            tam_tools.tam_print.tam_print(tam_surface,
                                          0,
                                          9,
                                          "Key State Mode: {}".format(self._key_state_mode),
                                          tam_io.tam_colors.AQUA,
                                          tam_io.tam_colors.BLACK)


def run():
    tam.tam_loop.TAMLoop(TAMKeys()).run()
