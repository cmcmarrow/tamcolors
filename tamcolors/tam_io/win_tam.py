# built in libraries
import string
import sys

# tamcolors libraries
from .tam_buffer import TAMBuffer
from . import io_tam
from tamcolors.tam_c import _win_tam as io


"""
WinIO
draws out to windows terminal
gets ASCII key input from windows terminal
color mode 2
color mode 16
"""


class WinIOError(Exception):
    pass


class WinIO(io_tam.IO):
    def __init__(self):
        """
        info: makes WinIO object
        """
        super().__init__()
        self.__mode = 16
        self.__modes = {2: self._draw_2,
                        16: self._draw_16}
        self.__buffer = TAMBuffer(0, 0, " ", 1, 1)
        self.__last_frame = TAMBuffer(0, 0, " ", 1, 1)
        self.__windows_keys = self.get_key_dict()

    @classmethod
    def get_io(cls):
        """
        info: will see if environment supported by WinIO
        :return: WinIO object or None
        """
        if hasattr(cls, "win_io"):
            return cls.win_io
        if hasattr(io, "_init_default_color"):
            if io._init_default_color() == 1:
                cls.win_io = WinIO()
                return cls.win_io
        return None

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        self.__mode = mode

    def get_mode(self):
        """
        info: will return the current color mode
        :return: int
        """
        return self.__mode

    def get_modes(self):
        """
        info: will return a tuple of all color modes
        :return: (int, int, ...)
        """
        return tuple(self.__modes)

    def draw(self, tam_buffer):
        """
        info: will draw tam buffer to terminal
        :param tam_buffer: TAMBuffer
        :return:
        """
        if self.__buffer.get_dimensions() != io._get_dimension():
            self.clear()
            io._show_console_cursor(False)
            self.__buffer.set_dimensions_and_clear(*io._get_dimension())
            self.__last_frame = None

        self.__modes[self.__mode](tam_buffer)

    def _draw_2(self, tam_buffer):
        """
        info: will draw tam buffer to terminal in mode 2
        :param tam_buffer: TAMBuffer
        :return:
        """
        # checks if buffer needs to be updated
        if " " != self.__buffer.get_defaults()[0] or self.__buffer.get_defaults()[1:] != tam_buffer.get_defaults()[1:]:
            # buffer defaults changed
            self.__buffer.set_defaults_and_clear(" ", *tam_buffer.get_defaults()[1:])

        # draw onto WinIO buffer
        self._draw_onto(self.__buffer, tam_buffer)

        # draw WinIO buffer to terminal
        self._print(0, 0, "".join(self.__buffer.get_raw_buffers()[0]), *tam_buffer.get_defaults()[1:])

    def _draw_16(self, tam_buffer):
        """
        info: will draw tam buffer to terminal in mode 16
        :param tam_buffer: TAMBuffer
        :return:
        """
        # checks if buffer needs to be updated
        if "." != self.__buffer.get_defaults()[0] or self.__buffer.get_defaults()[2] != tam_buffer.get_defaults()[2]:
            # buffer defaults changed
            background = tam_buffer.get_defaults()[2]
            self.__buffer.set_defaults_and_clear(".", background, background)
            self.__last_frame = None

        # draw onto WinIO buffer
        self._draw_onto(self.__buffer, tam_buffer)

        """
        A block is a string or spots that 
        all share the same colors
        """
        start = None
        width = self.__buffer.get_dimensions()[0]
        length = 0
        this_foreground, this_background = None, None
        char_buffer, foreground_buffer, background_buffer = self.__buffer.get_raw_buffers()
        for spot, char, foreground, background in zip(range(len(self.__buffer)),
                                                      char_buffer,
                                                      foreground_buffer,
                                                      background_buffer):

            # no block has benn made
            if start is None:
                # last frame buffer is not None
                if self.__last_frame is not None:
                    # spot has not change
                    if (char, foreground, background) == self.__last_frame.get_from_raw_spot(spot):
                        continue
                # make block
                start = spot
                this_foreground, this_background = foreground, background
                length = 1
            # spot has same colors as block
            elif (this_foreground == foreground or " " == char) and this_background == background:
                # add to block
                length += 1
            # spot does not have same colors as block
            else:
                # draw block to terminal
                self._print(start % width,
                            start//width,
                            "".join(char_buffer[start:start + length]),
                            this_foreground, this_background)
                # start new block
                this_foreground, this_background = foreground, background
                start = spot
                length = 1
                # last frame buffer is not None
                if self.__last_frame is not None:
                    # spot has not change
                    if (char, foreground, background) == self.__last_frame.get_from_raw_spot(spot):
                        # remove new block
                        start = None
                        length = 0

        if start is not None:
            # draw last block
            self._print(start % width, start//width, "".join(char_buffer[start:start + length]),
                        this_foreground, this_background)

        # update last frame
        if self.__last_frame is None:
            # last frame is not made
            self.__last_frame = self.__buffer.copy()
        else:
            # draw tam_buffer onto last frame
            self._draw_onto(self.__last_frame, tam_buffer)

    def start(self):
        """
        info: will setup terminal to be used
        :return:
        """
        self.clear()
        io._show_console_cursor(False)

    def done(self):
        """
        info: will reset terminal
        :return:
        """
        self.__buffer = TAMBuffer(0, 0, " ", 1, 1)
        self.__last_frame = TAMBuffer(0, 0, " ", 1, 1)

        io._set_cursor_info(0, 0, io._get_default_color())
        self.clear()
        io._show_console_cursor(True)

    def get_key(self):
        """
        info: will get single key input or return False
        :return: str or False
        """
        key_bytes = []
        key_byte = io._get_key()
        while key_byte != -1:
            key_bytes.append(key_byte)
            key_byte = io._get_key()

        if len(key_bytes) != 0:
            return self.__windows_keys.get(";".join([str(key_byte) for key_byte in key_bytes]), False)

        return False

    def get_dimensions(self):
        return io._get_dimension()

    @staticmethod
    def get_key_dict():
        """
        info: makes a dict mapping key codes to key
        :return: dict
        """
        normal_key = string.digits + string.ascii_letters + "`-=[]\\;',./~!@#$%^&*()_+{}|:\"<>?"
        windows_keys = {str(ord(key)): (key, "NORMAL") for key in normal_key}

        for f_key in range(1, 10):
            windows_keys["0;{0}".format(58 + f_key)] = ("F{0}".format(f_key), "SPECIAL")
            windows_keys["0;{0}".format(83 + f_key)] = ("F{0}_SHIFT".format(f_key), "SPECIAL")

        code_224 = [[72, "UP"], [80, "DOWN"], [75, "LEFT"], [77, "RIGHT"], [83, "DELETE"],
                    [134, "F12"], [136, "F12_SHIFT"]]

        for code, key in code_224:
            windows_keys["224;{0}".format(code)] = (key, "SPECIAL")

        windows_keys["9"] = ("\t", "WHITESPACE")
        windows_keys["13"] = ("\n", "WHITESPACE")
        windows_keys["32"] = (" ", "WHITESPACE")

        windows_keys["8"] = ("BACKSPACE", "SPECIAL")
        windows_keys["27"] = ("ESCAPE", "SPECIAL")

        return windows_keys

    def printc(self, output, color):
        default_color = io._get_default_color()
        io._set_console_color((color[0] % 16) + (color[1] % 16) * 16)
        sys.stdout.write(output)
        sys.stdout.flush()
        io._set_console_color(default_color)

    def inputc(self, output, color):
        default_color = io._get_default_color()
        io._set_console_color((color[0] % 16) + (color[1] % 16)*16)
        ret = input(output)
        io._set_console_color(default_color)
        return ret

    def clear(self):
        """
        info: will clear the screen
        :return:
        """
        io._clear()

    @staticmethod
    def _print(x, y, output, foreground_color, background_color):
        """
        info: will print to terminal
        :param x: int
        :param y: int
        :param output: str
        :param foreground_color: int
        :param background_color: int
        :return:
        """
        io._set_cursor_info(x, y, (foreground_color % 16) + (background_color % 16)*16)
        sys.stdout.write(output)
        sys.stdout.flush()
