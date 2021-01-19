# built in libraries
import string
from abc import ABC
from threading import Lock
from itertools import cycle


# tamcolors libraries
from .tam_surface import TAMSurface
from tamcolors.tam_c import _win_tam as io
from tamcolors.tam_io import tam_drivers
from tamcolors.tam_io import tam_colors
from tamcolors.tam_io import io_tam, tam_keys


WIN_STABLE = False
if io is not None:
    WIN_STABLE = io._has_vaild_win_console()
    if WIN_STABLE:
        io._init_default_color()


class WinSharedData(tam_drivers.TAMDriver, ABC):
    @classmethod
    def able_to_execute(cls):
        """
        info: checks that io is stable in current environment
        :return: bool
        """
        return WIN_STABLE and super().able_to_execute()


class WINKeyDriver(tam_drivers.KeyDriver, WinSharedData, ABC):
    def __init__(self, *args, **kwargs):
        self._windows_keyboard = tam_keys.KEYBOARD_US_ENGLISH(*tam_keys.Keyboard.split_code_dict(self.get_key_dict()))
        self._keys = cycle(self._windows_keyboard.get_key_list())
        self._key_count = len(self._windows_keyboard.get_key_list())

        super().__init__(*args, **kwargs)

    def get_key(self):
        """
        info: will get single key input or return False
        :return: str or False
        """
        if not self.is_console_keys_enabled():
            return False
        elif self.is_key_state_mode_enabled():
            for _ in range(self._key_count):
                key = next(self._keys)
                key_code = key[2]
                if key_code is not None:
                    if io._get_key_state(key_code):
                        return key[0]
        else:
            key_bytes = []
            key_byte = io._get_key()
            while key_byte != -1:
                key_bytes.append(key_byte)
                key_byte = io._get_key()

            if len(key_bytes) != 0:
                return self._windows_keyboard.code_to_key(tuple(key_bytes))
        return False

    def get_key_dict(self, language=None):
        """
        info: Gets a dict of all the keys
        :param language: str or None
        :return: dict
        """

        if language is None:
            language = self.get_keyboard_name()

        if language == tam_keys.LANGUAGE_US_ENGLISH:
            return {tam_keys.KEY_ESCAPE: ((27,), 0),
                    tam_keys.KEY_F1: ((0, 59), 0),
                    tam_keys.KEY_F1_SHIFT: ((0, 84), 0),
                    tam_keys.KEY_F2: ((0, 60), 0),
                    tam_keys.KEY_F2_SHIFT: ((0, 85), 0),
                    tam_keys.KEY_F3: ((0, 61), 0),
                    tam_keys.KEY_F3_SHIFT: ((0, 86), 0),
                    tam_keys.KEY_F4: ((0, 62), 0),
                    tam_keys.KEY_F4_SHIFT: ((0, 87), 0),
                    tam_keys.KEY_F5: ((0, 63), 0),
                    tam_keys.KEY_F5_SHIFT: ((0, 88), 0),
                    tam_keys.KEY_F6: ((0, 64), 0),
                    tam_keys.KEY_F6_SHIFT: ((0, 89), 0),
                    tam_keys.KEY_F7: ((0, 65), 0),
                    tam_keys.KEY_F7_SHIFT: ((0, 90), 0),
                    tam_keys.KEY_F8: ((0, 66), 0),
                    tam_keys.KEY_F8_SHIFT: ((0, 91), 0),
                    tam_keys.KEY_F9: ((0, 67), 0),
                    tam_keys.KEY_F9_SHIFT: ((0, 92), 0),
                    tam_keys.KEY_F12: ((224, 134), 0),
                    tam_keys.KEY_F12_SHIFT: ((224, 136), 0),
                    tam_keys.KEY_BACKTICK: ((97,), 0),
                    tam_keys.KEY_TILDE: ((126,), 0),
                    tam_keys.KEY_1: ((49,), 0),
                    tam_keys.KEY_EXCLAMATION_MART: ((33,), 0),
                    tam_keys.KEY_2: ((50,), 0),
                    tam_keys.KEY_AT_SIGN: ((64,), 0),
                    tam_keys.KEY_3: ((51,), 0),
                    tam_keys.KEY_POUND_SIGN: ((35,), 0),
                    tam_keys.KEY_4: ((52,), 0),
                    tam_keys.KEY_DOLLAR_SYMBOL: ((36,), 0),
                    tam_keys.KEY_5: ((53,), 0),
                    tam_keys.KEY_PERCENT_SIGN: ((37,), 0),
                    tam_keys.KEY_6: ((54,), 0),
                    tam_keys.KEY_CARET: ((94,), 0),
                    tam_keys.KEY_7: ((55,), 0),
                    tam_keys.KEY_AMPERSAND: ((38,), 0),
                    tam_keys.KEY_8: ((56,), 0),
                    tam_keys.KEY_ASTERISK: ((42,), 0),
                    tam_keys.KEY_9: ((57,), 0),
                    tam_keys.KEY_LEFT_PARENTHESIS: ((40,), 0),
                    tam_keys.KEY_0: ((48,), 0),
                    tam_keys.KEY_RIGHT_PARENTHESIS: ((41,), 0),
                    tam_keys.KEY_HYPHEN: ((45,), 0),
                    tam_keys.KEY_UNDERSCORE: ((95,), 0),
                    tam_keys.KEY_EQUAL_SIGN: ((61,), 0),
                    tam_keys.KEY_PLUS_SIGN: ((43,), 0),
                    tam_keys.KEY_BACKSPACE: ((8,), 8),
                    tam_keys.KEY_TAB: ((9,), 0),
                    tam_keys.KEY_q: ((113,), None),
                    tam_keys.KEY_Q: ((81,), 81),
                    tam_keys.KEY_w: ((119,), None),
                    tam_keys.KEY_W: ((87,), 87),
                    tam_keys.KEY_e: ((101,), None),
                    tam_keys.KEY_E: ((69,), 69),
                    tam_keys.KEY_r: ((114,), None),
                    tam_keys.KEY_R: ((82,), 82),
                    tam_keys.KEY_t: ((116,), None),
                    tam_keys.KEY_T: ((84,), 84),
                    tam_keys.KEY_y: ((121,), None),
                    tam_keys.KEY_Y: ((89,), 89),
                    tam_keys.KEY_u: ((117,), None),
                    tam_keys.KEY_U: ((85,), 85),
                    tam_keys.KEY_i: ((105,), None),
                    tam_keys.KEY_I: ((73,), 73),
                    tam_keys.KEY_o: ((111,), None),
                    tam_keys.KEY_O: ((73,), 73),
                    tam_keys.KEY_p: ((112,), None),
                    tam_keys.KEY_P: ((80,), 80),
                    tam_keys.KEY_LEFT_SQUARE_BRACKET: ((91,), 0),
                    tam_keys.KEY_LEFT_CURLY_BRACKET: ((123,), 0),
                    tam_keys.KEY_RIGHT_SQUARE_BRACKET: ((93,), 0),
                    tam_keys.KEY_RIGHT_CURLY_BRACKET: ((125,), 0),
                    tam_keys.KEY_BACKSLASH: ((92,), 0),
                    tam_keys.KEY_VERTICAL_BAR: ((124,), 0),
                    tam_keys.KEY_DELETE: ((224, 83), 0),
                    tam_keys.KEY_a: ((97,), None),
                    tam_keys.KEY_A: ((65,), 65),
                    tam_keys.KEY_s: ((115,), None),
                    tam_keys.KEY_S: ((83,), 83),
                    tam_keys.KEY_d: ((100,), None),
                    tam_keys.KEY_D: ((68,), 68),
                    tam_keys.KEY_f: ((102,), None),
                    tam_keys.KEY_F: ((70,), 70),
                    tam_keys.KEY_g: ((103,), None),
                    tam_keys.KEY_G: ((71,), 71),
                    tam_keys.KEY_h: ((104,), None),
                    tam_keys.KEY_H: ((72,), 72),
                    tam_keys.KEY_j: ((106,), None),
                    tam_keys.KEY_J: ((74,), 74),
                    tam_keys.KEY_k: ((107,), None),
                    tam_keys.KEY_K: ((75,), 75),
                    tam_keys.KEY_l: ((108,), None),
                    tam_keys.KEY_L: ((76,), 76),
                    tam_keys.KEY_SEMICOLON: ((59,), 0),
                    tam_keys.KEY_COLON: ((58,), 0),
                    tam_keys.KEY_APOSTROPHE: ((39,), 0),
                    tam_keys.KEY_QUOTATION_MARK: ((34,), 0),
                    tam_keys.KEY_ENTER: ((13,), 13),
                    tam_keys.KEY_z: ((122,), 0),
                    tam_keys.KEY_Z: ((90,), 0),
                    tam_keys.KEY_x: ((120,), 0),
                    tam_keys.KEY_X: ((88,), 0),
                    tam_keys.KEY_c: ((99,), 0),
                    tam_keys.KEY_C: ((67,), 0),
                    tam_keys.KEY_v: ((118,), 0),
                    tam_keys.KEY_V: ((86,), 0),
                    tam_keys.KEY_b: ((98,), 0),
                    tam_keys.KEY_B: ((66,), 0),
                    tam_keys.KEY_n: ((110,), 0),
                    tam_keys.KEY_N: ((78,), 0),
                    tam_keys.KEY_m: ((109,), 0),
                    tam_keys.KEY_M: ((77,), 0),
                    tam_keys.KEY_COMMA: ((44,), 0),
                    tam_keys.KEY_LEFT_ANGLE_BRACKET: ((60,), 0),
                    tam_keys.KEY_PERIOD: ((46,), 0),
                    tam_keys.KEY_RIGHT_ANGLE_BRACKET: ((62,), 0),
                    tam_keys.KEY_SLASH: ((47,), 0),
                    tam_keys.KEY_QUESTION_MARK: ((63,), 0),
                    tam_keys.KEY_UP: ((224, 72), 0),
                    tam_keys.KEY_SPACE: ((32,), 0),
                    tam_keys.KEY_LEFT: ((224, 75), 0),
                    tam_keys.KEY_DOWN: ((224, 80), 0),
                    tam_keys.KEY_RIGHT: ((224, 77), 0)}
        return {}

    def get_keyboard_name(self, default_to_us_english=True):
        """
        info: Will get the keyboard language name
        :param default_to_us_english: bool
        :return: str
        """
        name = io._get_keyboard_name()
        if default_to_us_english and name == tam_keys.LANGUAGE_UNKNOWN:
            return tam_keys.LANGUAGE_US_ENGLISH
        return name


class WINFullColorDriver(tam_drivers.FullColorDriver, WinSharedData, ABC):
    def __init__(self, *args, **kwargs):
        self._surface = TAMSurface(0, 0, " ", tam_colors.BLACK, tam_colors.BLACK)
        self._last_frame = TAMSurface(0, 0, " ", tam_colors.BLACK, tam_colors.BLACK)
        self._last_frame_lock = Lock()
        self._spot_swap_dict = {1: 4,
                                3: 6,
                                4: 1,
                                6: 3,
                                9: 12,
                                11: 14,
                                12: 9,
                                14: 11}

        kwargs.setdefault("mode_256", False)
        kwargs.setdefault("mode_rgb", False)

        super().__init__(*args, **kwargs)

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        self._surface = TAMSurface(0, 0, " ", tam_colors.BLACK, tam_colors.BLACK)
        self._last_frame = TAMSurface(0, 0, " ", tam_colors.BLACK, tam_colors.BLACK)
        io._set_cursor_info(0, 0, io._get_default_color())
        super().done()

    def printc(self, output, color, flush, stderr):
        """
        info: will print out user output with color
        :param output: str
        :param color: tuple: (int, int)
        :param flush: boolean
        :param stderr: boolean
        :return: None
        """
        default_color = io._get_default_color()
        color = self._spot_swap(color[0].mode_16), self._spot_swap(color[1].mode_16)
        color = self._processes_special_color(*color)
        io._set_console_color((color[0] % 16) + (color[1] % 16) * 16)
        self._write_to_output_stream(output, flush, stderr)
        io._set_console_color(default_color)

    def inputc(self, output, color):
        """
        info: will get user input with color
        :param output: str
        :param color: tuple: (int, int)
        :return: str
        """
        default_color = io._get_default_color()
        color = self._spot_swap(color[0].mode_16), self._spot_swap(color[1].mode_16)
        color = self._processes_special_color(*color)
        io._set_console_color((color[0] % 16) + (color[1] % 16) * 16)
        ret = input(output)
        io._set_console_color(default_color)
        return ret

    def get_printc_mode(self):
        """
        Gets the modes used by printc and inputc
        :return: str
        """
        return io_tam.MODE_16

    def set_mode(self, mode):
        """
        info: will set the color mode
        :param mode: int: key to color mode
        :return:
        """
        try:
            self._last_frame_lock.acquire()
            self._last_frame = None
        finally:
            self._last_frame_lock.release()
        super().set_mode(mode)

    def draw(self, tam_surface):
        """
        info: will draw tam surface to terminal
        :param tam_surface: TAMSurface
        :return:
        """
        if self._surface.get_dimensions() != io._get_dimensions():
            self.clear()
            self._surface.set_dimensions_and_clear(*io._get_dimensions())
            self._last_frame = None

        super().draw(tam_surface)

    def _draw_2(self, tam_surface):
        """
        info: will draw tam surface to terminal in mode 2
        :param tam_surface: TAMSurface
        :return:
        """
        foreground, background = tam_surface.get_defaults()[1:]
        foreground, background = foreground.mode_2, background.mode_2

        # checks if surface needs to be updated
        if " " != self._surface.get_defaults()[0] or self._surface.get_defaults()[1:] != tam_surface.get_defaults()[1:]:
            # surface defaults changed
            self._surface.set_defaults_and_clear(" ", *tam_surface.get_defaults()[1:])

        # draw onto WinIO surface
        self._draw_onto(self._surface, tam_surface)

        # draw WinIO surface to terminal
        self._print(0, 0, "".join(self._surface.get_raw_surface()[0]),
                    *self._processes_special_color(foreground, background))

    def _draw_16_pal_256(self, tam_surface):
        """
        info: will draw tam surface to terminal in mode 16_pal_256
        :param tam_surface: TAMSurface
        :return:
        """
        # checks if surface needs to be updated
        if "." != self._surface.get_defaults()[0] or\
                self._surface.get_defaults()[2].mode_16_pal_256 != tam_surface.get_defaults()[2].mode_16_pal_256:
            # surface defaults changed
            background = tam_surface.get_defaults()[2]
            self._surface.set_defaults_and_clear(".", background, background)
            self._last_frame = None

        # draw onto WinIO surface
        self._draw_onto(self._surface, tam_surface)

        """
        A block is a string or spots that 
        all share the same colors
        """
        try:
            self._last_frame_lock.acquire()

            start = None
            width = self._surface.get_dimensions()[0]
            length = 0
            this_foreground, this_background = None, None
            char_buffer, foreground_buffer, background_buffer = self._surface.get_raw_surface()
            for spot, char, foreground, background in zip(range(len(self._surface)),
                                                          char_buffer,
                                                          foreground_buffer,
                                                          background_buffer):
                foreground, background = self._processes_special_color(foreground.mode_16_pal_256, background.mode_16_pal_256)
                # no block has benn made
                if start is None:
                    # last frame surface is not None
                    if self._last_frame is not None:
                        # spot has not change
                        last_char, last_foreground, last_background = self._last_frame.get_from_raw_spot(spot)
                        last_foreground, last_background = self._processes_special_color(last_foreground.mode_16_pal_256,
                                                                                         last_background.mode_16_pal_256)
                        if (char, foreground, background) == (last_char, last_foreground, last_background):
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
                                start // width,
                                "".join(char_buffer[start:start + length]),
                                this_foreground, this_background)
                    # start new block
                    this_foreground, this_background = foreground, background
                    start = spot
                    length = 1
                    # last frame surface is not None
                    if self._last_frame is not None:
                        # spot has not change
                        last_char, last_foreground, last_background = self._last_frame.get_from_raw_spot(spot)
                        last_foreground, last_background = self._processes_special_color(last_foreground.mode_16_pal_256,
                                                                                         last_background.mode_16_pal_256)
                        if (char, foreground, background) == (last_char, last_foreground, last_background):
                            # remove new block
                            start = None
                            length = 0

            if start is not None:
                # draw last block
                self._print(start % width, start // width, "".join(char_buffer[start:start + length]),
                            this_foreground, this_background)

            # update last frame
            if self._last_frame is None:
                # last frame is not made
                self._last_frame = self._surface.copy()
            else:
                # draw tam_surface onto last frame
                self._draw_onto(self._last_frame, tam_surface)
            # set color back to default
            background = tam_surface.get_defaults()[2]
            _, background = self._processes_special_color(background.mode_16_pal_256,
                                                          background.mode_16_pal_256)
            self._print(0, 0, "", background, background)
        finally:
            self._last_frame_lock.release()

    def _draw_16(self, tam_surface):
        """
        info: will draw tam surface to terminal in mode 16
        :param tam_surface: TAMSurface
        :return:
        """
        # checks if surface needs to be updated
        if "." != self._surface.get_defaults()[0] or self._surface.get_defaults()[2].mode_16 != tam_surface.get_defaults()[2].mode_16:
            # surface defaults changed
            background = tam_surface.get_defaults()[2]
            self._surface.set_defaults_and_clear(".", background, background)
            self._last_frame = None

        # draw onto WinIO surface
        self._draw_onto(self._surface, tam_surface)

        """
        A block is a string or spots that 
        all share the same colors
        """
        try:
            self._last_frame_lock.acquire()

            start = None
            width = self._surface.get_dimensions()[0]
            length = 0
            this_foreground, this_background = None, None
            char_buffer, foreground_buffer, background_buffer = self._surface.get_raw_surface()
            for spot, char, foreground, background in zip(range(len(self._surface)),
                                                          char_buffer,
                                                          foreground_buffer,
                                                          background_buffer):
                foreground, background = self._processes_special_color(foreground.mode_16, background.mode_16)
                # no block has benn made
                if start is None:
                    # last frame surface is not None
                    if self._last_frame is not None:
                        # spot has not change
                        last_char, last_foreground, last_background = self._last_frame.get_from_raw_spot(spot)
                        last_foreground, last_background = self._processes_special_color(last_foreground.mode_16,
                                                                                         last_background.mode_16)
                        if (char, foreground, background) == (last_char, last_foreground, last_background):
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
                                start // width,
                                "".join(char_buffer[start:start + length]),
                                this_foreground, this_background)
                    # start new block
                    this_foreground, this_background = foreground, background
                    start = spot
                    length = 1
                    # last frame surface is not None
                    if self._last_frame is not None:
                        # spot has not change
                        last_char, last_foreground, last_background = self._last_frame.get_from_raw_spot(spot)
                        last_foreground, last_background = self._processes_special_color(last_foreground.mode_16,
                                                                                         last_background.mode_16)
                        if (char, foreground, background) == (last_char, last_foreground, last_background):
                            # remove new block
                            start = None
                            length = 0

            if start is not None:
                # draw last block
                self._print(start % width, start // width, "".join(char_buffer[start:start + length]),
                            this_foreground, this_background)

            # update last frame
            if self._last_frame is None:
                # last frame is not made
                self._last_frame = self._surface.copy()
            else:
                # draw tam_surface onto last frame
                self._draw_onto(self._last_frame, tam_surface)

            # set color back to default
            background = tam_surface.get_defaults()[2]
            _, background = self._processes_special_color(background.mode_16,
                                                          background.mode_16)
            self._print(0, 0, "", background, background)
        finally:
            self._last_frame_lock.release()

    def _print(self, x, y, output, foreground_color, background_color):
        """
        info: will print to terminal
        :param x: int
        :param y: int
        :param output: str
        :param foreground_color: int
        :param background_color: int
        :return:
        """
        foreground_color, background_color = self._spot_swap(foreground_color), self._spot_swap(background_color)
        io._set_cursor_info(x, y, (foreground_color % 16) + (background_color % 16) * 16)
        self._write_to_output_stream(output, True, False)

    def _processes_special_color(self, foreground_color, background_color):
        """
        info: will processes special colors
        -1 and -2 will become the default terminal color
        :param foreground_color: int
        :param background_color: int
        :return: tuple: (int, int)
        """
        if foreground_color in (-1, -2) or background_color in (-1, -2):
            default_color = io._get_default_color()
            default_background_color = default_color // 16
            default_foreground_color = default_color - default_background_color * 16

            if foreground_color in (-1, -2):
                foreground_color = default_foreground_color
            if background_color in (-1, -2):
                background_color = default_background_color

        return foreground_color, background_color

    def _spot_swap(self, spot):
        """
        info: Will swap spots this is so cmd will look normal
        :param spot: int
        :return: int
        """
        return self._spot_swap_dict.get(spot, spot)

    def _get_console_color(self, spot):
        """
        info: Will get a console color
        :param spot: int
        :return: RGBA
        """
        spot = self._spot_swap(spot)
        return tam_colors.RGBA(*io._get_rgb_color(spot))

    def _set_console_color(self, spot, color):
        """
        info: Will set a console color
        :param spot: int
        :param color: RGBA
        :return: None
        """
        try:
            self._last_frame_lock.acquire()
            spot = self._spot_swap(spot)
            io._set_rgb_color(spot, color.r, color.g, color.b)
            self._last_frame = None
        finally:
            self._last_frame_lock.release()

    def _console_color_count(self):
        """
        info: Get console color
        :return: int
        """
        return 16


class WINUtilitiesDriver(tam_drivers.UtilitiesDriver, WinSharedData, ABC):
    def __init__(self, *args, **kwargs):
        self._reset_buffer = False
        self._console_buffer = None
        super().__init__(*args, **kwargs)

    def start(self):
        """
        info: operations for IO to start
        :return: None
        """
        self._console_buffer = io._get_buffer_dimensions()
        self._reset_buffer = True
        super().start()

    def done(self):
        """
        info: operations for IO to stop
        :return: None
        """
        if self._console_buffer is not None:
            io._set_buffer_dimensions(self.get_dimensions()[0], self._console_buffer[1])
        self._reset_buffer = False
        super().done()

    def get_dimensions(self):
        """
        info: will get teh terminal dimensions
        :return: (int, int)
        """
        return io._get_dimensions()

    def clear(self):
        """
        info: will clear the screen
        :return:
        """
        io._clear(self._reset_buffer)
        super().clear()

    def show_console_cursor(self, show):
        """
        info: Will show or hide console cursor
        :param show: bool
        :return: None
        """
        io._show_console_cursor(show)
        super().show_console_cursor(show)
