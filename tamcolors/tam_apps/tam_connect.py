from tamcolors import tam, tam_tools, tam_io
from random import randint
from tamcolors.tam_tools import tam_print
from tamcolors.tam_io import tam_keys

from tamcolors.utils.tcp import TCPConnection
from tamcolors.tam_io.tcp_io import run_tcp_connection


HIT_ACTION_LETTER = "Enter character to run action!"


class BootTAMConnect(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char=" ",
                         foreground_color=tam_io.tam_colors.GREEN,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=57, max_width=57, min_height=10, max_height=10)

        self._icon = None
        self._wait = None
        self._tam_connect = TAMConnect()
        self.rest_frame()

    def update(self, tam_loop, keys, loop_data, *args):

        if not self._icon.done():
            self._icon.slide()
        else:
            self._wait -= 1

        if self._wait == 0 or len(keys):
            self.rest_frame()
            tam_loop.add_frame_stack(self._tam_connect)

    def draw(self, tam_surface, loop_data, *args):
        tam_surface.clear()

        tam_surface.draw_onto(self._icon.peak(), 0, 0)

    def rest_frame(self):
        self._icon = tam_tools.tam_fade.tam_fade_in(surface=tam_tools.tam_icon.get_icon(),
                                                    char=" ",
                                                    foreground_color=tam_io.tam_colors.BLACK,
                                                    background_color=tam_io.tam_colors.BLACK)
        self._wait = 10


class TAMConnect(tam.tam_loop.TAMFrame):
    def __init__(self):
        super().__init__(fps=10,
                         char=" ",
                         foreground_color=tam_io.tam_colors.GREEN,
                         background_color=tam_io.tam_colors.BLACK,
                         min_width=0, max_width=2000, min_height=0, max_height=1000)

        self._in = None
        self._action_keys = set(list("IP6NCQ"))

        self._ip = "127.0.0.1"
        self._port = "4444"
        self._ipv6 = False
        self._name = hex(randint(0, 10000000))[2:].upper()

        self._message = HIT_ACTION_LETTER
        self._error = False

    def update(self, tam_loop, keys, loop_data, *args):
        for key in keys:
            if self._in is None:
                if key == tam_keys.KEY_BACKSPACE:
                    tam_loop.pop_frame_stack()
                    break
                elif key in (tam_keys.KEY_Q, tam_keys.KEY_q):
                    tam_loop.done()
                    break
                elif key in (tam_keys.KEY_C, tam_keys.KEY_c):
                    try:
                        tam_loop.freeze_handler()
                        run_tcp_connection(TCPConnection(user_name=self._name,
                                                         ipv6=self._ipv6,
                                                         host=self._ip,
                                                         port=int(self._port)))
                    except Exception as error:
                        self._error = True
                        self._message = str(error)
                    finally:
                        tam_loop.unfreeze_handler()
                    break
                elif key == tam_keys.KEY_6:
                    self._ipv6 = not self._ipv6
                elif key in (tam_keys.KEY_I, tam_keys.KEY_i):
                    self._in = "I"
                    self._error = False
                    self._message = "Enter connections IP."
                elif key in (tam_keys.KEY_P, tam_keys.KEY_p):
                    self._in = "P"
                    self._error = False
                    self._message = "Enter connections port."
                elif key in (tam_keys.KEY_N, tam_keys.KEY_n):
                    self._in = "N"
                    self._error = False
                    self._message = "Enter Your name."
            elif key == tam_keys.KEY_ENTER:
                self._in = None
                self._error = False
                self._message = HIT_ACTION_LETTER
            elif self._in == "I":
                if key == tam_keys.KEY_BACKSPACE and self._ip:
                    self._ip = self._ip[:-1]
                elif key[1] == tam_keys.KEY_TYPE_NORMAL and len(self._ip) != 45:
                    self._ip += key[0]
            elif self._in == "P":
                if key == tam_keys.KEY_BACKSPACE and self._port:
                    self._port = self._port[:-1]
                elif key[1] == tam_keys.KEY_TYPE_NORMAL and len(self._port) != 45:
                    self._port += key[0]
            elif self._in == "N":
                if key == tam_keys.KEY_BACKSPACE and self._name:
                    self._name = self._name[:-1]
                elif key[1] == tam_keys.KEY_TYPE_NORMAL and len(self._name) != 45:
                    self._name += key[0]

    def draw(self, tam_surface, loop_data, *args):
        tam_surface.clear()
        tam_print.tam_print(tam_surface, 0, 0, "tam connect",
                            tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.ALPHA)
        tam_print.tam_print(tam_surface, 0, 1, "I: ip: " + self._ip,
                            tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.ALPHA)
        tam_print.tam_print(tam_surface, 0, 2, "P: port: " + self._port,
                            tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.ALPHA)
        tam_print.tam_print(tam_surface, 0, 3, "6: ipv6: " + str(self._ipv6),
                            tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.ALPHA)
        tam_print.tam_print(tam_surface, 0, 4, "N: name: " + self._name,
                            tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.ALPHA)
        tam_print.tam_print(tam_surface, 0, 5, "C: connect",
                            tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.ALPHA)
        tam_print.tam_print(tam_surface, 0, 6, "Q: quit",
                            tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.ALPHA)
        if self._error:
            tam_print.tam_print(tam_surface, 0, 7, self._message,
                                tam_io.tam_colors.LIGHT_RED, tam_io.tam_colors.ALPHA)
        else:
            tam_print.tam_print(tam_surface, 0, 7, self._message,
                                tam_io.tam_colors.LIGHT_GREEN, tam_io.tam_colors.ALPHA)


def run_app():
    tam.tam_loop.TAMLoop.run_application(BootTAMConnect())


if __name__ == "__main__":
    run_app()
