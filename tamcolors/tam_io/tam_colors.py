# built in libraries
from functools import lru_cache
from tamcolors.utils.immutable_cache import ImmutableCache
from tamcolors.utils.object_packer import FastHandObjectPacker


"""
terminal colors supported on all platforms
Color holds all color values for all supported modes
RGBA holds the values for mode rgb
"""


class Color(ImmutableCache, FastHandObjectPacker):
    __slots__ = ("_mode_2", "_mode_16", "_mode_256", "_mode_rgb", "_has_alpha", "_byte_cache")

    def __init__(self, mode_16, mode_256, mode_rgb, mode_2=None):
        """
        info: Makes a Color object
        :param mode_16: int
        :param mode_256: int
        :param mode_rgb: RGBA
        :param mode_2: int or None
        """
        if mode_2 is None:
            mode_2 = mode_16

        self._mode_2 = mode_2
        self._mode_16 = mode_16
        self._mode_256 = mode_256
        self._mode_rgb = mode_rgb
        self._has_alpha = -2 in (mode_2, mode_16, mode_256) or (mode_rgb.a != 255 and not mode_rgb.is_default)
        self._byte_cache = bytes((*self._int_mode_to_binary(self._mode_2),
                                  *self._int_mode_to_binary(self._mode_16),
                                  *self._int_mode_to_binary(self._mode_256),
                                  *self.mode_rgb.to_bytes()))

    def __str__(self):
        return "(2: {}, 16: {}, 256: {}, rgb: {}, has_alpha: {})".format(self.mode_2,
                                                                         self.mode_16,
                                                                         self.mode_256,
                                                                         self.mode_rgb,
                                                                         self.has_alpha)

    def __hash__(self):
        return hash((self._mode_2, self._mode_16, self._mode_256, self._mode_rgb, self._has_alpha))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.mode_2 == other.mode_2 and self.mode_16 == other.mode_16 and self.mode_256 == other.mode_256 \
                   and self.mode_rgb == other.mode_rgb and self.has_alpha == other.has_alpha
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def _int_mode_to_binary(mode):
        return abs(min(0, mode)), abs(mode)

    @staticmethod
    def _int_mode_from_binary(binary):
        if binary[0] == 0:
            return binary[1]
        return binary[0]*-1

    @property
    def mode_2(self):
        """
        info: Gets mode 2
        :return: int
        """
        return self._mode_2

    @property
    def mode_16(self):
        """
        info: Gets mode 16
        :return: int
        """
        return self._mode_16

    @property
    def mode_256(self):
        """
        info: Gets mode 256
        :return: int
        """
        return self._mode_256

    @property
    def mode_rgb(self):
        """
        info: Gets mode rgb
        :return: RGBA
        """
        return self._mode_rgb

    @property
    def has_alpha(self):
        """
        info: Checks if color has any alpha
        :return: bool
        """
        return self._has_alpha

    def place_color_over(self, old_color, override_alpha):
        """
        info: Will calculate what the new color will be
        :param old_color: Color
        :param override_alpha: bool
        :return: color
        """
        if override_alpha:
            return self

        mode_2 = self.mode_2
        if mode_2 == -2:
            mode_2 = old_color.mode_2

        mode_16 = self.mode_16
        if mode_16 == -2:
            mode_16 = old_color.mode_16

        mode_256 = self.mode_256
        if mode_256 == -2:
            mode_256 = old_color.mode_256

        mode_rgb = self.mode_rgb
        if mode_rgb.a != 255 and not self.mode_rgb.is_default:
            if mode_rgb.a == 0:
                mode_rgb = old_color.mode_rgb
            else:
                mode_rgb = RGBA(self.transparent_value(mode_rgb.r, mode_rgb.a, old_color.mode_rgb.r),
                                self.transparent_value(mode_rgb.g, mode_rgb.a, old_color.mode_rgb.g),
                                self.transparent_value(mode_rgb.b, mode_rgb.a, old_color.mode_rgb.b),
                                old_color.mode_rgb.a)

        return self.__class__(mode_16, mode_256, mode_rgb, mode_2)

    @staticmethod
    @lru_cache(maxsize=5000)
    def transparent_value(new,  alpha, old):
        alpha = alpha/255
        return min(255, max(0, round(alpha * new + (1 - alpha) * old)))

    def to_bytes(self):
        return self._byte_cache

    @classmethod
    @lru_cache(maxsize=5000)
    def _from(cls, other_modes, mode_rgb):
        mode_2 = cls._int_mode_from_binary(other_modes[:2])
        mode_16 = cls._int_mode_from_binary(other_modes[2:4])
        mode_256 = cls._int_mode_from_binary(other_modes[4:6])
        return cls(mode_16, mode_256, mode_rgb, mode_2)

    @classmethod
    def from_bytes(cls, object_byte_array):
        other_modes = bytes(object_byte_array[:6])
        del object_byte_array[:6]
        mode_rgb = RGBA.from_bytes(object_byte_array)
        return cls._from(other_modes, mode_rgb)


class RGBA(ImmutableCache, FastHandObjectPacker):
    __slots__ = ("_r", "_g", "_b", "_a", "_is_default", "_byte_cache")

    def __init__(self, r, g, b, a=255, is_default=False):
        """
        info: Will make a RGBA object
        :param r: int
        :param g: int
        :param b: int
        :param a: int
        :param is_default: Bool
        """
        self._r = r
        self._g = g
        self._b = b
        self._a = a
        self._is_default = is_default
        self._byte_cache = bytes((self._r, self._g, self._b, self._a, int(self._is_default)))

    def __str__(self):
        return "(r: {}, g: {}, b: {}, a: {}, is_default: {})".format(self.r,
                                                                     self.g,
                                                                     self.b,
                                                                     self.a,
                                                                     self.is_default)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self._r, self._g, self._b, self._a, self._is_default))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a \
                   and self.is_default == other.is_default
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def r(self):
        """
        info: Will get the r value
        :return: int
        """
        return self._r

    @property
    def g(self):
        """
        info: Will get the g value
        :return: int
        """
        return self._g

    @property
    def b(self):
        """
        info: Will get the b value
        :return: int
        """
        return self._b

    @property
    def a(self):
        """
        info: Will get the a value
        :return: int
        """
        return self._a

    @property
    def is_default(self):
        """
        info: See if color is default
        :return: bool
        """
        return self._is_default

    def to_bytes(self):
        return self._byte_cache

    @classmethod
    @lru_cache(maxsize=5000)
    def _from(cls, r, g, b, a, is_default):
        return cls(r, g, b, a, bool(is_default))

    @classmethod
    def from_bytes(cls, object_byte_array):
        obj = cls._from(*object_byte_array[:5])
        del object_byte_array[:5]
        return obj


ALPHA = Color(-2, -2, RGBA(0, 0, 0, 0))
DEFAULT = Color(-1, -1, RGBA(0, 0, 0, 255, True))

BLACK = Color(0, 0, RGBA(0, 0, 0))
RED = Color(1, 1, RGBA(128, 0, 0))
GREEN = Color(2, 2, RGBA(0, 128, 0))
YELLOW = Color(3, 3, RGBA(128, 128, 0))
BLUE = Color(4, 4, RGBA(0, 0, 128))
PURPLE = Color(5, 5, RGBA(128, 0, 128))
AQUA = Color(6, 6, RGBA(0, 128, 128))
WHITE = Color(7, 7, RGBA(192, 192, 192))
GRAY = Color(8, 8, RGBA(128, 128, 128))
LIGHT_RED = Color(9, 9, RGBA(255, 0, 0))
LIGHT_GREEN = Color(10, 10, RGBA(0, 255, 0))
LIGHT_YELLOW = Color(11, 11, RGBA(255, 255, 0))
LIGHT_BLUE = Color(12, 12, RGBA(0, 0, 255))
LIGHT_PURPLE = Color(13, 13, RGBA(255, 0, 255))
LIGHT_AQUA = Color(14, 14, RGBA(0, 255, 255))
LIGHT_WHITE = Color(15, 15, RGBA(255, 255, 255))

COLOR_0 = BLACK
COLOR_1 = RED
COLOR_2 = GREEN
COLOR_3 = YELLOW
COLOR_4 = BLUE
COLOR_5 = PURPLE
COLOR_6 = AQUA
COLOR_7 = WHITE
COLOR_8 = GRAY
COLOR_9 = LIGHT_RED
COLOR_10 = LIGHT_GREEN
COLOR_11 = LIGHT_YELLOW
COLOR_12 = LIGHT_BLUE
COLOR_13 = LIGHT_PURPLE
COLOR_14 = LIGHT_AQUA
COLOR_15 = LIGHT_WHITE
COLOR_16 = Color(0, 16, RGBA(0, 0, 0))
COLOR_17 = Color(4, 17, RGBA(0, 0, 95))
COLOR_18 = Color(4, 18, RGBA(0, 0, 95))
COLOR_19 = Color(12, 19, RGBA(0, 0, 175))
COLOR_20 = Color(12, 20, RGBA(0, 0, 215))
COLOR_21 = Color(12, 21, RGBA(0, 0, 255))
COLOR_22 = Color(6, 22, RGBA(0, 95, 0))
COLOR_23 = Color(12, 23, RGBA(0, 95, 95))
COLOR_24 = Color(6, 24, RGBA(0, 95, 135))
COLOR_25 = Color(6, 25, RGBA(0, 95, 175))
COLOR_26 = Color(12, 26, RGBA(0, 95, 215))
COLOR_27 = Color(12, 27, RGBA(0, 95, 255))
COLOR_28 = Color(2, 28, RGBA(0, 135, 0))
COLOR_29 = Color(6, 29, RGBA(0, 135, 95))
COLOR_30 = Color(14, 30, RGBA(0, 135, 135))
COLOR_31 = Color(6, 31, RGBA(0, 135, 175))
COLOR_32 = Color(12, 32, RGBA(0, 135, 215))
COLOR_33 = Color(14, 33, RGBA(0, 135, 255))
COLOR_34 = Color(2, 34, RGBA(0, 175, 0))
COLOR_35 = Color(2, 35, RGBA(0, 175, 95))
COLOR_36 = Color(6, 36, RGBA(0, 175, 135))
COLOR_37 = Color(6, 37, RGBA(0, 175, 175))
COLOR_38 = Color(6, 38, RGBA(0, 175, 215))
COLOR_39 = Color(12, 39, RGBA(0, 175, 255))
COLOR_40 = Color(10, 40, RGBA(0, 215, 0))
COLOR_41 = Color(10, 41, RGBA(0, 215, 95))
COLOR_42 = Color(10, 42, RGBA(0, 215, 135))
COLOR_43 = Color(10, 43, RGBA(0, 215, 175))
COLOR_44 = Color(2, 44, RGBA(0, 215, 21))
COLOR_45 = Color(14, 45, RGBA(0, 215, 255))
COLOR_46 = Color(10, 46, RGBA(0, 255, 0))
COLOR_47 = Color(10, 47, RGBA(0, 255, 95))
COLOR_48 = Color(10, 48, RGBA(0, 255, 135))
COLOR_49 = Color(10, 49, RGBA(0, 255, 175))
COLOR_50 = Color(14, 50, RGBA(0, 255, 215))
COLOR_51 = Color(14, 51, RGBA(0, 255, 255))
COLOR_52 = Color(1, 52, RGBA(95, 0, 0))
COLOR_53 = Color(5, 53, RGBA(95, 0, 95))
COLOR_54 = Color(5, 54, RGBA(95, 0, 135))
COLOR_55 = Color(5, 55, RGBA(95, 0, 175))
COLOR_56 = Color(5, 56, RGBA(95, 0, 215))
COLOR_57 = Color(5, 57, RGBA(95, 0, 255))
COLOR_58 = Color(3, 58, RGBA(95, 95, 0))
COLOR_59 = Color(8, 59, RGBA(95, 95, 95))
COLOR_60 = Color(8, 60, RGBA(95, 95, 135))
COLOR_61 = Color(5, 61, RGBA(95, 95, 175))
COLOR_62 = Color(5, 62, RGBA(95, 95, 215))
COLOR_63 = Color(5, 63, RGBA(95, 95, 255))
COLOR_64 = Color(3, 64, RGBA(95, 135, 0))
COLOR_65 = Color(2, 65, RGBA(95, 135, 95))
COLOR_66 = Color(2, 66, RGBA(95, 135, 135))
COLOR_67 = Color(5, 67, RGBA(95, 135, 175))
COLOR_68 = Color(6, 68, RGBA(95, 135, 215))
COLOR_69 = Color(5, 69, RGBA(95, 135, 255))
COLOR_70 = Color(2, 70, RGBA(95, 175, 0))
COLOR_71 = Color(2, 71, RGBA(95, 175, 95))
COLOR_72 = Color(2, 72, RGBA(95, 175, 135))
COLOR_73 = Color(6, 73, RGBA(95, 175, 175))
COLOR_74 = Color(14, 74, RGBA(95, 175, 215))
COLOR_75 = Color(14, 75, RGBA(95, 175, 255))
COLOR_76 = Color(2, 76, RGBA(95, 215, 0))
COLOR_77 = Color(10, 77, RGBA(95, 215, 95))
COLOR_78 = Color(14, 78, RGBA(95, 215, 135))
COLOR_79 = Color(6, 79, RGBA(95, 215, 175))
COLOR_80 = Color(14, 80, RGBA(95, 215, 215))
COLOR_81 = Color(14, 81, RGBA(95, 215, 255))
COLOR_82 = Color(2, 82, RGBA(95, 255, 0))
COLOR_83 = Color(10, 83, RGBA(95, 255, 95))
COLOR_84 = Color(10, 84, RGBA(95, 255, 135))
COLOR_85 = Color(14, 85, RGBA(95, 255, 175))
COLOR_86 = Color(6, 86, RGBA(95, 255, 215))
COLOR_87 = Color(14, 87, RGBA(95, 255, 255))
COLOR_88 = Color(1, 88, RGBA(135, 0, 0))
COLOR_89 = Color(1, 89, RGBA(135, 0, 95))
COLOR_90 = Color(5, 90, RGBA(135, 0, 135))
COLOR_91 = Color(5, 91, RGBA(135, 0, 175))
COLOR_92 = Color(5, 92, RGBA(135, 0, 215))
COLOR_93 = Color(13, 93, RGBA(135, 0, 255))
COLOR_94 = Color(3, 94, RGBA(135, 95, 0))
COLOR_95 = Color(1, 95, RGBA(135, 95, 95))
COLOR_96 = Color(5, 96, RGBA(135, 95, 135))
COLOR_97 = Color(5, 97, RGBA(135, 95, 175))
COLOR_98 = Color(5, 98, RGBA(135, 95, 215))
COLOR_99 = Color(5, 99, RGBA(135, 95, 255))
COLOR_100 = Color(3, 100, RGBA(135, 135, 0))
COLOR_101 = Color(3, 101, RGBA(135, 135, 95))
COLOR_102 = Color(7, 102, RGBA(135, 135, 135))
COLOR_103 = Color(8, 103, RGBA(135, 135, 175))
COLOR_104 = Color(8, 104, RGBA(135, 135, 215))
COLOR_105 = Color(5, 105, RGBA(135, 135, 255))
COLOR_106 = Color(10, 106, RGBA(135, 175, 0))
COLOR_107 = Color(3, 107, RGBA(135, 175, 95))
COLOR_108 = Color(12, 108, RGBA(135, 175, 135))
COLOR_109 = Color(6, 109, RGBA(135, 175, 175))
COLOR_110 = Color(14, 110, RGBA(135, 175, 215))
COLOR_111 = Color(14, 111, RGBA(135, 175, 255))
COLOR_112 = Color(2, 112, RGBA(135, 215, 0))
COLOR_113 = Color(10, 113, RGBA(135, 215, 95))
COLOR_114 = Color(2, 114, RGBA(135, 215, 135))
COLOR_115 = Color(10, 115, RGBA(135, 215, 175))
COLOR_116 = Color(14, 116, RGBA(135, 215, 215))
COLOR_117 = Color(14, 117, RGBA(135, 215, 255))
COLOR_118 = Color(10, 118, RGBA(135, 255, 0))
COLOR_119 = Color(10, 119, RGBA(135, 255, 95))
COLOR_120 = Color(10, 120, RGBA(135, 255, 135))
COLOR_121 = Color(10, 121, RGBA(135, 255, 175))
COLOR_122 = Color(10, 122, RGBA(135, 255, 215))
COLOR_123 = Color(14, 123, RGBA(135, 255, 255))
COLOR_124 = Color(1, 124, RGBA(175, 0, 0))
COLOR_125 = Color(1, 125, RGBA(175, 0, 95))
COLOR_126 = Color(5, 126, RGBA(175, 0, 135))
COLOR_127 = Color(5, 127, RGBA(175, 0, 175))
COLOR_128 = Color(5, 128, RGBA(175, 0, 215))
COLOR_129 = Color(13, 129, RGBA(175, 0, 255))
COLOR_130 = Color(3, 130, RGBA(175, 95, 0))
COLOR_131 = Color(1, 131, RGBA(175, 95, 95))
COLOR_132 = Color(1, 132, RGBA(175, 95, 135))
COLOR_133 = Color(5, 133, RGBA(175, 95, 175))
COLOR_134 = Color(5, 134, RGBA(175, 95, 215))
COLOR_135 = Color(13, 135, RGBA(175, 95, 255))
COLOR_136 = Color(3, 136, RGBA(175, 135, 0))
COLOR_137 = Color(3, 137, RGBA(175, 135, 95))
COLOR_138 = Color(3, 138, RGBA(175, 135, 135))
COLOR_139 = Color(3, 139, RGBA(175, 135, 175))
COLOR_140 = Color(5, 140, RGBA(175, 135, 215))
COLOR_141 = Color(13, 141, RGBA(175, 135, 255))
COLOR_142 = Color(3, 142, RGBA(175, 175, 0))
COLOR_143 = Color(3, 143, RGBA(175, 175, 95))
COLOR_144 = Color(3, 144, RGBA(175, 175, 135))
COLOR_145 = Color(7, 145, RGBA(175, 175, 175))
COLOR_146 = Color(5, 146, RGBA(175, 175, 215))
COLOR_147 = Color(8, 147, RGBA(175, 175, 255))
COLOR_148 = Color(10, 148, RGBA(175, 215, 0))
COLOR_149 = Color(2, 149, RGBA(175, 215, 95))
COLOR_150 = Color(6, 150, RGBA(175, 215, 135))
COLOR_151 = Color(7, 151, RGBA(175, 215, 175))
COLOR_152 = Color(14, 152, RGBA(175, 215, 215))
COLOR_153 = Color(14, 153, RGBA(175, 215, 255))
COLOR_154 = Color(10, 154, RGBA(175, 255, 0))
COLOR_155 = Color(10, 155, RGBA(175, 255, 95))
COLOR_156 = Color(10, 156, RGBA(175, 255, 135))
COLOR_157 = Color(10, 157, RGBA(175, 255, 175))
COLOR_158 = Color(14, 158, RGBA(175, 255, 215))
COLOR_159 = Color(14, 159, RGBA(175, 255, 255))
COLOR_160 = Color(9, 160, RGBA(215, 0, 0))
COLOR_161 = Color(9, 161, RGBA(215, 0, 95))
COLOR_162 = Color(13, 162, RGBA(215, 0, 135))
COLOR_163 = Color(13, 163, RGBA(215, 0, 175))
COLOR_164 = Color(13, 164, RGBA(215, 0, 215))
COLOR_165 = Color(5, 165, RGBA(215, 0, 255))
COLOR_166 = Color(3, 166, RGBA(215, 95, 0))
COLOR_167 = Color(9, 167, RGBA(215, 95, 95))
COLOR_168 = Color(9, 168, RGBA(215, 95, 135))
COLOR_169 = Color(9, 169, RGBA(215, 95, 175))
COLOR_170 = Color(5, 170, RGBA(215, 95, 215))
COLOR_171 = Color(13, 171, RGBA(215, 95, 255))
COLOR_172 = Color(3, 172, RGBA(215, 135, 0))
COLOR_173 = Color(3, 173, RGBA(215, 135, 95))
COLOR_174 = Color(3, 174, RGBA(215, 135, 135))
COLOR_175 = Color(13, 175, RGBA(215, 135, 175))
COLOR_176 = Color(13, 176, RGBA(215, 135, 215))
COLOR_177 = Color(13, 177, RGBA(215, 135, 255))
COLOR_178 = Color(3, 178, RGBA(215, 175, 0))
COLOR_179 = Color(3, 179, RGBA(215, 175, 95))
COLOR_180 = Color(3, 180, RGBA(215, 175, 135))
COLOR_181 = Color(3, 181, RGBA(215, 175, 175))
COLOR_182 = Color(6, 182, RGBA(215, 175, 215))
COLOR_183 = Color(13, 183, RGBA(215, 175, 255))
COLOR_184 = Color(11, 184, RGBA(215, 215, 0))
COLOR_185 = Color(3, 185, RGBA(215, 215, 95))
COLOR_186 = Color(3, 186, RGBA(215, 215, 135))
COLOR_187 = Color(11, 187, RGBA(215, 215, 175))
COLOR_188 = Color(7, 188, RGBA(215, 215, 215))
COLOR_189 = Color(13, 189, RGBA(215, 215, 255))
COLOR_190 = Color(10, 190, RGBA(215, 255, 0))
COLOR_191 = Color(11, 191, RGBA(215, 255, 95))
COLOR_192 = Color(10, 192, RGBA(215, 255, 135))
COLOR_193 = Color(10, 193, RGBA(215, 255, 175))
COLOR_194 = Color(2, 194, RGBA(215, 255, 215))
COLOR_195 = Color(14, 195, RGBA(215, 255, 255))
COLOR_196 = Color(9, 196, RGBA(255, 0, 0))
COLOR_197 = Color(9, 197, RGBA(255, 0, 95))
COLOR_198 = Color(9, 198, RGBA(255, 0, 135))
COLOR_199 = Color(13, 199, RGBA(255, 0, 175))
COLOR_200 = Color(13, 200, RGBA(255, 0, 215))
COLOR_201 = Color(9, 201, RGBA(255, 0, 255))
COLOR_202 = Color(9, 202, RGBA(255, 95, 0))
COLOR_203 = Color(11, 203, RGBA(255, 95, 95))
COLOR_204 = Color(9, 204, RGBA(255, 95, 135))
COLOR_205 = Color(13, 205, RGBA(255, 95, 175))
COLOR_206 = Color(13, 206, RGBA(255, 95, 215))
COLOR_207 = Color(13, 207, RGBA(255, 95, 255))
COLOR_208 = Color(11, 208, RGBA(255, 135, 0))
COLOR_209 = Color(11, 209, RGBA(255, 135, 95))
COLOR_210 = Color(9, 210, RGBA(255, 135, 135))
COLOR_211 = Color(13, 211, RGBA(255, 135, 175))
COLOR_212 = Color(13, 212, RGBA(255, 135, 215))
COLOR_213 = Color(5, 213, RGBA(255, 135, 255))
COLOR_214 = Color(6, 214, RGBA(255, 175, 0))
COLOR_215 = Color(11, 215, RGBA(255, 175, 95))
COLOR_216 = Color(11, 216, RGBA(255, 175, 135))
COLOR_217 = Color(9, 217, RGBA(255, 175, 175))
COLOR_218 = Color(13, 218, RGBA(255, 175, 215))
COLOR_219 = Color(13, 219, RGBA(255, 175, 255))
COLOR_220 = Color(11, 220, RGBA(255, 215, 0))
COLOR_221 = Color(11, 221, RGBA(255, 215, 95))
COLOR_222 = Color(11, 222, RGBA(255, 215, 135))
COLOR_223 = Color(11, 223, RGBA(255, 215, 175))
COLOR_224 = Color(13, 224, RGBA(255, 215, 215))
COLOR_225 = Color(13, 225, RGBA(255, 215, 255))
COLOR_226 = Color(11, 226, RGBA(255, 255, 0))
COLOR_227 = Color(11, 227, RGBA(255, 255, 95))
COLOR_228 = Color(11, 228, RGBA(255, 255, 135))
COLOR_229 = Color(11, 229, RGBA(255, 255, 175))
COLOR_230 = Color(6, 230, RGBA(255, 255, 215))
COLOR_231 = Color(15, 231, RGBA(255, 255, 255))
COLOR_232 = Color(0, 232, RGBA(8, 8, 8))
COLOR_233 = Color(0, 233, RGBA(18, 18, 18))
COLOR_234 = Color(0, 234, RGBA(28, 28, 28))
COLOR_235 = Color(0, 235, RGBA(38, 38, 38))
COLOR_236 = Color(0, 236, RGBA(48, 48, 48))
COLOR_237 = Color(0, 237, RGBA(58, 58, 58))
COLOR_238 = Color(0, 238, RGBA(68, 68, 68))
COLOR_239 = Color(8, 239, RGBA(78, 78, 78))
COLOR_240 = Color(8, 240, RGBA(88, 88, 88))
COLOR_241 = Color(8, 241, RGBA(98, 98, 98))
COLOR_242 = Color(8, 242, RGBA(108, 108, 108))
COLOR_243 = Color(8, 243, RGBA(118, 118, 118))
COLOR_244 = Color(8, 244, RGBA(128, 128, 128))
COLOR_245 = Color(8, 245, RGBA(138, 138, 138))
COLOR_246 = Color(8, 246, RGBA(148, 148, 148))
COLOR_247 = Color(8, 247, RGBA(158, 158, 158))
COLOR_248 = Color(8, 248, RGBA(168, 168, 168))
COLOR_249 = Color(8, 249, RGBA(178, 178, 178))
COLOR_250 = Color(7, 250, RGBA(188, 188, 188))
COLOR_251 = Color(15, 251, RGBA(198, 198, 198))
COLOR_252 = Color(15, 252, RGBA(208, 208, 208))
COLOR_253 = Color(15, 253, RGBA(218, 218, 218))
COLOR_254 = Color(15, 254, RGBA(228, 228, 228))
COLOR_255 = Color(15, 255, RGBA(238, 238, 238))

COLORS = []
for color_id in range(256):
    COLORS.append(vars()["COLOR_{}".format(color_id)])
COLORS = tuple(COLORS)
