# built in libraries
import platform
import string
import sys
import os
from abc import ABC

# tamcolors libraries
from .tam_buffer import TAMBuffer
from tamcolors.tam_c import _uni_tam as io
from tamcolors.tam_io import tam_drivers


"""
UniIO
draws out to Unix terminal
gets ASCII key input from linux terminal
color mode 2
color mode 16
"""


class UniIOError(Exception):
    pass


class UniIO():
    def __init__(self):
        """
        info: makes UniIO object
        """
        self.__buffer = TAMBuffer(0, 0, " ", 1, 1)
        self.__unix_keys = self.get_key_dict()

        self.__foreground_color_map = {-2: "39",
                                       -1: "39"}

        self.__background_color_map = {-2: "49",
                                       -1: "49"}
        super().__init__()
        self.set_tam_color_defaults()

    def draw(self, tam_buffer):
        """
        info: will draw tam buffer to terminal
        :param tam_buffer: TAMBuffer
        :return:
        """

        dimension = io._get_dimension()
        if self.__buffer.get_dimensions() != dimension:
            self.clear()
            self._show_console_cursor(False)
            io._enable_get_key()
            self.__buffer.set_dimensions_and_clear(*dimension)

        super().draw(tam_buffer)

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

        # draw onto LinIO buffer
        self._draw_onto(self.__buffer, tam_buffer)

        color = self._get_lin_tam_color(*self.__buffer.get_defaults()[1:])
        output = "".join(self.__buffer.get_raw_buffers()[0])
        sys.stdout.write("\u001b[1;1H\u001b[{0};{1}m{2}\u001b[0".format(*color, output))
        sys.stdout.flush()

    def _draw_16(self, tam_buffer):
        """
        info: will draw tam buffer to terminal in mode 16
        :param tam_buffer: TAMBuffer
        :return:
        """
        # checks if buffer needs to be updated
        if " " != self.__buffer.get_defaults()[0] or self.__buffer.get_defaults()[1:] != tam_buffer.get_defaults()[1:]:
            # buffer defaults changed
            self.__buffer.set_defaults_and_clear(" ", *tam_buffer.get_defaults()[1:])

        # draw onto LinIO buffer
        self._draw_onto(self.__buffer, tam_buffer)

        # make output string
        output = ["\u001b[1;1H"]
        foreground, background = None, None
        char_buffer, foreground_buffer, background_buffer = self.__buffer.get_raw_buffers()
        for spot in range(len(char_buffer)):
            if foreground is None:
                foreground = foreground_buffer[spot]
                background = background_buffer[spot]
                output.append("\u001b[{0};{1}m".format(*self._get_lin_tam_color(foreground, background)))
                output.append(char_buffer[spot])
            elif foreground == foreground_buffer[spot] and background == background_buffer[spot]:
                output.append(char_buffer[spot])
            else:
                foreground = foreground_buffer[spot]
                background = background_buffer[spot]
                output.append("\u001b[{0};{1}m".format(*self._get_lin_tam_color(foreground, background)))
                output.append(char_buffer[spot])

        sys.stdout.write("".join(output) + "\u001b[0")
        sys.stdout.flush()

    def set_color(self, spot, color):
        """
        info: sets a color value
        :param spot: int: 0 - 15
        :param color: tuple: (int, int, int)
        :return: None
        """
        self.__foreground_color_map[spot] = "38;2;{};{};{}".format(*color)
        self.__background_color_map[spot] = "48;2;{};{};{}".format(*color)
        super().set_color(spot, color)

    def get_color(self, spot):
        """
        info: will get the color value
        :param spot: int
        :return: tuple: (int, int, int)
        """
        return self._colors[spot]

    def _get_lin_tam_color(self, foreground_color, background_color):
        """
        info: will get the ANI color code
        :param foreground_color: int
        :param background_color: int
        :return: (str, sr)
        """
        return self.__foreground_color_map.get(foreground_color),\
               self.__background_color_map.get(background_color)

    def printc(self, output, color, flush, stderr):
        """
        info: will print out user output with color
        :param output: str
        :param color: tuple: (int, int)
        :param flush: boolean
        :param stderr: boolean
        :return: None
        """
        output_str = "\u001b[{0};{1}m{2}\u001b[0m".format(*self._get_lin_tam_color(*color), output)
        self._write_to_output_stream(output_str, flush, stderr)

    def inputc(self, output, color):
        """
        info: will get user input with color
        :param output: str
        :param color: tuple: (int, int)
        :return: str
        """
        output_str = "\u001b[{0};{1}m{2}".format(*self._get_lin_tam_color(*color), output)
        ret = input(output_str)
        sys.stdout.write("\u001b[0m")
        sys.stdout.flush()
        return ret


class UNISharedData(tam_drivers.TAMDriver, ABC):
    @classmethod
    def able_to_execute(cls):
        """
        info: checks that io is stable in current environment
        :return: bool
        """
        if platform.system() in ("Darwin", "Linux") and io is not None:
            return os.system("test -t 0 -a -t 1 -a -t 2") == 0
        return False


class UNIKeyDriver(tam_drivers.KeyDriver, UNISharedData, ABC):
    def __init__(self, *args, **kwargs):
        self._uni_keys = self.get_key_dict()
        super().__init__(*args, **kwargs)

    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        super().start()
        io._enable_get_key()

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        super().done()
        io._disable_get_key()

    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
        """
        key_bytes = []
        key_byte = io._get_key()
        while key_byte != -1:
            key_bytes.append(key_byte)
            key_byte = io._get_key()

        if len(key_bytes) != 0:
            return self._uni_keys.get(";".join([str(key_byte) for key_byte in key_bytes]), False)

        return False

    @staticmethod
    def get_key_dict():
        """
        info: Gets a dict of all the keys
        :return: {str: (str, str), ...}
        """
        normal_key = string.digits + string.ascii_letters + "`-=[]\\;',./~!@#$%^&*()_+{}|:\"<>?"
        linux_keys = {str(ord(key)): (key, "NORMAL") for key in normal_key}

        code_27_91 = [[65, "UP"], [66, "DOWN"], [68, "LEFT"], [67, "RIGHT"]]

        for code, key in code_27_91:
            linux_keys["27;91;{0}".format(code)] = (key, "SPECIAL")

        for f_key in range(0, 4):
            linux_keys["27;79;{0}".format(f_key + 80)] = ("F{0}".format(f_key + 1), "SPECIAL")
            linux_keys["27;91;49;59;50;{0}".format(f_key + 80)] = ("F{0}_SHIFT".format(f_key + 1), "SPECIAL")

        linux_keys["27;91;49;53;126"] = ("F5", "SPECIAL")
        linux_keys["27;91;49;53;59;50;126"] = ("F5_SHIFT", "SPECIAL")

        linux_keys["27;91;49;55;126"] = ("F6", "SPECIAL")
        linux_keys["27;91;49;55;59;50;126"] = ("F6_SHIFT", "SPECIAL")

        linux_keys["27;91;49;56;126"] = ("F7", "SPECIAL")
        linux_keys["27;91;49;56;59;50;126"] = ("F7_SHIFT", "SPECIAL")

        linux_keys["27;91;49;57;126"] = ("F8", "SPECIAL")
        linux_keys["27;91;49;57;59;50;126"] = ("F8_SHIFT", "SPECIAL")

        linux_keys["27;91;50;48;126"] = ("F9", "SPECIAL")
        linux_keys["27;91;50;48;59;50;126"] = ("F9_SHIFT", "SPECIAL")

        linux_keys["27;91;50;52;126"] = ("F12", "SPECIAL")
        linux_keys["27;91;50;52;59;50;126"] = ("F12_SHIFT", "SPECIAL")

        linux_keys["27;91;51;126"] = ("DELETE", "SPECIAL")

        linux_keys["9"] = ("\t", "WHITESPACE")
        linux_keys["10"] = ("\n", "WHITESPACE")
        linux_keys["32"] = (" ", "WHITESPACE")

        linux_keys["127"] = ("BACKSPACE", "SPECIAL")
        linux_keys["27"] = ("ESCAPE", "SPECIAL")

        return linux_keys


class UNIUtilitiesDriver(tam_drivers.UtilitiesDriver, UNISharedData, ABC):
    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        self.clear()
        self.show_console_cursor(False)
        super().start()

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        self.clear()
        self.show_console_cursor(True)
        os.system("clear")
        super().done()

    def get_dimensions(self):
        """
        info: Gets the dimensions of console
        :return: (int, int): (row, column)
        """
        return io._get_dimension()

    def clear(self):
        """
        info: Will clear the console
        :return: None
        """
        os.system("tput reset")

    def show_console_cursor(self, show):
        """
        info: Will show or hide console cursor
        :param show: int
        :return: None
        """
        if platform.system() != "Darwin":
            if show:
                os.system("setterm -cursor on")
            else:
                os.system("setterm -cursor off")
