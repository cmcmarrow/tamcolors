# built in libraries
import string
import os
import sys
from abc import ABC

# tamcolors libraries
from tamcolors.tam_c import _uni_tam as io
from tamcolors.tam_io import tam_drivers


UNI_STABLE = io is not None


class UNISharedData(tam_drivers.TAMDriver, ABC):
    @classmethod
    def able_to_execute(cls):
        """
        info: checks that io is stable in current environment
        :return: bool
        """
        if UNI_STABLE:
            return os.system("test -t 0 -a -t 1 -a -t 2") == 0 and super().able_to_execute()
        return False


class UNIKeyDriver(tam_drivers.KeyDriver, UNISharedData, ABC):
    def __init__(self, *args, **kwargs):
        self._uni_keys = self.get_key_dict()
        super().__init__(*args, **kwargs)

    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
        """

        if not self.is_console_keys_enabled():
            return False

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

    def enable_console_keys(self, enable):
        """
        info: will enable console keys
        :param enable: boool
        :return: None
        """
        if enable:
            io._enable_get_key()
        else:
            io._disable_get_key()
        super().enable_console_keys(enable)


class UNIUtilitiesDriver(tam_drivers.UtilitiesDriver, UNISharedData, ABC):
    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
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
        super().clear()

    def show_console_cursor(self, show):
        """
        info: Will show or hide console cursor
        :param show: int
        :return: None
        """
        if show:
            sys.stdout.write("\u001b[?25h")
        else:
            sys.stdout.write("\u001b[?25l")
        super().show_console_cursor(show)

