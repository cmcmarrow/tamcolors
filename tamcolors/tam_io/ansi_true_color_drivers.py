from abc import ABC
from tamcolors.tam_io import tam_drivers
from .tam_surface import TAMSurface
from tamcolors.tam_io import io_tam
from tamcolors.tam_io import tam_colors
import sys


class ANSITrueFullColorDriver(tam_drivers.FullColorDriver, ABC):
    def __init__(self, *args, **kwargs):
        self._surface = TAMSurface(0, 0, " ", tam_colors.BLACK, tam_colors.BLACK)
        self._unix_keys = self.get_key_dict()
        super().__init__(*args, **kwargs)

    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        self._surface = TAMSurface(0, 0, " ", tam_colors.BLACK, tam_colors.BLACK)
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

    def get_printc_mode(self):
        """
        Gets the modes used by printc and inputc
        :return: str
        """
        return io_tam.MODE_RGB

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        super().set_mode(mode)

    def draw(self, tam_surface):
        """
        info: Will draw TAMSurface to console
        :param tam_surface: TAMSurface
        :return: None
        """
        dimension = self.get_dimensions()
        if self._surface.get_dimensions() != dimension:
            self.clear()
            self._surface.set_dimensions_and_clear(*dimension)

        super().draw(tam_surface)

    def _draw_2(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 2
        :param tam_surface: TAMSurface
        :return: None
        """
        # checks if surface needs to be updated
        if " " != self._surface.get_defaults()[0] or self._surface.get_defaults()[1:] != tam_surface.get_defaults()[1:]:
            # surface defaults changed
            self._surface.set_defaults_and_clear(" ", *tam_surface.get_defaults()[1:])

        # draw onto LinIO surface
        self._draw_onto(self._surface, tam_surface)

        color = self._surface.get_defaults()[1:]
        foreground = self._process_2_color(color[0])
        background = self._process_2_color(color[1], False)
        output = "".join(self._surface.get_raw_surface()[0])
        sys.stdout.write("\u001b[1;1H\u001b[{0};{1}m{2}\u001b[0".format(foreground, background, output))
        sys.stdout.flush()

    def _draw_16_pal_256(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 16_pal_256
        :param tam_surface: TAMSurface
        :return: None
        """
        self._draw(tam_surface, self._process_16_pal_256_color)

    def _draw_16(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 16
        :param tam_surface: TAMSurface
        :return: None
        """
        self._draw(tam_surface, self._process_16_color)

    def _draw_256(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode 256
        :param tam_surface: TAMSurface
        :return: None
        """
        self._draw(tam_surface, self._process_256_color)

    def _draw_rgb(self, tam_surface):
        """
        info: Will draw TAMSurface to console in mode rgb
        :param tam_surface: TAMSurface
        :return: None
        """
        self._draw(tam_surface, self._process_rgb_color)

    def _draw(self, tam_surface, process_func):
        """
        info: Will draw TAMSurface to console
        :param tam_surface: TAMSurface
        :param process_func: func
        :return: None
        """
        # checks if surface needs to be updated
        if " " != self._surface.get_defaults()[0] or self._surface.get_defaults()[1:] != tam_surface.get_defaults()[1:]:
            # surface defaults changed
            self._surface.set_defaults_and_clear(" ", *tam_surface.get_defaults()[1:])

        # draw onto LinIO surface
        self._draw_onto(self._surface, tam_surface)

        # make output string
        output = ["\u001b[1;1H"]
        foreground, background = None, None
        char_surface, foreground_surface, background_surface = self._surface.get_raw_surface()
        for spot in range(len(char_surface)):
            if foreground is None:
                foreground = process_func(foreground_surface[spot])
                background = process_func(background_surface[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_surface[spot])
            elif foreground == foreground_surface[spot] and background == background_surface[spot]:
                output.append(char_surface[spot])
            else:
                foreground = process_func(foreground_surface[spot])
                background = process_func(background_surface[spot], False)
                output.append("\u001b[{0};{1}m".format(foreground, background))
                output.append(char_surface[spot])

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
            rgb = self.get_color_2(color.mode_2)
        elif foreground:
            return "39"
        else:
            return "49"

        if foreground:
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)

    def _process_16_pal_256_color(self, color, foreground=True):
        """
        info process color to ansi
        :param color: COLOR
        :param foreground: bool
        :return: str
        """
        if color.mode_16 not in (-2, -1):
            rgb = tam_colors.COLORS[self.get_color_16_pal_256(color.mode_16_pal_256)].mode_rgb
        elif foreground:
            return "39"
        else:
            return "49"

        if foreground:
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)

    def _process_16_color(self, color, foreground=True):
        """
        info process color to ansi
        :param color: COLOR
        :param foreground: bool
        :return: str
        """
        if color.mode_16 not in (-2, -1):
            rgb = self.get_color_16(color.mode_16)
        elif foreground:
            return "39"
        else:
            return "49"

        if foreground:
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)

    def _process_256_color(self, color, foreground=True):
        """
        info process color to ansi
        :param color: COLOR
        :param foreground: bool
        :return: str
        """
        if color.mode_256 not in (-2, -1):
            rgb = self.get_color_256(color.mode_256)
        elif foreground:
            return "39"
        else:
            return "49"

        if foreground:
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)

    @staticmethod
    def _process_rgb_color(color, foreground=True):
        """
        info process color to ansi
        :param color: COLOR
        :param foreground: bool
        :return: str
        """
        rgb = color.mode_rgb
        if foreground:
            if rgb.is_default or rgb.a == 0:
                return "39"
            return "38;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)
        else:
            if rgb.is_default or rgb.a == 0:
                return "49"
            return "48;2;{};{};{}".format(rgb.r, rgb.g, rgb.b)

    def _console_color_count(self):
        """
        info: Get console color
        :return: int
        """
        return 0
