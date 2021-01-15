from random import choice
from tamcolors import tam, tam_io, tam_tools


class HostMultiPlayer(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char=" ",
                         foreground_color=tam_io.tam_colors.GREEN,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=50, max_width=50, min_height=26, max_height=26)

    def update(self, tam_loop, keys, loop_data, other_handlers, other_keys, other_data):
        def _update_handler(this_handler, this_keys, this_loop_data):
            if "at" not in this_loop_data:
                this_loop_data["at"] = [25, 13]
                this_loop_data["color"] = choice(tam_io.tam_colors.COLORS)
                this_loop_data["keys"] = tam_tools.tam_key_manager.TAMKeyManager()

            key_manager = this_loop_data["keys"]
            key_manager.update(this_keys)

            if key_manager.get_key_state("a"):
                this_loop_data["at"][0] += -1

            if key_manager.get_key_state("d"):
                this_loop_data["at"][0] += 1

            if key_manager.get_key_state("w"):
                this_loop_data["at"][1] += -1

            if key_manager.get_key_state("s"):
                this_loop_data["at"][1] += 1

            if key_manager.get_key_state("BACKSPACE"):
                this_handler.done()

        _update_handler(tam_loop, keys, loop_data)
        for other_handler in other_handlers:
            _update_handler(other_handlers[other_handler],
                            other_keys[other_handler],
                            other_data[other_handler])

    def draw(self, tam_surface, loop_data, other_surfaces, other_data):
        def _draw_handler(this_tam_surface, this_all_loop_data):
            for w in range(this_tam_surface.get_dimensions()[0]):
                for h in range(this_tam_surface.get_dimensions()[1]):
                    this_tam_surface.set_spot(w, h, " ", tam_io.tam_colors.GRAY, tam_io.tam_colors.GRAY)

            for this_loop_data in this_all_loop_data:
                this_tam_surface.set_spot(*this_loop_data["at"],
                                          " ",
                                          this_loop_data["color"],
                                          this_loop_data["color"])

        all_loop_data = [loop_data] + [other_data[other_handler] for other_handler in other_data]
        _draw_handler(tam_surface, all_loop_data)
        for other_handler in other_surfaces:
            _draw_handler(other_surfaces[other_handler], all_loop_data)


def run():
    tam.tam_loop.TAMLoop(HostMultiPlayer(), receivers=(tam.tam_loop_tcp_receiver.TAMLoopTCPReceiver(),)).run()
