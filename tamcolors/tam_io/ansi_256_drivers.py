from abc import ABC
from tamcolors.tam_io import tam_drivers
from .tam_buffer import TAMBuffer
from tamcolors.tam_io import io_tam
from tamcolors.tam_io import tam_colors
import sys


class ANSI256ColorDriver(tam_drivers.FullColorDriver, ABC):
    def __init__(self, *args, **kwargs):
        self._buffer = TAMBuffer(0, 0, " ", tam_colors.BLACK, tam_colors.BLACK)
        self._unix_keys = self.get_key_dict()
        kwargs.setdefault("mode_rgb", False)
        super().__init__(*args, **kwargs)

    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        self._buffer = TAMBuffer(0, 0, " ", tam_colors.BLACK, tam_colors.BLACK)
        super().start()

    def printc(self, output, color, flush, stderr):
        """
        info: Will print to the console in color
        :param output: str
        :param color: COLOR
        :param flush: bool
        :param stderr: std
        :return:
        """
        foreground = self._process_256_color(color[0])
        background = self._process_256_color(color[1], False)
        output_str = "\u001b[{0};{1}m{2}\u001b[0m".format(foreground, background, output)
        self._write_to_output_stream(output_str, flush, stderr)

    def inputc(self, output, color):
        """
        info: Will get input from the console in color
        :param output: str
        :param color: COLOR
        :return: str
        """
        foreground = self._process_256_color(color[0])
        background = self._process_256_color(color[1], False)
        output_str = "\u001b[{0};{1}m{2}".format(foreground, background, output)
        ret = input(output_str)
        sys.stdout.write("\u001b[0m")
        sys.stdout.flush()
        return ret

    def get_printc_mode(self):
        """
        Gets the modes used by printc and inputc
        :return: str
        """
        return io_tam.MODE_256

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
        if self._buffer.get_dimensions() != dimension:
            self.clear()
            self._buffer.set_dimensions_and_clear(*dimension)

        super().draw(tam_buffer)

    def _draw_2(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 2
        :param tam_buffer: TAMBuffer
        :return: None
        """
        # checks if buffer needs to be updated
        if " " != self._buffer.get_defaults()[0] or self._buffer.get_defaults()[1:] != tam_buffer.get_defaults()[1:]:
            # buffer defaults changed
            self._buffer.set_defaults_and_clear(" ", *tam_buffer.get_defaults()[1:])

        # draw onto LinIO buffer
        self._draw_onto(self._buffer, tam_buffer)

        color = self._buffer.get_defaults()[1:]
        foreground = self._process_2_color(color[0])
        background = self._process_2_color(color[1], False)
        output = "".join(self._buffer.get_raw_buffers()[0])
        sys.stdout.write("\u001b[1;1H\u001b[{0};{1}m{2}\u001b[0".format(foreground, background, output))
        sys.stdout.flush()

    def _draw_16(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 16
        :param tam_buffer: TAMBuffer
        :return: None
        """
        self._draw(tam_buffer, self._process_16_color)

    def _draw_256(self, tam_buffer):
        """
        info: Will draw TAMBuffer to console in mode 256
        :param tam_buffer: TAMBuffer
        :return: None
        """
        self._draw(tam_buffer, self._process_256_color)

    def _draw(self, tam_buffer, process_func):
        """
        info: Will draw TAMBuffer to console
        :param tam_buffer: TAMBuffer
        :param process_func: func
        :return: None
        """
        # checks if buffer needs to be updated
        if " " != self._buffer.get_defaults()[0] or self._buffer.get_defaults()[1:] != tam_buffer.get_defaults()[1:]:
            # buffer defaults changed
            self._buffer.set_defaults_and_clear(" ", *tam_buffer.get_defaults()[1:])

        # draw onto LinIO buffer
        self._draw_onto(self._buffer, tam_buffer)

        # make output string
        output = ["\u001b[1;1H"]
        foreground, background = None, None
        char_buffer, foreground_buffer, background_buffer = self._buffer.get_raw_buffers()
        for spot in range(len(char_buffer)):
            if foreground is None:
                foreground = process_func(foreground_buffer[spot])
                background = process_func(background_buffer[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_buffer[spot])
            elif foreground == foreground_buffer[spot] and background == background_buffer[spot]:
                output.append(char_buffer[spot])
            else:
                foreground = process_func(foreground_buffer[spot])
                background = process_func(background_buffer[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_buffer[spot])

        sys.stdout.write("".join(output) + "\u001b[0")
        sys.stdout.flush()

    def _process_2_color(self, color, foreground=True):
        """
        info process color to ansi
        :param color: COLOR
        :param foreground: bool
        :return: str
        """
        if color.mode_2 not in (-2, -1):
            spot = color.mode_2
        elif foreground:
            return "39"
        else:
            return "49"

        if foreground:
            return "38;5;{}".format(spot)
        else:
            return "48;5;{}".format(spot)

    def _process_16_color(self, color, foreground=True):
        """
        info process color to ansi
        :param color: COLOR
        :param foreground: bool
        :return: str
        """
        if color.mode_16 not in (-2, -1):
            spot = color.mode_16
        elif foreground:
            return "39"
        else:
            return "49"

        if foreground:
            return "38;5;{}".format(spot)
        else:
            return "48;5;{}".format(spot)

    def _process_256_color(self, color, foreground=True):
        """
        info process color to ansi
        :param color: COLOR
        :param foreground: bool
        :return: str
        """
        if color.mode_256 not in (-2, -1):
            spot = color.mode_256
        elif foreground:
            return "39"
        else:
            return "49"

        if foreground:
            return "38;5;{}".format(spot)
        else:
            return "48;5;{}".format(spot)


class ANSI256ChangerDriver(tam_drivers.ColorChangerDriver, ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("color_changer_driver_operational", False)
        super().__init__(*args, **kwargs)

    def _console_color_count(self):
        """
        info: Get console color
        :return: int
        """
        return 0
