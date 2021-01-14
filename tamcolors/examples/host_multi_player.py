from tamcolors import tam, tam_io, tam_tools


class HostMultiPlayer(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char=" ",
                         foreground_color=tam_io.tam_colors.GREEN,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=50, max_width=50, min_height=25, max_height=25)
        self._at = [25, 12]
        self._key_manager = tam_tools.tam_key_manager.TAMKeyManager()

    def update(self, tam_loop, keys, loop_data):
        self._key_manager.update(keys)

        if self._key_manager.get_key_state("a"):
            self._at[0] += -1

        if self._key_manager.get_key_state("d"):
            self._at[0] += 1

        if self._key_manager.get_key_state("w"):
            self._at[1] += -1

        if self._key_manager.get_key_state("s"):
            self._at[1] += 1

        if self._key_manager.get_key_state("BACKSPACE"):
            tam_loop.done()

    def draw(self, tam_surface, loop_data):
        for w in range(tam_surface.get_dimensions()[0]):
            for h in range(tam_surface.get_dimensions()[1]):
                tam_surface.set_spot(w, h, " ", tam_io.tam_colors.GRAY, tam_io.tam_colors.GRAY)

        tam_surface.set_spot(*self._at, " ", tam_io.tam_colors.LIGHT_AQUA, tam_io.tam_colors.LIGHT_AQUA)


def run():
    tam.tam_loop.TAMLoop(HostMultiPlayer(), receivers=(tam.tam_loop_tcp_receiver.TAMLoopTCPReceiver(),)).run()
