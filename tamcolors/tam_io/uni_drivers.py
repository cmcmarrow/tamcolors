# built in libraries
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
        return io._get_dimensions()

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

