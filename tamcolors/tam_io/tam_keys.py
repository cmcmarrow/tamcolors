"""
terminal keys supported on all platforms
"""


class Keyboard:
    def __init__(self, name, key_spot_dict, key_dict=None, key_state_dict=None):
        self._name = name
        self._key_spot_dict = key_spot_dict
        self._key_dict = key_dict
        self._key_state_dict = key_state_dict

        self._key_spot_dict_reverse = {spot: key for key, spot, in key_spot_dict.items()}

        self._key_dict_reverse = {}
        if key_dict is not None:
            self._key_dict_reverse = {spot: key for key, spot, in key_dict.items()}

        self._key_state_dict_reverse = {}
        if key_state_dict is not None:
            self._key_state_dict_reverse = {spot: key for key, spot, in key_state_dict.items()}

    def __call__(self, key_dict, key_state_dict):
        """
        info: will make a new object with new key_dict and key_state_dict
        :param key_dict: dict or None
        :param key_state_dict: dict or None
        :return: Keyboard
        """
        return self.__class__(self.get_name(),
                              self.get_key_spot_dict().copy(),
                              key_dict,
                              key_state_dict)

    def get_name(self):
        """
        info: will get keyboard name
        :return: str
        """
        return self._name

    def get_key_spot_dict(self):
        """
        info: will get key spot dict
        :return: dict
        """
        return self._key_spot_dict

    def get_key_dict(self):
        """
        info: will get key dict
        :return: dict or None
        """
        return self._key_dict

    def get_key_state_dict(self):
        """
        info: will get key state dict
        :return: dict or None
        """
        return self._key_state_dict

    def spot_to_key(self, spot):
        """
        info: will get key from spot
        :param spot: int
        :return: tuple or None
        """
        return self._key_spot_dict_reverse.get(spot)

    def key_to_spot(self, key):
        """
        info: will get spot from key
        :param key: tuple
        :return: int or None
        """
        return self._key_spot_dict.get(key)

    def code_to_key(self, code):
        """
        info: will get key from code
        :param code: object
        :return: tuple or False
        """
        return self._key_dict_reverse.get(code, False)

    def code_to_key_state(self, code):
        """
        info: will get key from code
        :param code: object
        :return: tuple or False
        """
        return self._key_state_dict_reverse.get(code, False)

    def get_key_list(self):
        key_list = []
        for key in self._key_dict:
            key_list.append((key, self._key_dict[key], self._key_state_dict.get(key)))
        return key_list

    @staticmethod
    def split_code_dict(code_dict):
        """
        info: will split a code dict
        :param code_dict: dict: {tuple: (object, object)}
        :return: dict, dict
        """
        key_dict = {}
        key_state_dict = {}

        for key, item in code_dict.items():
            key_dict[key] = item[0]
            key_state_dict[key] = item[1]

        return key_dict, key_state_dict


LANGUAGE_UNKNOWN = "UNKNOWN"

LANGUAGE_US_ENGLISH = "US_ENGLISH"
LANGUAGE_UK_ENGLISH = "UK_ENGLISH"
LANGUAGE_CAN_ENGLISH = "CAN_ENGLISH"
LANGUAGE_AUS_ENGLISH = "AUS_ENGLISH"
LANGUAGE_SPA_SPANISH = "SPA_SPANISH"
LANGUAGE_LAT_SPANISH = "LAT_SPANISH"
LANGUAGE_GER_GERMAN = "GER_GERMAN"
LANGUAGE_FRE_FRENCH = "FRE_FRENCH"

KEY_TYPE_NORMAL = "NORMAL"
KEY_TYPE_WHITE_SPACE = "WHITESPACE"
KEY_TYPE_SPECIAL = "SPECIAL"

KEY_a = ("a", KEY_TYPE_NORMAL)
KEY_b = ("b", KEY_TYPE_NORMAL)
KEY_c = ("c", KEY_TYPE_NORMAL)
KEY_d = ("d", KEY_TYPE_NORMAL)
KEY_e = ("e", KEY_TYPE_NORMAL)
KEY_f = ("f", KEY_TYPE_NORMAL)
KEY_g = ("g", KEY_TYPE_NORMAL)
KEY_h = ("h", KEY_TYPE_NORMAL)
KEY_i = ("i", KEY_TYPE_NORMAL)
KEY_j = ("j", KEY_TYPE_NORMAL)
KEY_k = ("k", KEY_TYPE_NORMAL)
KEY_l = ("l", KEY_TYPE_NORMAL)
KEY_m = ("m", KEY_TYPE_NORMAL)
KEY_n = ("n", KEY_TYPE_NORMAL)
KEY_o = ("o", KEY_TYPE_NORMAL)
KEY_p = ("p", KEY_TYPE_NORMAL)
KEY_q = ("q", KEY_TYPE_NORMAL)
KEY_r = ("r", KEY_TYPE_NORMAL)
KEY_s = ("s", KEY_TYPE_NORMAL)
KEY_t = ("t", KEY_TYPE_NORMAL)
KEY_u = ("u", KEY_TYPE_NORMAL)
KEY_v = ("v", KEY_TYPE_NORMAL)
KEY_w = ("w", KEY_TYPE_NORMAL)
KEY_x = ("x", KEY_TYPE_NORMAL)
KEY_y = ("y", KEY_TYPE_NORMAL)
KEY_z = ("z", KEY_TYPE_NORMAL)
KEY_A = ("A", KEY_TYPE_NORMAL)
KEY_B = ("B", KEY_TYPE_NORMAL)
KEY_C = ("C", KEY_TYPE_NORMAL)
KEY_D = ("D", KEY_TYPE_NORMAL)
KEY_E = ("E", KEY_TYPE_NORMAL)
KEY_F = ("F", KEY_TYPE_NORMAL)
KEY_G = ("G", KEY_TYPE_NORMAL)
KEY_H = ("H", KEY_TYPE_NORMAL)
KEY_I = ("I", KEY_TYPE_NORMAL)
KEY_J = ("J", KEY_TYPE_NORMAL)
KEY_K = ("K", KEY_TYPE_NORMAL)
KEY_L = ("L", KEY_TYPE_NORMAL)
KEY_M = ("M", KEY_TYPE_NORMAL)
KEY_N = ("N", KEY_TYPE_NORMAL)
KEY_O = ("O", KEY_TYPE_NORMAL)
KEY_P = ("P", KEY_TYPE_NORMAL)
KEY_Q = ("Q", KEY_TYPE_NORMAL)
KEY_R = ("R", KEY_TYPE_NORMAL)
KEY_S = ("S", KEY_TYPE_NORMAL)
KEY_T = ("T", KEY_TYPE_NORMAL)
KEY_U = ("U", KEY_TYPE_NORMAL)
KEY_V = ("V", KEY_TYPE_NORMAL)
KEY_W = ("W", KEY_TYPE_NORMAL)
KEY_X = ("X", KEY_TYPE_NORMAL)
KEY_Y = ("Y", KEY_TYPE_NORMAL)
KEY_Z = ("Z", KEY_TYPE_NORMAL)
KEY_0 = ("0", KEY_TYPE_NORMAL)
KEY_1 = ("1", KEY_TYPE_NORMAL)
KEY_2 = ("2", KEY_TYPE_NORMAL)
KEY_3 = ("3", KEY_TYPE_NORMAL)
KEY_4 = ("4", KEY_TYPE_NORMAL)
KEY_5 = ("5", KEY_TYPE_NORMAL)
KEY_6 = ("6", KEY_TYPE_NORMAL)
KEY_7 = ("7", KEY_TYPE_NORMAL)
KEY_8 = ("8", KEY_TYPE_NORMAL)
KEY_9 = ("9", KEY_TYPE_NORMAL)
KEY_BACKTICK = ("`", KEY_TYPE_NORMAL)
KEY_HYPHEN = ("-", KEY_TYPE_NORMAL)
KEY_EQUAL_SIGN = ("=", KEY_TYPE_NORMAL)
KEY_LEFT_SQUARE_BRACKET = ("[", KEY_TYPE_NORMAL)
KEY_RIGHT_SQUARE_BRACKET = ("]", KEY_TYPE_NORMAL)
KEY_BACKSLASH = ("\\", KEY_TYPE_NORMAL)
KEY_SEMICOLON = (";", KEY_TYPE_NORMAL)
KEY_APOSTROPHE = ("'", KEY_TYPE_NORMAL)
KEY_COMMA = (",", KEY_TYPE_NORMAL)
KEY_PERIOD = (".", KEY_TYPE_NORMAL)
KEY_SLASH = ("/", KEY_TYPE_NORMAL)
KEY_TILDE = ("~", KEY_TYPE_NORMAL)
KEY_EXCLAMATION_MART = ("!", KEY_TYPE_NORMAL)
KEY_AT_SIGN = ("@", KEY_TYPE_NORMAL)
KEY_NUMBER_SIGN = ("#", KEY_TYPE_NORMAL)
KEY_DOLLAR_SYMBOL = ("$", KEY_TYPE_NORMAL)
KEY_PERCENT_SIGN = ("%", KEY_TYPE_NORMAL)
KEY_CARET = ("^", KEY_TYPE_NORMAL)
KEY_AMPERSAND = ("&", KEY_TYPE_NORMAL)
KEY_ASTERISK = ("*", KEY_TYPE_NORMAL)
KEY_LEFT_PARENTHESIS = ("(", KEY_TYPE_NORMAL)
KEY_RIGHT_PARENTHESIS = (")", KEY_TYPE_NORMAL)
KEY_UNDERSCORE = ("_", KEY_TYPE_NORMAL)
KEY_PLUS_SIGN = ("+", KEY_TYPE_NORMAL)
KEY_LEFT_CURLY_BRACKET = ("{", KEY_TYPE_NORMAL)
KEY_RIGHT_CURLY_BRACKET = ("}", KEY_TYPE_NORMAL)
KEY_VERTICAL_BAR = ("|", KEY_TYPE_NORMAL)
KEY_COLON = (":", KEY_TYPE_NORMAL)
KEY_QUOTATION_MARK = ("\"", KEY_TYPE_NORMAL)
KEY_LEFT_ANGLE_BRACKET = ("<", KEY_TYPE_NORMAL)
KEY_RIGHT_ANGLE_BRACKET = (">", KEY_TYPE_NORMAL)
KEY_QUESTION_MARK = ("?", KEY_TYPE_NORMAL)

KEY_POUND_SIGN = ("£", KEY_TYPE_NORMAL)
KEY_NOT_SIGN = ("¬", KEY_TYPE_NORMAL)

KEY_TAB = ("\t", KEY_TYPE_WHITE_SPACE)
KEY_ENTER = ("\n", KEY_TYPE_WHITE_SPACE)
KEY_SPACE = (" ", KEY_TYPE_WHITE_SPACE)
KEY_UP = ("UP", KEY_TYPE_SPECIAL)
KEY_DOWN = ("DOWN", KEY_TYPE_SPECIAL)
KEY_LEFT = ("LEFT", KEY_TYPE_SPECIAL)
KEY_RIGHT = ("RIGHT", KEY_TYPE_SPECIAL)
KEY_F1 = ("F1", KEY_TYPE_SPECIAL)
KEY_F2 = ("F2", KEY_TYPE_SPECIAL)
KEY_F3 = ("F3", KEY_TYPE_SPECIAL)
KEY_F4 = ("F4", KEY_TYPE_SPECIAL)
KEY_F5 = ("F5", KEY_TYPE_SPECIAL)
KEY_F6 = ("F6", KEY_TYPE_SPECIAL)
KEY_F7 = ("F7", KEY_TYPE_SPECIAL)
KEY_F8 = ("F8", KEY_TYPE_SPECIAL)
KEY_F9 = ("F9", KEY_TYPE_SPECIAL)
KEY_F12 = ("F12", KEY_TYPE_SPECIAL)
KEY_F1_SHIFT = ("F1_SHIFT", KEY_TYPE_SPECIAL)
KEY_F2_SHIFT = ("F2_SHIFT", KEY_TYPE_SPECIAL)
KEY_F3_SHIFT = ("F3_SHIFT", KEY_TYPE_SPECIAL)
KEY_F4_SHIFT = ("F4_SHIFT", KEY_TYPE_SPECIAL)
KEY_F5_SHIFT = ("F5_SHIFT", KEY_TYPE_SPECIAL)
KEY_F6_SHIFT = ("F6_SHIFT", KEY_TYPE_SPECIAL)
KEY_F7_SHIFT = ("F7_SHIFT", KEY_TYPE_SPECIAL)
KEY_F8_SHIFT = ("F8_SHIFT", KEY_TYPE_SPECIAL)
KEY_F9_SHIFT = ("F9_SHIFT", KEY_TYPE_SPECIAL)
KEY_F12_SHIFT = ("F12_SHIFT", KEY_TYPE_SPECIAL)
KEY_BACKSPACE = ("BACKSPACE", KEY_TYPE_SPECIAL)
KEY_ESCAPE = ("ESCAPE", KEY_TYPE_SPECIAL)
KEY_DELETE = ("DELETE", KEY_TYPE_SPECIAL)

KEYBOARD_UNKNOWN = Keyboard(LANGUAGE_UNKNOWN, {})
KEYBOARD_US_ENGLISH = Keyboard(LANGUAGE_US_ENGLISH, {KEY_ESCAPE: 0,
                                                     KEY_F1: 2,
                                                     KEY_F1_SHIFT: 3,
                                                     KEY_F2: 4,
                                                     KEY_F2_SHIFT: 5,
                                                     KEY_F3: 6,
                                                     KEY_F3_SHIFT: 7,
                                                     KEY_F4: 8,
                                                     KEY_F4_SHIFT: 9,
                                                     KEY_F5: 10,
                                                     KEY_F5_SHIFT: 11,
                                                     KEY_F6: 12,
                                                     KEY_F6_SHIFT: 13,
                                                     KEY_F7: 14,
                                                     KEY_F7_SHIFT: 15,
                                                     KEY_F8: 16,
                                                     KEY_F8_SHIFT: 17,
                                                     KEY_F9: 18,
                                                     KEY_F9_SHIFT: 19,
                                                     KEY_F12: 24,
                                                     KEY_F12_SHIFT: 25,
                                                     KEY_BACKTICK: 32,
                                                     KEY_TILDE: 33,
                                                     KEY_1: 34,
                                                     KEY_EXCLAMATION_MART: 35,
                                                     KEY_2: 36,
                                                     KEY_AT_SIGN: 37,
                                                     KEY_3: 38,
                                                     KEY_NUMBER_SIGN: 39,
                                                     KEY_4: 40,
                                                     KEY_DOLLAR_SYMBOL: 41,
                                                     KEY_5: 42,
                                                     KEY_PERCENT_SIGN: 43,
                                                     KEY_6: 44,
                                                     KEY_CARET: 45,
                                                     KEY_7: 46,
                                                     KEY_AMPERSAND: 47,
                                                     KEY_8: 48,
                                                     KEY_ASTERISK: 49,
                                                     KEY_9: 50,
                                                     KEY_LEFT_PARENTHESIS: 51,
                                                     KEY_0: 52,
                                                     KEY_RIGHT_PARENTHESIS: 53,
                                                     KEY_HYPHEN: 54,
                                                     KEY_UNDERSCORE: 55,
                                                     KEY_EQUAL_SIGN: 56,
                                                     KEY_PLUS_SIGN: 57,
                                                     KEY_BACKSPACE: 58,
                                                     KEY_TAB: 74,
                                                     KEY_q: 76,
                                                     KEY_Q: 77,
                                                     KEY_w: 78,
                                                     KEY_W: 79,
                                                     KEY_e: 80,
                                                     KEY_E: 81,
                                                     KEY_r: 82,
                                                     KEY_R: 83,
                                                     KEY_t: 84,
                                                     KEY_T: 85,
                                                     KEY_y: 86,
                                                     KEY_Y: 87,
                                                     KEY_u: 88,
                                                     KEY_U: 89,
                                                     KEY_i: 90,
                                                     KEY_I: 91,
                                                     KEY_o: 92,
                                                     KEY_O: 93,
                                                     KEY_p: 94,
                                                     KEY_P: 95,
                                                     KEY_LEFT_SQUARE_BRACKET: 96,
                                                     KEY_LEFT_CURLY_BRACKET: 97,
                                                     KEY_RIGHT_SQUARE_BRACKET: 98,
                                                     KEY_RIGHT_CURLY_BRACKET: 99,
                                                     KEY_BACKSLASH: 100,
                                                     KEY_VERTICAL_BAR: 101,
                                                     KEY_DELETE: 102,
                                                     KEY_a: 116,
                                                     KEY_A: 117,
                                                     KEY_s: 118,
                                                     KEY_S: 119,
                                                     KEY_d: 120,
                                                     KEY_D: 121,
                                                     KEY_f: 122,
                                                     KEY_F: 123,
                                                     KEY_g: 124,
                                                     KEY_G: 125,
                                                     KEY_h: 126,
                                                     KEY_H: 127,
                                                     KEY_j: 128,
                                                     KEY_J: 129,
                                                     KEY_k: 130,
                                                     KEY_K: 131,
                                                     KEY_l: 132,
                                                     KEY_L: 133,
                                                     KEY_SEMICOLON: 134,
                                                     KEY_COLON: 135,
                                                     KEY_APOSTROPHE: 136,
                                                     KEY_QUOTATION_MARK: 137,
                                                     KEY_ENTER: 138,
                                                     KEY_z: 148,
                                                     KEY_Z: 149,
                                                     KEY_x: 150,
                                                     KEY_X: 151,
                                                     KEY_c: 152,
                                                     KEY_C: 153,
                                                     KEY_v: 154,
                                                     KEY_V: 155,
                                                     KEY_b: 156,
                                                     KEY_B: 157,
                                                     KEY_n: 158,
                                                     KEY_N: 159,
                                                     KEY_m: 160,
                                                     KEY_M: 161,
                                                     KEY_COMMA: 162,
                                                     KEY_LEFT_ANGLE_BRACKET: 163,
                                                     KEY_PERIOD: 164,
                                                     KEY_RIGHT_ANGLE_BRACKET: 165,
                                                     KEY_SLASH: 166,
                                                     KEY_QUESTION_MARK: 167,
                                                     KEY_UP: 170,
                                                     KEY_SPACE: 186,
                                                     KEY_LEFT: 196,
                                                     KEY_DOWN: 198,
                                                     KEY_RIGHT: 200})
KEYBOARD_UK_ENGLISH = Keyboard(LANGUAGE_UK_ENGLISH, {KEY_ESCAPE: 0,
                                                     KEY_F1: 2,
                                                     KEY_F1_SHIFT: 3,
                                                     KEY_F2: 4,
                                                     KEY_F2_SHIFT: 5,
                                                     KEY_F3: 6,
                                                     KEY_F3_SHIFT: 7,
                                                     KEY_F4: 8,
                                                     KEY_F4_SHIFT: 9,
                                                     KEY_F5: 10,
                                                     KEY_F5_SHIFT: 11,
                                                     KEY_F6: 12,
                                                     KEY_F6_SHIFT: 13,
                                                     KEY_F7: 14,
                                                     KEY_F7_SHIFT: 15,
                                                     KEY_F8: 16,
                                                     KEY_F8_SHIFT: 17,
                                                     KEY_F9: 18,
                                                     KEY_F9_SHIFT: 19,
                                                     KEY_F12: 24,
                                                     KEY_F12_SHIFT: 25,
                                                     KEY_BACKTICK: 32,
                                                     KEY_NOT_SIGN: 33,
                                                     KEY_1: 34,
                                                     KEY_EXCLAMATION_MART: 35,
                                                     KEY_2: 36,
                                                     KEY_QUOTATION_MARK: 37,
                                                     KEY_3: 38,
                                                     KEY_POUND_SIGN: 39,
                                                     KEY_4: 40,
                                                     KEY_DOLLAR_SYMBOL: 41,
                                                     KEY_5: 42,
                                                     KEY_PERCENT_SIGN: 43,
                                                     KEY_6: 44,
                                                     KEY_CARET: 45,
                                                     KEY_7: 46,
                                                     KEY_AMPERSAND: 47,
                                                     KEY_8: 48,
                                                     KEY_ASTERISK: 49,
                                                     KEY_9: 50,
                                                     KEY_LEFT_PARENTHESIS: 51,
                                                     KEY_0: 52,
                                                     KEY_RIGHT_PARENTHESIS: 53,
                                                     KEY_HYPHEN: 54,
                                                     KEY_UNDERSCORE: 55,
                                                     KEY_EQUAL_SIGN: 56,
                                                     KEY_PLUS_SIGN: 57,
                                                     KEY_BACKSPACE: 58,
                                                     KEY_TAB: 74,
                                                     KEY_q: 76,
                                                     KEY_Q: 77,
                                                     KEY_w: 78,
                                                     KEY_W: 79,
                                                     KEY_e: 80,
                                                     KEY_E: 81,
                                                     KEY_r: 82,
                                                     KEY_R: 83,
                                                     KEY_t: 84,
                                                     KEY_T: 85,
                                                     KEY_y: 86,
                                                     KEY_Y: 87,
                                                     KEY_u: 88,
                                                     KEY_U: 89,
                                                     KEY_i: 90,
                                                     KEY_I: 91,
                                                     KEY_o: 92,
                                                     KEY_O: 93,
                                                     KEY_p: 94,
                                                     KEY_P: 95,
                                                     KEY_LEFT_SQUARE_BRACKET: 96,
                                                     KEY_LEFT_CURLY_BRACKET: 97,
                                                     KEY_RIGHT_SQUARE_BRACKET: 98,
                                                     KEY_RIGHT_CURLY_BRACKET: 99,
                                                     KEY_BACKSLASH: 100,
                                                     KEY_VERTICAL_BAR: 101,
                                                     KEY_DELETE: 102,
                                                     KEY_a: 116,
                                                     KEY_A: 117,
                                                     KEY_s: 118,
                                                     KEY_S: 119,
                                                     KEY_d: 120,
                                                     KEY_D: 121,
                                                     KEY_f: 122,
                                                     KEY_F: 123,
                                                     KEY_g: 124,
                                                     KEY_G: 125,
                                                     KEY_h: 126,
                                                     KEY_H: 127,
                                                     KEY_j: 128,
                                                     KEY_J: 129,
                                                     KEY_k: 130,
                                                     KEY_K: 131,
                                                     KEY_l: 132,
                                                     KEY_L: 133,
                                                     KEY_SEMICOLON: 134,
                                                     KEY_COLON: 135,
                                                     KEY_APOSTROPHE: 136,
                                                     KEY_AT_SIGN: 137,
                                                     KEY_NUMBER_SIGN: 300,
                                                     KEY_TILDE: 301,
                                                     KEY_ENTER: 138,
                                                     KEY_z: 148,
                                                     KEY_Z: 149,
                                                     KEY_x: 150,
                                                     KEY_X: 151,
                                                     KEY_c: 152,
                                                     KEY_C: 153,
                                                     KEY_v: 154,
                                                     KEY_V: 155,
                                                     KEY_b: 156,
                                                     KEY_B: 157,
                                                     KEY_n: 158,
                                                     KEY_N: 159,
                                                     KEY_m: 160,
                                                     KEY_M: 161,
                                                     KEY_COMMA: 162,
                                                     KEY_LEFT_ANGLE_BRACKET: 163,
                                                     KEY_PERIOD: 164,
                                                     KEY_RIGHT_ANGLE_BRACKET: 165,
                                                     KEY_SLASH: 166,
                                                     KEY_QUESTION_MARK: 167,
                                                     KEY_UP: 170,
                                                     KEY_SPACE: 186,
                                                     KEY_LEFT: 196,
                                                     KEY_DOWN: 198,
                                                     KEY_RIGHT: 200})
KEYBOARD_CAN_ENGLISH = Keyboard(LANGUAGE_CAN_ENGLISH, KEYBOARD_US_ENGLISH.get_key_spot_dict().copy())
KEYBOARD_AUS_ENGLISH = Keyboard(LANGUAGE_AUS_ENGLISH, KEYBOARD_US_ENGLISH.get_key_spot_dict().copy())

LANGUAGES = set()
KEY_TYPES = set()
KEYS = set()
KEYBOARDS = {}


for var in list(vars()):
    if "KEY_TYPE_" in var:
        KEY_TYPES.add(vars()[var])
    elif "LANGUAGE_" in var:
        LANGUAGES.add(vars()[var])
    elif "KEY_" in var and "KEY_TYPE" not in var:
        KEYS.add(vars()[var])
    elif "KEYBOARD_" in var:
        KEYBOARDS[vars()[var].get_name()] = vars()[var]
del var
