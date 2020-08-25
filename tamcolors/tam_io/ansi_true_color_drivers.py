from abc import ABC
from tamcolors.tam_io import tam_drivers
from .tam_buffer import TAMBuffer
import sys


class ANSITrueColorDriver(tam_drivers.ColorDriver, ABC):
    def __init__(self, *args, **kwargs):
        self.__buffer = TAMBuffer(0, 0, " ", 1, 1)
        self.__unix_keys = self.get_key_dict()

        self.__foreground_color_map = {-2: "39",
                                       -1: "39"}

        self.__background_color_map = {-2: "49",
                                       -1: "49"}
        super().__init__(*args, **kwargs)

    def printc(self, output, color, flush, stderr):
        """
        info: Will print to the console in color
        :param output: str
        :param color: COLOR
        :param flush: bool
        :param stderr: std
        :return:
        """
        foreground = self._process_rgb_color(color[0])
        background = self._process_rgb_color(color[1], False)
        output_str = "\u001b[{0};{1}m{2}\u001b[0m".format(foreground, background, output)
        self._write_to_output_stream(output_str, flush, stderr)

    def inputc(self, output, color):
        """
        info: Will get input from the console in color
        :param output: str
        :param color: COLOR
        :return: str
        """
        foreground = self._process_rgb_color(color[0])
        background = self._process_rgb_color(color[1], False)
        output_str = "\u001b[{0};{1}m{2}".format(foreground, background, output)
        ret = input(output_str)
        sys.stdout.write("\u001b[0m")
        sys.stdout.flush()
        return ret

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        super().set_mode(mode)

    def draw(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console
        :param tam_buffer: TAMBuffer
        :return: None
        """
        dimension = self.get_dimensions()
        if self.__buffer.get_dimensions() != dimension:
            self.clear()
            self.show_console_cursor(False)
            self.__buffer.set_dimensions_and_clear(*dimension)

        super().draw(tam_buffer)

    def _draw_2(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 2
        :param tam_buffer: TAMBuffer
        :return: None
        """
        # checks if buffer needs to be updated
        if " " != self.__buffer.get_defaults()[0] or self.__buffer.get_defaults()[1:] != tam_buffer.get_defaults()[1:]:
            # buffer defaults changed
            self.__buffer.set_defaults_and_clear(" ", *tam_buffer.get_defaults()[1:])

        # draw onto LinIO buffer
        self._draw_onto(self.__buffer, tam_buffer)

        color = self.__buffer.get_defaults()[1:]
        foreground = self._process_2_color(color[0])
        background = self._process_2_color(color[1], False)
        output = "".join(self.__buffer.get_raw_buffers()[0])
        sys.stdout.write("\u001b[1;1H\u001b[{0};{1}m{2}\u001b[0".format(foreground, background, output))
        sys.stdout.flush()

    def _draw_16(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 16
        :param tam_buffer: TAMBuffer
        :return: None
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
                foreground = self._process_16_color(foreground_buffer[spot])
                background = self._process_16_color(background_buffer[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_buffer[spot])
            elif foreground == foreground_buffer[spot] and background == background_buffer[spot]:
                output.append(char_buffer[spot])
            else:
                foreground = self._process_16_color(foreground_buffer[spot])
                background = self._process_16_color(background_buffer[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_buffer[spot])

        sys.stdout.write("".join(output) + "\u001b[0")
        sys.stdout.flush()

    def _draw_256(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 256
        :param tam_buffer: TAMBuffer
        :return: None
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
                foreground = self._process_256_color(foreground_buffer[spot])
                background = self._process_256_color(background_buffer[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_buffer[spot])
            elif foreground == foreground_buffer[spot] and background == background_buffer[spot]:
                output.append(char_buffer[spot])
            else:
                foreground = self._process_256_color(foreground_buffer[spot])
                background = self._process_256_color(background_buffer[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_buffer[spot])

        sys.stdout.write("".join(output) + "\u001b[0")
        sys.stdout.flush()

    def _draw_rgb(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode rgb
        :param tam_buffer: TAMBuffer
        :return: None
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
                foreground = self._process_rgb_color(foreground_buffer[spot])
                background = self._process_rgb_color(background_buffer[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_buffer[spot])
            elif foreground == foreground_buffer[spot] and background == background_buffer[spot]:
                output.append(char_buffer[spot])
            else:
                foreground = self._process_rgb_color(foreground_buffer[spot])
                background = self._process_rgb_color(background_buffer[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_buffer[spot])

        sys.stdout.write("".join(output) + "\u001b[0")
        sys.stdout.flush()

    def _process_2_color(self, color, foreground=True):
        rgb = self.get_color(color.mode_2)
        if foreground:
            if rgb.is_default or rgb.a == 0:
                return "39"
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            if rgb.is_default or rgb.a == 0:
                return "49"
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)

    def _process_16_color(self, color, foreground=True):
        rgb = self.get_color(color.mode_16)
        if foreground:
            if rgb.is_default or rgb.a == 0:
                return "39"
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            if rgb.is_default or rgb.a == 0:
                return "49"
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)

    def _process_256_color(self, color, foreground=True):
        rgb = self.get_color(color.mode_256)
        if foreground:
            if rgb.is_default or rgb.a == 0:
                return "39"
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            if rgb.is_default or rgb.a == 0:
                return "49"
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)

    def _process_rgb_color(self, color, foreground=True):
        rgb = color.mode_rgb
        if foreground:
            if rgb.is_default or rgb.a == 0:
                return "39"
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            if rgb.is_default or rgb.a == 0:
                return "49"
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)


class ANSITrueColorChangerDriver(tam_drivers.ColorChangerDriver, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _console_color_count(self):
        """
        info: Get console color
        :return: int
        """
        return 0
