from collections import namedtuple


"""
terminal colors supported on all platforms
"""

COLOR = namedtuple("COLOR", ("mode_2", "mode_16", "mode_256", "mode_rgb", "has_alpha"))


class Color:
    __slots__ = ("_mode_2", "_mode_16", "_mode_256", "_mode_rgb", "_has_alpha")

    def __init__(self, mode_16, mode_256, mode_rgb, mode_2=None):
        if mode_2 is None:
            mode_2 = mode_16

        self._mode_2 = mode_2
        self._mode_16 = mode_16
        self._mode_256 = mode_256
        self._mode_rgb = mode_rgb
        self._has_alpha = -2 in (mode_2, mode_16, mode_256) or (mode_rgb.a != 255 and not mode_rgb.is_default)

    @property
    def mode_2(self):
        return self._mode_2

    @property
    def mode_16(self):
        return self._mode_16

    @property
    def mode_256(self):
        return self._mode_256

    @property
    def mode_rgb(self):
        return self._mode_rgb

    @property
    def has_alpha(self):
        return self._has_alpha

    def place_color_over(self, old_color, override_alpha):
        if override_alpha:
            return old_color

        mode_2 = self.mode_2
        if mode_2 == -2:
            mode_2 = old_color.mode_2

        mode_16 = self.mode_16
        if mode_16 == -2:
            mode_16 = old_color.mode_16

        mode_256 = self.mode_256
        if mode_256 == -2:
            mode_256 = old_color.mode_256

        # TODO
        mode_rgb = self.mode_rgb

        return self.__class__(mode_16, mode_256, mode_rgb, mode_2)


class RGBA:
    __slots__ = ("_r", "_g", "_b", "_a", "_is_default")

    def __init__(self, r, g, b, a=255, is_default=False):
        self._r = r
        self._g = g
        self._b = b
        self._a = a
        self._is_default = is_default

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    @property
    def a(self):
        return self._a

    @property
    def is_default(self):
        return self._is_default


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
COLOR_17 = Color(1, 17, RGBA(0, 0, 95))
COLOR_18 = Color(2, 18, RGBA(0, 0, 95))
COLOR_19 = Color(3, 19, RGBA(0, 0, 175))
COLOR_20 = Color(4, 20, RGBA(0, 0, 215))
COLOR_21 = Color(5, 21, RGBA(0, 0, 255))
COLOR_22 = Color(6, 22, RGBA(0, 95, 0))
COLOR_23 = Color(7, 23, RGBA(0, 95, 95))
COLOR_24 = Color(8, 24, RGBA(0, 95, 135))
COLOR_25 = Color(9, 25, RGBA(0, 95, 175))
COLOR_26 = Color(10, 26, RGBA(0, 95, 215))
COLOR_27 = Color(11, 27, RGBA(0, 95, 255))
COLOR_28 = Color(12, 28, RGBA(0, 135, 0))
COLOR_29 = Color(13, 29, RGBA(0, 135, 95))
COLOR_30 = Color(14, 30, RGBA(0, 135, 135))
COLOR_31 = Color(15, 31, RGBA(0, 135, 175))
COLOR_32 = Color(0, 32, RGBA(0, 135, 215))
COLOR_33 = Color(1, 33, RGBA(0, 135, 255))
COLOR_34 = Color(2, 34, RGBA(0, 175, 0))
COLOR_35 = Color(3, 35, RGBA(0, 175, 95))
COLOR_36 = Color(4, 36, RGBA(0, 175, 135))
COLOR_37 = Color(5, 37, RGBA(0, 175, 175))
COLOR_38 = Color(6, 38, RGBA(0, 175, 215))
COLOR_39 = Color(7, 39, RGBA(0, 175, 255))
COLOR_40 = Color(8, 40, RGBA(0, 215, 0))
COLOR_41 = Color(9, 41, RGBA(0, 215, 95))
COLOR_42 = Color(10, 42, RGBA(0, 215, 135))
COLOR_43 = Color(11, 43, RGBA(0, 215, 175))
COLOR_44 = Color(12, 44, RGBA(0, 215, 21))
COLOR_45 = Color(13, 45, RGBA(0, 215, 255))
COLOR_46 = Color(14, 46, RGBA(0, 255, 0))
COLOR_47 = Color(15, 47, RGBA(0, 255, 95))
COLOR_48 = Color(0, 48, RGBA(0, 255, 135))
COLOR_49 = Color(1, 49, RGBA(0, 255, 175))
COLOR_50 = Color(2, 50, RGBA(0, 255, 215))
COLOR_51 = Color(3, 51, RGBA(0, 255, 255))
COLOR_52 = Color(4, 52, RGBA(95, 0, 0))
COLOR_53 = Color(5, 53, RGBA(95, 0, 95))
COLOR_54 = Color(6, 54, RGBA(95, 0, 135))
COLOR_55 = Color(7, 55, RGBA(95, 0, 175))
COLOR_56 = Color(8, 56, RGBA(95, 0, 215))
COLOR_57 = Color(9, 57, RGBA(95, 0, 255))
COLOR_58 = Color(10, 58, RGBA(95, 95, 0))
COLOR_59 = Color(11, 59, RGBA(95, 95, 95))
COLOR_60 = Color(12, 60, RGBA(95, 95, 135))
COLOR_61 = Color(13, 61, RGBA(95, 95, 175))
COLOR_62 = Color(14, 62, RGBA(95, 95, 215))
COLOR_63 = Color(15, 63, RGBA(95, 95, 255))
COLOR_64 = Color(0, 64, RGBA(95, 135, 0))
COLOR_65 = Color(1, 65, RGBA(95, 135, 95))
COLOR_66 = Color(2, 66, RGBA(95, 135, 135))
COLOR_67 = Color(3, 67, RGBA(95, 135, 175))
COLOR_68 = Color(4, 68, RGBA(95, 135, 215))
COLOR_69 = Color(5, 69, RGBA(95, 135, 255))
COLOR_70 = Color(6, 70, RGBA(95, 175, 0))
COLOR_71 = Color(7, 71, RGBA(95, 175, 95))
COLOR_72 = Color(8, 72, RGBA(95, 175, 135))
COLOR_73 = Color(9, 73, RGBA(95, 175, 175))
COLOR_74 = Color(10, 74, RGBA(95, 175, 215))
COLOR_75 = Color(11, 75, RGBA(95, 175, 255))
COLOR_76 = Color(12, 76, RGBA(95, 215, 0))
COLOR_77 = Color(13, 77, RGBA(95, 215, 95))
COLOR_78 = Color(14, 78, RGBA(95, 215, 135))
COLOR_79 = Color(15, 79, RGBA(95, 215, 175))
COLOR_80 = Color(0, 80, RGBA(95, 215, 215))
COLOR_81 = Color(1, 81, RGBA(95, 215, 255))
COLOR_82 = Color(2, 82, RGBA(95, 255, 0))
COLOR_83 = Color(3, 83, RGBA(95, 255, 95))
COLOR_84 = Color(4, 84, RGBA(95, 255, 135))
COLOR_85 = Color(5, 85, RGBA(95, 255, 175))
COLOR_86 = Color(6, 86, RGBA(95, 255, 215))
COLOR_87 = Color(7, 87, RGBA(95, 255, 255))
COLOR_88 = Color(8, 88, RGBA(135, 0, 0))
COLOR_89 = Color(9, 89, RGBA(135, 0, 95))
COLOR_90 = Color(10, 90, RGBA(135, 0, 135))
COLOR_91 = Color(11, 91, RGBA(135, 0, 175))
COLOR_92 = Color(12, 92, RGBA(135, 0, 215))
COLOR_93 = Color(13, 93, RGBA(135, 0, 255))
COLOR_94 = Color(14, 94, RGBA(135, 95, 0))
COLOR_95 = Color(15, 95, RGBA(135, 95, 95))
COLOR_96 = Color(0, 96, RGBA(135, 95, 135))
COLOR_97 = Color(1, 97, RGBA(135, 95, 175))
COLOR_98 = Color(2, 98, RGBA(135, 95, 215))
COLOR_99 = Color(3, 99, RGBA(135, 95, 255))
COLOR_100 = Color(4, 100, RGBA(135, 135, 0))
COLOR_101 = Color(5, 101, RGBA(135, 135, 95))
COLOR_102 = Color(6, 102, RGBA(135, 135, 135))
COLOR_103 = Color(7, 103, RGBA(135, 135, 175))
COLOR_104 = Color(8, 104, RGBA(135, 135, 215))
COLOR_105 = Color(9, 105, RGBA(135, 135, 255))
COLOR_106 = Color(10, 106, RGBA(135, 175, 0))
COLOR_107 = Color(11, 107, RGBA(135, 175, 95))
COLOR_108 = Color(12, 108, RGBA(135, 175, 135))
COLOR_109 = Color(13, 109, RGBA(135, 175, 175))
COLOR_110 = Color(14, 110, RGBA(135, 175, 215))
COLOR_111 = Color(15, 111, RGBA(135, 175, 255))
COLOR_112 = Color(0, 112, RGBA(135, 215, 0))
COLOR_113 = Color(1, 113, RGBA(135, 215, 95))
COLOR_114 = Color(2, 114, RGBA(135, 215, 135))
COLOR_115 = Color(3, 115, RGBA(135, 215, 175))
COLOR_116 = Color(4, 116, RGBA(135, 215, 215))
COLOR_117 = Color(5, 117, RGBA(135, 215, 255))
COLOR_118 = Color(6, 118, RGBA(135, 255, 0))
COLOR_119 = Color(7, 119, RGBA(135, 255, 95))
COLOR_120 = Color(8, 120, RGBA(135, 255, 135))
COLOR_121 = Color(9, 121, RGBA(135, 255, 175))
COLOR_122 = Color(10, 122, RGBA(135, 255, 215))
COLOR_123 = Color(11, 123, RGBA(135, 255, 255))
COLOR_124 = Color(12, 124, RGBA(175, 0, 0))
COLOR_125 = Color(13, 125, RGBA(175, 0, 95))
COLOR_126 = Color(14, 126, RGBA(175, 0, 135))
COLOR_127 = Color(15, 127, RGBA(175, 0, 175))
COLOR_128 = Color(0, 128, RGBA(175, 0, 215))
COLOR_129 = Color(1, 129, RGBA(175, 0, 255))
COLOR_130 = Color(2, 130, RGBA(175, 95, 0))
COLOR_131 = Color(3, 131, RGBA(175, 95, 95))
COLOR_132 = Color(4, 132, RGBA(175, 95, 135))
COLOR_133 = Color(5, 133, RGBA(175, 95, 175))
COLOR_134 = Color(6, 134, RGBA(175, 95, 215))
COLOR_135 = Color(7, 135, RGBA(175, 95, 255))
COLOR_136 = Color(8, 136, RGBA(175, 135, 0))
COLOR_137 = Color(9, 137, RGBA(175, 135, 95))
COLOR_138 = Color(10, 138, RGBA(175, 135, 135))
COLOR_139 = Color(11, 139, RGBA(175, 135, 175))
COLOR_140 = Color(12, 140, RGBA(175, 135, 215))
COLOR_141 = Color(13, 141, RGBA(175, 135, 255))
COLOR_142 = Color(14, 142, RGBA(175, 175, 0))
COLOR_143 = Color(15, 143, RGBA(175, 175, 95))
COLOR_144 = Color(0, 144, RGBA(175, 175, 135))
COLOR_145 = Color(1, 145, RGBA(175, 175, 175))
COLOR_146 = Color(2, 146, RGBA(175, 175, 215))
COLOR_147 = Color(3, 147, RGBA(175, 175, 255))
COLOR_148 = Color(4, 148, RGBA(175, 215, 0))
COLOR_149 = Color(5, 149, RGBA(175, 215, 95))
COLOR_150 = Color(6, 150, RGBA(175, 215, 135))
COLOR_151 = Color(7, 151, RGBA(175, 215, 175))
COLOR_152 = Color(8, 152, RGBA(175, 215, 215))
COLOR_153 = Color(9, 153, RGBA(175, 215, 255))
COLOR_154 = Color(10, 154, RGBA(175, 255, 0))
COLOR_155 = Color(11, 155, RGBA(175, 255, 95))
COLOR_156 = Color(12, 156, RGBA(175, 255, 135))
COLOR_157 = Color(13, 157, RGBA(175, 255, 175))
COLOR_158 = Color(14, 158, RGBA(175, 255, 215))
COLOR_159 = Color(15, 159, RGBA(175, 255, 255))
COLOR_160 = Color(0, 160, RGBA(215, 0, 0))
COLOR_161 = Color(1, 161, RGBA(215, 0, 95))
COLOR_162 = Color(2, 162, RGBA(215, 0, 135))
COLOR_163 = Color(3, 163, RGBA(215, 0, 175))
COLOR_164 = Color(4, 164, RGBA(215, 0, 215))
COLOR_165 = Color(5, 165, RGBA(215, 0, 255))
COLOR_166 = Color(6, 166, RGBA(215, 95, 0))
COLOR_167 = Color(7, 167, RGBA(215, 95, 95))
COLOR_168 = Color(8, 168, RGBA(215, 95, 135))
COLOR_169 = Color(9, 169, RGBA(215, 95, 175))
COLOR_170 = Color(10, 170, RGBA(215, 95, 215))
COLOR_171 = Color(11, 171, RGBA(215, 95, 255))
COLOR_172 = Color(12, 172, RGBA(215, 135, 0))
COLOR_173 = Color(13, 173, RGBA(215, 135, 95))
COLOR_174 = Color(14, 174, RGBA(215, 135, 135))
COLOR_175 = Color(15, 175, RGBA(215, 135, 175))
COLOR_176 = Color(0, 176, RGBA(215, 135, 215))
COLOR_177 = Color(1, 177, RGBA(215, 135, 255))
COLOR_178 = Color(2, 178, RGBA(215, 175, 0))
COLOR_179 = Color(3, 179, RGBA(215, 175, 95))
COLOR_180 = Color(4, 180, RGBA(215, 175, 135))
COLOR_181 = Color(5, 181, RGBA(215, 175, 175))
COLOR_182 = Color(6, 182, RGBA(215, 175, 215))
COLOR_183 = Color(7, 183, RGBA(215, 175, 255))
COLOR_184 = Color(8, 184, RGBA(215, 215, 0))
COLOR_185 = Color(9, 185, RGBA(215, 215, 95))
COLOR_186 = Color(10, 186, RGBA(215, 215, 135))
COLOR_187 = Color(11, 187, RGBA(215, 215, 175))
COLOR_188 = Color(12, 188, RGBA(215, 215, 215))
COLOR_189 = Color(13, 189, RGBA(215, 215, 255))
COLOR_190 = Color(14, 190, RGBA(215, 255, 0))
COLOR_191 = Color(15, 191, RGBA(215, 255, 95))
COLOR_192 = Color(0, 192, RGBA(215, 255, 135))
COLOR_193 = Color(1, 193, RGBA(215, 255, 175))
COLOR_194 = Color(2, 194, RGBA(215, 255, 215))
COLOR_195 = Color(3, 195, RGBA(215, 255, 255))
COLOR_196 = Color(4, 196, RGBA(255, 0, 0))
COLOR_197 = Color(5, 197, RGBA(255, 0, 95))
COLOR_198 = Color(6, 198, RGBA(255, 0, 135))
COLOR_199 = Color(7, 199, RGBA(255, 0, 175))
COLOR_200 = Color(8, 200, RGBA(255, 0, 215))
COLOR_201 = Color(9, 201, RGBA(255, 0, 255))
COLOR_202 = Color(10, 202, RGBA(255, 95, 0))
COLOR_203 = Color(11, 203, RGBA(255, 95, 95))
COLOR_204 = Color(12, 204, RGBA(255, 95, 135))
COLOR_205 = Color(13, 205, RGBA(255, 95, 175))
COLOR_206 = Color(14, 206, RGBA(255, 95, 215))
COLOR_207 = Color(15, 207, RGBA(255, 95, 255))
COLOR_208 = Color(0, 208, RGBA(255, 135, 0))
COLOR_209 = Color(1, 209, RGBA(255, 135, 95))
COLOR_210 = Color(2, 210, RGBA(255, 135, 135))
COLOR_211 = Color(3, 211, RGBA(255, 135, 175))
COLOR_212 = Color(4, 212, RGBA(255, 135, 215))
COLOR_213 = Color(5, 213, RGBA(255, 135, 255))
COLOR_214 = Color(6, 214, RGBA(255, 175, 0))
COLOR_215 = Color(7, 215, RGBA(255, 175, 95))
COLOR_216 = Color(8, 216, RGBA(255, 175, 135))
COLOR_217 = Color(9, 217, RGBA(255, 175, 175))
COLOR_218 = Color(10, 218, RGBA(255, 175, 215))
COLOR_219 = Color(11, 219, RGBA(255, 175, 255))
COLOR_220 = Color(12, 220, RGBA(255, 215, 0))
COLOR_221 = Color(13, 221, RGBA(255, 215, 95))
COLOR_222 = Color(14, 222, RGBA(255, 215, 135))
COLOR_223 = Color(15, 223, RGBA(255, 215, 175))
COLOR_224 = Color(0, 224, RGBA(255, 215, 215))
COLOR_225 = Color(1, 225, RGBA(255, 215, 255))
COLOR_226 = Color(2, 226, RGBA(255, 255, 0))
COLOR_227 = Color(3, 227, RGBA(255, 255, 95))
COLOR_228 = Color(4, 228, RGBA(255, 255, 135))
COLOR_229 = Color(5, 229, RGBA(255, 255, 175))
COLOR_230 = Color(6, 230, RGBA(255, 255, 215))
COLOR_231 = Color(7, 231, RGBA(255, 255, 255))
COLOR_232 = Color(8, 232, RGBA(8, 8, 8))
COLOR_233 = Color(9, 233, RGBA(18, 18, 18))
COLOR_234 = Color(10, 234, RGBA(28, 28, 28))
COLOR_235 = Color(11, 235, RGBA(38, 38, 38))
COLOR_236 = Color(12, 236, RGBA(48, 48, 48))
COLOR_237 = Color(13, 237, RGBA(58, 58, 58))
COLOR_238 = Color(14, 238, RGBA(68, 68, 68))
COLOR_239 = Color(15, 239, RGBA(78, 78, 78))
COLOR_240 = Color(0, 240, RGBA(88, 88, 88))
COLOR_241 = Color(1, 241, RGBA(98, 98, 98))
COLOR_242 = Color(2, 242, RGBA(108, 108, 108))
COLOR_243 = Color(3, 243, RGBA(118, 118, 118))
COLOR_244 = Color(4, 244, RGBA(128, 128, 128))
COLOR_245 = Color(5, 245, RGBA(138, 138, 138))
COLOR_246 = Color(6, 246, RGBA(148, 148, 148))
COLOR_247 = Color(7, 247, RGBA(158, 158, 158))
COLOR_248 = Color(8, 248, RGBA(168, 168, 168))
COLOR_249 = Color(9, 249, RGBA(178, 178, 178))
COLOR_250 = Color(10, 250, RGBA(188, 188, 188))
COLOR_251 = Color(11, 251, RGBA(198, 198, 198))
COLOR_252 = Color(12, 252, RGBA(208, 208, 208))
COLOR_253 = Color(13, 253, RGBA(218, 218, 218))
COLOR_254 = Color(14, 254, RGBA(228, 228, 228))
COLOR_255 = Color(15, 255, RGBA(238, 238, 238))


COLOR_LIST = []

for color_id in range(256):
    COLOR_LIST.append(vars()["COLOR_{}".format(color_id)])
