# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors.tam_io.tam_colors import*


class TAMSurfaceTests(unittest.TestCase):
    def test_surface_init(self):
        surface = tam_io.tam_surface.TAMSurface(3, 4, "&", RED, GREEN)
        self.assertEqual(str(surface), ("&&&\n"*4)[:-1])

    def test_surface_str(self):
        surface = tam_io.tam_surface.TAMSurface(3, 400, "&", RED, GREEN)
        self.assertEqual(str(surface), ("&&&\n" * 400)[:-1])

    def test_surface_str_2(self):
        surface = tam_io.tam_surface.TAMSurface(3, 400, "&", RED, GREEN)
        surface.set_spot(1, 2, tam_io.tam_surface.ALPHA_CHAR, ALPHA, ALPHA, False)
        self.assertEqual(str(surface), ("&&&\n" * 400)[:-1])

    def test_surface_str_3(self):
        surface = tam_io.tam_surface.TAMSurface(3, 2, tam_io.tam_surface.ALPHA_CHAR, RED, GREEN)
        surface.set_spot(2, 1, "#", ALPHA, ALPHA, False)
        self.assertEqual(str(surface), "   \n  #")

    def test_surface_len(self):
        surface = tam_io.tam_surface.TAMSurface(5, 4, "&", RED, GREEN)
        self.assertEqual(len(surface), 20)

    def test_surface_len_2(self):
        surface = tam_io.tam_surface.TAMSurface(50, 6, "&", RED, GREEN)
        self.assertEqual(len(surface), 300)

    def test_surface_len_3(self):
        surface = tam_io.tam_surface.TAMSurface(55, 65, "&", RED, GREEN)
        self.assertEqual(len(surface), 3575)
        surface.set_dimensions_and_clear(5, 7)
        self.assertEqual(len(surface), 35)

    def test_surface_len_4(self):
        surface = tam_io.tam_surface.TAMSurface(0, 50, "&", RED, GREEN)
        self.assertEqual(len(surface), 0)

    def test_surface_eq(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        self.assertTrue(surface == surface2)

    def test_surface_eq_2(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(26, 50, "&", RED, GREEN)
        self.assertFalse(surface == surface2)

    def test_surface_eq_3(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(25, 50, "c", RED, GREEN)
        self.assertFalse(surface == surface2)

    def test_surface_eq_4(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2.set_spot(12, 34, "b", AQUA, WHITE)
        self.assertFalse(surface == surface2)

    def test_surface_eq_5(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        self.assertFalse(surface == 34)

    def test_surface_ne(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        self.assertFalse(surface != surface2)

    def test_surface_ne_2(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(26, 50, "&", RED, GREEN)
        self.assertTrue(surface != surface2)

    def test_surface_ne_3(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(25, 50, "c", RED, GREEN)
        self.assertTrue(surface != surface2)

    def test_surface_ne_4(self):
        surface = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(25, 50, "&", RED, GREEN)
        surface2.set_spot(12, 34, "b", AQUA, WHITE)
        self.assertTrue(surface != surface2)

    def test_clear(self):
        surface = tam_io.tam_surface.TAMSurface(5, 20, ".", RED, GREEN)
        for y in range(20):
            for x in range(5):
                surface.set_spot(x, y, "@", LIGHT_RED, LIGHT_GREEN)

        surface.clear()

        for y in range(20):
            for x in range(5):
                self.assertEqual(surface.get_spot(x, y), (".", RED, GREEN))
        self.assertEqual(str(surface), (".....\n" * 20)[:-1])

    def test_get_dimensions(self):
        surface = tam_io.tam_surface.TAMSurface(5, 20, ".", RED, GREEN)
        self.assertEqual(surface.get_dimensions(), (5, 20))

    def test_get_dimensions_2(self):
        surface = tam_io.tam_surface.TAMSurface(3005, 2200, ".", RED, GREEN)
        self.assertEqual(surface.get_dimensions(), (3005, 2200))

    def test_get_dimensions_3(self):
        surface = tam_io.tam_surface.TAMSurface(0, 1, ".", RED, GREEN)
        self.assertEqual(surface.get_dimensions(), (0, 1))

    def test_set_dimensions_and_clear(self):
        surface = tam_io.tam_surface.TAMSurface(5, 20, ".", RED, GREEN)
        surface.set_dimensions_and_clear(2, 3)
        self.assertEqual(str(surface), ("..\n" * 3)[:-1])

    def test_set_dimensions_and_clear_2(self):
        surface = tam_io.tam_surface.TAMSurface(5, 20, ".", RED, GREEN)
        surface.set_dimensions_and_clear(6, 300)
        self.assertEqual(str(surface), ("......\n" * 300)[:-1])

    def test_get_defaults(self):
        surface = tam_io.tam_surface.TAMSurface(5, 20, ".", RED, GREEN)
        surface.get_defaults()
        self.assertEqual(surface.get_defaults(), (".", RED, GREEN))

    def test_set_defaults_and_clear(self):
        surface = tam_io.tam_surface.TAMSurface(5, 20, ".", RED, GREEN)
        surface.set_defaults_and_clear("L", PURPLE, AQUA)
        for y in range(20):
            for x in range(5):
                self.assertEqual(surface.get_spot(x, y), ("L", PURPLE, AQUA))

    def test_set_defaults_and_clear_2(self):
        surface = tam_io.tam_surface.TAMSurface(50, 22, ".", RED, GREEN)
        surface.set_defaults_and_clear("A", WHITE, GREEN)
        for y in range(22):
            for x in range(50):
                self.assertEqual(surface.get_spot(x, y), ("A", WHITE, GREEN))

    def test_get_raw_surface(self):
        surface = tam_io.tam_surface.TAMSurface(50, 22, ".", RED, GREEN)
        length = 50 * 22
        self.assertEqual((["."] * length, [RED] * length, [GREEN] * length), surface.get_raw_surface())

    def test_get_raw_surface_2(self):
        surface = tam_io.tam_surface.TAMSurface(501, 222, ".", RED, GREEN)
        length = 501 * 222
        self.assertEqual((["."] * length, [RED] * length, [GREEN] * length), surface.get_raw_surface())

    def test_copy(self):
        surface = tam_io.tam_surface.TAMSurface(50, 22, ".", RED, GREEN)
        surface2 = surface.copy()

        for y in range(22):
            for x in range(50):
                surface2.set_spot(x, y, "H", PURPLE, GREEN)

        self.assertNotEqual(str(surface), str(surface2))

    def test_copy_2(self):
        surface = tam_io.tam_surface.TAMSurface(55, 23, ".", RED, GREEN)
        surface2 = surface.copy()

        for y in range(23):
            for x in range(55):
                surface2.set_spot(x, y, "H", PURPLE, GREEN)

        self.assertNotEqual(str(surface), str(surface2))

    def test_get_raw_spot(self):
        surface = tam_io.tam_surface.TAMSurface(55, 23, ".", RED, GREEN)
        raw_spots = []

        for y in range(23):
            for x in range(55):
                raw_spot = surface.get_raw_spot(x, y)
                self.assertTrue(raw_spot not in raw_spots)
                raw_spots.append(raw_spot)

        self.assertTrue(all([i in range(0, 55 * 23) for i in raw_spots]))

    def test_set_spot(self):
        surface = tam_io.tam_surface.TAMSurface(3, 4, "&", RED, GREEN)
        for y in range(4):
            surface.set_spot(0, y, 'T', RED, GREEN)
        self.assertEqual(str(surface), ("T&&\n"*4)[:-1])

    def test_set_spot_2(self):
        surface = tam_io.tam_surface.TAMSurface(3, 4, "&", RED, GREEN)
        for y in range(4):
            surface.set_spot(y % 3, y, "T", RED, GREEN)
        self.assertEqual(str(surface), "T&&\n&T&\n&&T\nT&&")

    def test_set_spot_3(self):
        surface = tam_io.tam_surface.TAMSurface(5, 5, "&", RED, GREEN)
        for y in range(5):
            for x in range(5):
                surface.set_spot(x, y, str(x), RED, GREEN)
        self.assertEqual(str(surface), ("01234\n"*5)[:-1])

    def test_set_spot_4(self):
        surface = tam_io.tam_surface.TAMSurface(5, 5, "&", RED, GREEN)
        surface.set_spot(0, 1, "C", AQUA, AQUA)
        self.assertEqual(surface.get_spot(0, 1), ("C", AQUA, AQUA))

    def test_set_spot_5(self):
        surface = tam_io.tam_surface.TAMSurface(5, 5, "&", RED, GREEN)
        surface.set_spot(3, 2, "A", BLUE, ALPHA)
        surface.set_spot(3, 2, "C", ALPHA, AQUA)
        self.assertEqual(surface.get_spot(3, 2), ("C", BLUE, AQUA))

    def test_set_spot_6(self):
        surface = tam_io.tam_surface.TAMSurface(5, 5, "&", RED, GREEN)
        surface.set_spot(3, 2, "A", BLUE, DEFAULT)
        surface.set_spot(3, 2, "C", DEFAULT, DEFAULT)
        self.assertEqual(surface.get_spot(3, 2), ("C", DEFAULT, DEFAULT))

    def test_set_spot_7(self):
        surface = tam_io.tam_surface.TAMSurface(5, 5, "&", RED, GREEN)
        surface.set_spot(3, 2, "C", DEFAULT, LIGHT_RED)
        self.assertEqual(surface.get_spot(3, 2), ("C", DEFAULT, LIGHT_RED))

    def test_set_spot_8(self):
        surface = tam_io.tam_surface.TAMSurface(5, 5, "&", RED, GREEN)
        surface.set_spot(3, 2, tam_io.tam_surface.ALPHA_CHAR, ALPHA, ALPHA, True)
        self.assertEqual(surface.get_spot(3, 2), (tam_io.tam_surface.ALPHA_CHAR, ALPHA, ALPHA))

    def test_set_spot_9(self):
        surface = tam_io.tam_surface.TAMSurface(5, 5, "&", RED, GREEN)
        surface.set_spot(3, 2, tam_io.tam_surface.ALPHA_CHAR, ALPHA, ALPHA)
        self.assertEqual(surface.get_spot(3, 2), ("&", RED, GREEN))

    def test_get_spot(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "&", RED, GREEN)

        surface.set_spot(0, 0, "A", GREEN, YELLOW)
        surface.set_spot(1, 0, "B", YELLOW, BLUE)
        surface.set_spot(4, 0, "C", BLUE, PURPLE)
        surface.set_spot(3, 2, "D", PURPLE, AQUA)
        surface.set_spot(4, 5, "E", AQUA, WHITE)

        self.assertEqual(surface.get_spot(0, 0), ("A", GREEN, YELLOW))
        self.assertEqual(surface.get_spot(1, 0), ("B", YELLOW, BLUE))
        self.assertEqual(surface.get_spot(4, 0), ("C", BLUE, PURPLE))
        self.assertEqual(surface.get_spot(3, 2), ("D", PURPLE, AQUA))
        self.assertEqual(surface.get_spot(4, 5), ("E", AQUA, WHITE))

        self.assertEqual(surface.get_spot(0, 6), None)
        self.assertEqual(surface.get_spot(-1, 0), None)

    def test_get_from_raw_spot(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "&", RED, GREEN)

        surface.set_spot(0, 0, "A", GREEN, YELLOW)
        surface.set_spot(1, 0, "B", YELLOW, BLUE)
        surface.set_spot(4, 0, "C", BLUE, PURPLE)
        surface.set_spot(3, 2, "D", PURPLE, AQUA)
        surface.set_spot(4, 5, "E", AQUA, WHITE)

        self.assertEqual(surface.get_from_raw_spot(0), ("A", GREEN, YELLOW))
        self.assertEqual(surface.get_from_raw_spot(1), ("B", YELLOW, BLUE))
        self.assertEqual(surface.get_from_raw_spot(4), ("C", BLUE, PURPLE))
        self.assertEqual(surface.get_from_raw_spot(13), ("D", PURPLE, AQUA))
        self.assertEqual(surface.get_from_raw_spot(29), ("E", AQUA, WHITE))

        self.assertEqual(surface.get_from_raw_spot(-1), None)
        self.assertEqual(surface.get_from_raw_spot(30), None)

    def test_draw_onto(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        surface.draw_onto(surface2)
        self.assertEqual(str(surface), "BBBAA\n" * 4 + "AAAAA\nAAAAA")

    def test_draw_onto_2(self):
        surface = tam_io.tam_surface.TAMSurface(6, 7, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        surface.draw_onto(surface2, -1, -1)
        self.assertEqual(str(surface), ("BBAAAA\n" * 3 + "AAAAAA\n" * 4)[:-1])

    def test_draw_onto_3(self):
        surface = tam_io.tam_surface.TAMSurface(6, 7, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        surface.draw_onto(surface2, 0, 0, 1, 1)
        self.assertEqual(str(surface), ("BBAAAA\n" * 3 + "AAAAAA\n" * 4)[:-1])

    def test_draw_onto_4(self):
        surface = tam_io.tam_surface.TAMSurface(6, 7, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        surface.draw_onto(surface2, -1, -1, 1, 1)
        self.assertEqual(str(surface), ("BAAAAA\n" * 2 + "AAAAAA\n" * 5)[:-1])

    def test_draw_onto_5(self):
        surface = tam_io.tam_surface.TAMSurface(6, 7, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        surface.draw_onto(surface2, 0, 0, 2, 2)
        self.assertEqual(str(surface), ("BAAAAA\n" * 2 + "AAAAAA\n" * 5)[:-1])

    def test_draw_onto_6(self):
        surface = tam_io.tam_surface.TAMSurface(6, 7, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        surface.draw_onto(surface2, 8, 8)
        self.assertEqual(str(surface), ("AAAAAA\n" * 7)[:-1])

    def test_draw_onto_7(self):
        surface = tam_io.tam_surface.TAMSurface(6, 7, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        surface.draw_onto(surface2, 5, 6)
        self.assertEqual(str(surface), "AAAAAA\n" * 6 + "AAAAAB")

    def test_draw_onto_8(self):
        surface = tam_io.tam_surface.TAMSurface(6, 7, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        surface.draw_onto(surface2, 1, 1, 0, 0, 2, 2)
        self.assertEqual(str(surface), ("AAAAAA\n" + "ABBAAA\n" * 2 + "AAAAAA\n" * 4)[:-1])

    def test_get_cross_rect(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        self.assertEqual(surface.get_cross_rect(surface2, -2, -1, 0, 0), (0, 0, 2, 1, 1, 3))

    def test_get_cross_rect_2(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", RED, GREEN)

        self.assertEqual(surface.get_cross_rect(surface2, -6, -6, -12, -12, 100, 100), (6, 6, 0, 0, 0, 0))

    def test_replace_alpha_chars_1(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "A", RED, GREEN)
        surface.set_spot(0, 0, tam_io.tam_surface.ALPHA_CHAR, PURPLE, WHITE, True)
        surface.replace_alpha_chars()
        self.assertEqual(surface.get_spot(0, 0), ("A", PURPLE, WHITE))

    def test_replace_alpha_chars_2(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "A", RED, GREEN)
        surface.set_spot(0, 0, tam_io.tam_surface.ALPHA_CHAR, ALPHA, WHITE, True)
        surface.replace_alpha_chars("C")
        self.assertEqual(surface.get_spot(0, 0), ("C", ALPHA, WHITE))

    def test_replace_alpha_chars_3(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, tam_io.tam_surface.ALPHA_CHAR, RED, GREEN)
        surface.set_spot(0, 0, tam_io.tam_surface.ALPHA_CHAR, ALPHA, WHITE, True)
        surface.replace_alpha_chars(tam_io.tam_surface.ALPHA_CHAR)
        self.assertEqual(surface.get_spot(0, 0), (" ", ALPHA, WHITE))

    def test_to_bytes_from_bytes(self):
        surface = tam_io.tam_surface.TAMSurface(300, 6, tam_io.tam_surface.ALPHA_CHAR, RED, GREEN)

        for color_code in COLOR_MAP:
            surface.set_spot(color_code + 5, 0, "@", COLOR_MAP[color_code], COLOR_MAP[color_code])

        surface.set_spot(4, 5, "*", Color(1, 1, RGBA(207, 201, 2)), Color(1, 1, RGBA(233, 255, 21)))
        surface.set_spot(4, 7, tam_io.tam_surface.ALPHA_CHAR,
                         Color(1, 2, RGBA(237, 200, 7)),
                         Color(4, 13, RGBA(44, 44, 1)))

        surface_bytes = surface.to_bytes()
        self.assertIsInstance(surface_bytes, bytes)
        surface_2 = tam_io.tam_surface.TAMSurface.from_bytes(bytearray(surface_bytes))
        self.assertIsInstance(surface_2, tam_io.tam_surface.TAMSurface)
        self.assertEqual(surface, surface_2)
