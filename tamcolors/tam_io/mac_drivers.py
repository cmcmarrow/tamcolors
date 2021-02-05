# built in libraries
from abc import ABC
from itertools import cycle

# tamcolors libraries
from tamcolors.tam_c import _uni_tam as io
from tamcolors.tam_io import tam_drivers, tam_keys, uni_drivers


class MACKeyDriver(tam_drivers.KeyDriver, uni_drivers.UNISharedData, ABC):
    def __init__(self, *args, **kwargs):
        self._mac_keyboard = tam_keys.KEYBOARDS[self.get_keyboard_name()](
            *tam_keys.Keyboard.split_code_dict(self.get_key_dict()))
        self._keys = cycle(self._mac_keyboard.get_key_list())
        self._key_count = len(self._mac_keyboard.get_key_list())
        super().__init__(*args, **kwargs)

    def get_key(self):
        """
        info: Gets an input from the terminal
        :return: tuple or false
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
                return self._mac_keyboard.code_to_key(tuple(key_bytes))
        return False

    def get_key_dict(self, language=None):
        """
        info: Gets a dict of all the keys
        :param language: str or None
        :return: dict
        """
        if language is None:
            language = self.get_keyboard_name()

        if language in (tam_keys.LANGUAGE_US_ENGLISH, tam_keys.LANGUAGE_CAN_ENGLISH, tam_keys.LANGUAGE_AUS_ENGLISH):
            return {tam_keys.KEY_ESCAPE: ((27,), None),
                    tam_keys.KEY_F1: ((27, 79, 80), None),
                    tam_keys.KEY_F1_SHIFT: ((27, 91, 49, 59, 50, 80), None),
                    tam_keys.KEY_F2: ((27, 79, 81), None),
                    tam_keys.KEY_F2_SHIFT: ((27, 91, 49, 59, 50, 81), None),
                    tam_keys.KEY_F3: ((27, 79, 82), None),
                    tam_keys.KEY_F3_SHIFT: ((27, 91, 49, 59, 50, 82), None),
                    tam_keys.KEY_F4: ((27, 79, 83), None),
                    tam_keys.KEY_F4_SHIFT: ((27, 91, 49, 59, 50, 83), None),
                    tam_keys.KEY_F5: ((27, 91, 49, 53, 126), None),
                    tam_keys.KEY_F5_SHIFT: ((27, 91, 49, 53, 59, 50, 126), None),
                    tam_keys.KEY_F6: ((27, 91, 49, 55, 126), None),
                    tam_keys.KEY_F6_SHIFT: ((27, 91, 49, 55, 59, 50, 126), None),
                    tam_keys.KEY_F7: ((27, 91, 49, 56, 126), None),
                    tam_keys.KEY_F7_SHIFT: ((27, 91, 49, 56, 59, 50, 126), None),
                    tam_keys.KEY_F8: ((27, 91, 49, 57, 126), None),
                    tam_keys.KEY_F8_SHIFT: ((27, 91, 49, 57, 59, 50, 126), None),
                    tam_keys.KEY_F9: ((27, 91, 50, 48, 126), None),
                    tam_keys.KEY_F9_SHIFT: ((27, 91, 50, 48, 59, 50, 126), None),
                    tam_keys.KEY_F12: ((27, 91, 50, 52, 126), None),
                    tam_keys.KEY_F12_SHIFT: ((27, 91, 50, 52, 59, 50, 126), None),
                    tam_keys.KEY_BACKTICK: ((96,), None),
                    tam_keys.KEY_TILDE: ((126,), None),
                    tam_keys.KEY_1: ((49,), None),
                    tam_keys.KEY_EXCLAMATION_MART: ((33,), None),
                    tam_keys.KEY_2: ((50,), None),
                    tam_keys.KEY_AT_SIGN: ((64,), None),
                    tam_keys.KEY_3: ((51,), None),
                    tam_keys.KEY_NUMBER_SIGN: ((35,), None),
                    tam_keys.KEY_4: ((52,), None),
                    tam_keys.KEY_DOLLAR_SYMBOL: ((36,), None),
                    tam_keys.KEY_5: ((53,), None),
                    tam_keys.KEY_PERCENT_SIGN: ((37,), None),
                    tam_keys.KEY_6: ((54,), None),
                    tam_keys.KEY_CARET: ((94,), None),
                    tam_keys.KEY_7: ((55,), None),
                    tam_keys.KEY_AMPERSAND: ((38,), None),
                    tam_keys.KEY_8: ((56,), None),
                    tam_keys.KEY_ASTERISK: ((42,), None),
                    tam_keys.KEY_9: ((57,), None),
                    tam_keys.KEY_LEFT_PARENTHESIS: ((40,), None),
                    tam_keys.KEY_0: ((48,), None),
                    tam_keys.KEY_RIGHT_PARENTHESIS: ((41,), None),
                    tam_keys.KEY_HYPHEN: ((45,), None),
                    tam_keys.KEY_UNDERSCORE: ((95,), None),
                    tam_keys.KEY_EQUAL_SIGN: ((61,), None),
                    tam_keys.KEY_PLUS_SIGN: ((43,), None),
                    tam_keys.KEY_BACKSPACE: ((127,), None),
                    tam_keys.KEY_TAB: ((9,), None),
                    tam_keys.KEY_q: ((113,), None),
                    tam_keys.KEY_Q: ((81,), None),
                    tam_keys.KEY_w: ((119,), None),
                    tam_keys.KEY_W: ((87,), None),
                    tam_keys.KEY_e: ((101,), None),
                    tam_keys.KEY_E: ((69,), None),
                    tam_keys.KEY_r: ((114,), None),
                    tam_keys.KEY_R: ((82,), None),
                    tam_keys.KEY_t: ((116,), None),
                    tam_keys.KEY_T: ((84,), None),
                    tam_keys.KEY_y: ((121,), None),
                    tam_keys.KEY_Y: ((89,), None),
                    tam_keys.KEY_u: ((117,), None),
                    tam_keys.KEY_U: ((85,), None),
                    tam_keys.KEY_i: ((105,), None),
                    tam_keys.KEY_I: ((73,), None),
                    tam_keys.KEY_o: ((111,), None),
                    tam_keys.KEY_O: ((79,), None),
                    tam_keys.KEY_p: ((112,), None),
                    tam_keys.KEY_P: ((80,), None),
                    tam_keys.KEY_LEFT_SQUARE_BRACKET: ((91,), None),
                    tam_keys.KEY_LEFT_CURLY_BRACKET: ((123,), None),
                    tam_keys.KEY_RIGHT_SQUARE_BRACKET: ((93,), None),
                    tam_keys.KEY_RIGHT_CURLY_BRACKET: ((125,), None),
                    tam_keys.KEY_BACKSLASH: ((92,), None),
                    tam_keys.KEY_VERTICAL_BAR: ((124,), None),
                    tam_keys.KEY_DELETE: ((27, 91, 51, 126), None),
                    tam_keys.KEY_a: ((97,), None),
                    tam_keys.KEY_A: ((65,), None),
                    tam_keys.KEY_s: ((115,), None),
                    tam_keys.KEY_S: ((83,), None),
                    tam_keys.KEY_d: ((100,), None),
                    tam_keys.KEY_D: ((68,), None),
                    tam_keys.KEY_f: ((102,), None),
                    tam_keys.KEY_F: ((70,), None),
                    tam_keys.KEY_g: ((103,), None),
                    tam_keys.KEY_G: ((71,), None),
                    tam_keys.KEY_h: ((104,), None),
                    tam_keys.KEY_H: ((72,), None),
                    tam_keys.KEY_j: ((106,), None),
                    tam_keys.KEY_J: ((74,), None),
                    tam_keys.KEY_k: ((107,), None),
                    tam_keys.KEY_K: ((75,), None),
                    tam_keys.KEY_l: ((108,), None),
                    tam_keys.KEY_L: ((76,), None),
                    tam_keys.KEY_SEMICOLON: ((59,), None),
                    tam_keys.KEY_COLON: ((58,), None),
                    tam_keys.KEY_APOSTROPHE: ((39,), None),
                    tam_keys.KEY_QUOTATION_MARK: ((34,), None),
                    tam_keys.KEY_ENTER: ((10,), None),
                    tam_keys.KEY_z: ((122,), None),
                    tam_keys.KEY_Z: ((90,), None),
                    tam_keys.KEY_x: ((120,), None),
                    tam_keys.KEY_X: ((88,), None),
                    tam_keys.KEY_c: ((99,), None),
                    tam_keys.KEY_C: ((67,), None),
                    tam_keys.KEY_v: ((118,), None),
                    tam_keys.KEY_V: ((86,), None),
                    tam_keys.KEY_b: ((98,), None),
                    tam_keys.KEY_B: ((66,), None),
                    tam_keys.KEY_n: ((110,), None),
                    tam_keys.KEY_N: ((78,), None),
                    tam_keys.KEY_m: ((109,), None),
                    tam_keys.KEY_M: ((77,), None),
                    tam_keys.KEY_COMMA: ((44,), None),
                    tam_keys.KEY_LEFT_ANGLE_BRACKET: ((60,), None),
                    tam_keys.KEY_PERIOD: ((46,), None),
                    tam_keys.KEY_RIGHT_ANGLE_BRACKET: ((62,), None),
                    tam_keys.KEY_SLASH: ((47,), None),
                    tam_keys.KEY_QUESTION_MARK: ((63,), None),
                    tam_keys.KEY_UP: ((27, 91, 65), None),
                    tam_keys.KEY_SPACE: ((32,), None),
                    tam_keys.KEY_LEFT: ((27, 91, 68), None),
                    tam_keys.KEY_DOWN: ((27, 91, 66), None),
                    tam_keys.KEY_RIGHT: ((27, 91, 67), None)}
        return {}

    def get_keyboard_name(self, default_to_us_english=True):
        """
        info: Will get the keyboard language name
        :param default_to_us_english: bool
        :return: str
        """
        if default_to_us_english:
            return tam_keys.LANGUAGE_US_ENGLISH
        return tam_keys.LANGUAGE_UNKNOWN

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
