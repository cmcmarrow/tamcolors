# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors.tam_io.tam_colors import*


class TAMBufferTests(unittest.TestCase):
    def test_buffer_init(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 4, "&", RED, GREEN)
        self.assertEqual(str(buffer), ("&&&\n"*4)[:-1])

    def test_buffer_str(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 400, "&", RED, GREEN)
        self.assertEqual(str(buffer), ("&&&\n" * 400)[:-1])

    def test_buffer_str_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 400, "&", RED, GREEN)
        buffer.set_spot(1, 2, tam_io.tam_buffer.ALPHA_CHAR, ALPHA, ALPHA, False)
        self.assertEqual(str(buffer), ("&&&\n" * 400)[:-1])

    def test_buffer_str_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 2, tam_io.tam_buffer.ALPHA_CHAR, RED, GREEN)
        buffer.set_spot(2, 1, "#", ALPHA, ALPHA, False)
        self.assertEqual(str(buffer), "   \n  #")

    def test_buffer_len(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 4, "&", RED, GREEN)
        self.assertEqual(len(buffer), 20)

    def test_buffer_len_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 6, "&", RED, GREEN)
        self.assertEqual(len(buffer), 300)

    def test_buffer_len_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(55, 65, "&", RED, GREEN)
        self.assertEqual(len(buffer), 3575)
        buffer.set_dimensions_and_clear(5, 7)
        self.assertEqual(len(buffer), 35)

    def test_buffer_len_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(0, 50, "&", RED, GREEN)
        self.assertEqual(len(buffer), 0)

    def test_buffer_eq(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        self.assertTrue(buffer == buffer2)

    def test_buffer_eq_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(26, 50, "&", RED, GREEN)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "c", RED, GREEN)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2.set_spot(12, 34, "b", AQUA, WHITE)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_5(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        self.assertFalse(buffer == 34)

    def test_buffer_ne(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        self.assertFalse(buffer != buffer2)

    def test_buffer_ne_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(26, 50, "&", RED, GREEN)
        self.assertTrue(buffer != buffer2)

    def test_buffer_ne_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "c", RED, GREEN)
        self.assertTrue(buffer != buffer2)

    def test_buffer_ne_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "&", RED, GREEN)
        buffer2.set_spot(12, 34, "b", AQUA, WHITE)
        self.assertTrue(buffer != buffer2)

    def test_clear(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", RED, GREEN)
        for y in range(20):
            for x in range(5):
                buffer.set_spot(x, y, "@", LIGHT_RED, LIGHT_GREEN)

        buffer.clear()

        for y in range(20):
            for x in range(5):
                self.assertEqual(buffer.get_spot(x, y), (".", RED, GREEN))
        self.assertEqual(str(buffer), (".....\n" * 20)[:-1])

    def test_get_dimensions(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", RED, GREEN)
        self.assertEqual(buffer.get_dimensions(), (5, 20))

    def test_get_dimensions_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3005, 2200, ".", RED, GREEN)
        self.assertEqual(buffer.get_dimensions(), (3005, 2200))

    def test_get_dimensions_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(0, 1, ".", RED, GREEN)
        self.assertEqual(buffer.get_dimensions(), (0, 1))

    def test_set_dimensions_and_clear(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", RED, GREEN)
        buffer.set_dimensions_and_clear(2, 3)
        self.assertEqual(str(buffer), ("..\n" * 3)[:-1])

    def test_set_dimensions_and_clear_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", RED, GREEN)
        buffer.set_dimensions_and_clear(6, 300)
        self.assertEqual(str(buffer), ("......\n" * 300)[:-1])

    def test_get_defaults(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", RED, GREEN)
        buffer.get_defaults()
        self.assertEqual(buffer.get_defaults(), (".", RED, GREEN))

    def test_set_defaults_and_clear(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", RED, GREEN)
        buffer.set_defaults_and_clear("L", PURPLE, AQUA)
        for y in range(20):
            for x in range(5):
                self.assertEqual(buffer.get_spot(x, y), ("L", PURPLE, AQUA))

    def test_set_defaults_and_clear_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 22, ".", RED, GREEN)
        buffer.set_defaults_and_clear("A", WHITE, GREEN)
        for y in range(22):
            for x in range(50):
                self.assertEqual(buffer.get_spot(x, y), ("A", WHITE, GREEN))

    def test_get_raw_buffers(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 22, ".", RED, GREEN)
        length = 50 * 22
        self.assertEqual((["."] * length, [RED] * length, [GREEN] * length), buffer.get_raw_buffers())

    def test_get_raw_buffers_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(501, 222, ".", RED, GREEN)
        length = 501 * 222
        self.assertEqual((["."] * length, [RED] * length, [GREEN] * length), buffer.get_raw_buffers())

    def test_copy(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 22, ".", RED, GREEN)
        buffer2 = buffer.copy()

        for y in range(22):
            for x in range(50):
                buffer2.set_spot(x, y, "H", PURPLE, GREEN)

        self.assertNotEqual(str(buffer), str(buffer2))

    def test_copy_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(55, 23, ".", RED, GREEN)
        buffer2 = buffer.copy()

        for y in range(23):
            for x in range(55):
                buffer2.set_spot(x, y, "H", PURPLE, GREEN)

        self.assertNotEqual(str(buffer), str(buffer2))

    def test_get_raw_spot(self):
        buffer = tam_io.tam_buffer.TAMBuffer(55, 23, ".", RED, GREEN)
        raw_spots = []

        for y in range(23):
            for x in range(55):
                raw_spot = buffer.get_raw_spot(x, y)
                self.assertTrue(raw_spot not in raw_spots)
                raw_spots.append(raw_spot)

        self.assertTrue(all([i in range(0, 55 * 23) for i in raw_spots]))

    def test_set_spot(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 4, "&", RED, GREEN)
        for y in range(4):
            buffer.set_spot(0, y, 'T', RED, GREEN)
        self.assertEqual(str(buffer), ("T&&\n"*4)[:-1])

    def test_set_spot_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 4, "&", RED, GREEN)
        for y in range(4):
            buffer.set_spot(y % 3, y, "T", RED, GREEN)
        self.assertEqual(str(buffer), "T&&\n&T&\n&&T\nT&&")

    def test_set_spot_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", RED, GREEN)
        for y in range(5):
            for x in range(5):
                buffer.set_spot(x, y, str(x), RED, GREEN)
        self.assertEqual(str(buffer), ("01234\n"*5)[:-1])

    def test_set_spot_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", RED, GREEN)
        buffer.set_spot(0, 1, "C", AQUA, AQUA)
        self.assertEqual(buffer.get_spot(0, 1), ("C", AQUA, AQUA))

    def test_set_spot_5(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", RED, GREEN)
        buffer.set_spot(3, 2, "A", BLUE, ALPHA)
        buffer.set_spot(3, 2, "C", ALPHA, AQUA)
        self.assertEqual(buffer.get_spot(3, 2), ("C", BLUE, AQUA))

    def test_set_spot_6(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", RED, GREEN)
        buffer.set_spot(3, 2, "A", BLUE, DEFAULT)
        buffer.set_spot(3, 2, "C", DEFAULT, DEFAULT)
        self.assertEqual(buffer.get_spot(3, 2), ("C", DEFAULT, DEFAULT))

    def test_set_spot_7(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", RED, GREEN)
        buffer.set_spot(3, 2, "C", DEFAULT, LIGHT_RED)
        self.assertEqual(buffer.get_spot(3, 2), ("C", DEFAULT, LIGHT_RED))

    def test_set_spot_8(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", RED, GREEN)
        buffer.set_spot(3, 2, tam_io.tam_buffer.ALPHA_CHAR, ALPHA, ALPHA, True)
        self.assertEqual(buffer.get_spot(3, 2), (tam_io.tam_buffer.ALPHA_CHAR, ALPHA, ALPHA))

    def test_set_spot_9(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", RED, GREEN)
        buffer.set_spot(3, 2, tam_io.tam_buffer.ALPHA_CHAR, ALPHA, ALPHA)
        self.assertEqual(buffer.get_spot(3, 2), ("&", RED, GREEN))

    def test_get_spot(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "&", RED, GREEN)

        buffer.set_spot(0, 0, "A", GREEN, YELLOW)
        buffer.set_spot(1, 0, "B", YELLOW, BLUE)
        buffer.set_spot(4, 0, "C", BLUE, PURPLE)
        buffer.set_spot(3, 2, "D", PURPLE, AQUA)
        buffer.set_spot(4, 5, "E", AQUA, WHITE)

        self.assertEqual(buffer.get_spot(0, 0), ("A", GREEN, YELLOW))
        self.assertEqual(buffer.get_spot(1, 0), ("B", YELLOW, BLUE))
        self.assertEqual(buffer.get_spot(4, 0), ("C", BLUE, PURPLE))
        self.assertEqual(buffer.get_spot(3, 2), ("D", PURPLE, AQUA))
        self.assertEqual(buffer.get_spot(4, 5), ("E", AQUA, WHITE))

        self.assertEqual(buffer.get_spot(0, 6), None)
        self.assertEqual(buffer.get_spot(-1, 0), None)

    def test_get_from_raw_spot(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "&", RED, GREEN)

        buffer.set_spot(0, 0, "A", GREEN, YELLOW)
        buffer.set_spot(1, 0, "B", YELLOW, BLUE)
        buffer.set_spot(4, 0, "C", BLUE, PURPLE)
        buffer.set_spot(3, 2, "D", PURPLE, AQUA)
        buffer.set_spot(4, 5, "E", AQUA, WHITE)

        self.assertEqual(buffer.get_from_raw_spot(0), ("A", GREEN, YELLOW))
        self.assertEqual(buffer.get_from_raw_spot(1), ("B", YELLOW, BLUE))
        self.assertEqual(buffer.get_from_raw_spot(4), ("C", BLUE, PURPLE))
        self.assertEqual(buffer.get_from_raw_spot(13), ("D", PURPLE, AQUA))
        self.assertEqual(buffer.get_from_raw_spot(29), ("E", AQUA, WHITE))

        self.assertEqual(buffer.get_from_raw_spot(-1), None)
        self.assertEqual(buffer.get_from_raw_spot(30), None)

    def test_draw_onto(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        buffer.draw_onto(buffer2)
        self.assertEqual(str(buffer), "BBBAA\n" * 4 + "AAAAA\nAAAAA")

    def test_draw_onto_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        buffer.draw_onto(buffer2, -1, -1)
        self.assertEqual(str(buffer), ("BBAAAA\n" * 3 + "AAAAAA\n" * 4)[:-1])

    def test_draw_onto_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        buffer.draw_onto(buffer2, 0, 0, 1, 1)
        self.assertEqual(str(buffer), ("BBAAAA\n" * 3 + "AAAAAA\n" * 4)[:-1])

    def test_draw_onto_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        buffer.draw_onto(buffer2, -1, -1, 1, 1)
        self.assertEqual(str(buffer), ("BAAAAA\n" * 2 + "AAAAAA\n" * 5)[:-1])

    def test_draw_onto_5(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        buffer.draw_onto(buffer2, 0, 0, 2, 2)
        self.assertEqual(str(buffer), ("BAAAAA\n" * 2 + "AAAAAA\n" * 5)[:-1])

    def test_draw_onto_6(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        buffer.draw_onto(buffer2, 8, 8)
        self.assertEqual(str(buffer), ("AAAAAA\n" * 7)[:-1])

    def test_draw_onto_7(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        buffer.draw_onto(buffer2, 5, 6)
        self.assertEqual(str(buffer), "AAAAAA\n" * 6 + "AAAAAB")

    def test_draw_onto_8(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        buffer.draw_onto(buffer2, 1, 1, 0, 0, 2, 2)
        self.assertEqual(str(buffer), ("AAAAAA\n" + "ABBAAA\n" * 2 + "AAAAAA\n" * 4)[:-1])

    def test_get_cross_rect(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        self.assertEqual(buffer.get_cross_rect(buffer2, -2, -1, 0, 0), (0, 0, 2, 1, 1, 3))

    def test_get_cross_rect_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", RED, GREEN)

        self.assertEqual(buffer.get_cross_rect(buffer2, -6, -6, -12, -12, 100, 100), (6, 6, 0, 0, 0, 0))

    def test_replace_alpha_chars_1(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", RED, GREEN)
        buffer.set_spot(0, 0, tam_io.tam_buffer.ALPHA_CHAR, PURPLE, WHITE, True)
        buffer.replace_alpha_chars()
        self.assertEqual(buffer.get_spot(0, 0), ("A", PURPLE, WHITE))

    def test_replace_alpha_chars_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", RED, GREEN)
        buffer.set_spot(0, 0, tam_io.tam_buffer.ALPHA_CHAR, ALPHA, WHITE, True)
        buffer.replace_alpha_chars("C")
        self.assertEqual(buffer.get_spot(0, 0), ("C", ALPHA, WHITE))

    def test_replace_alpha_chars_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, tam_io.tam_buffer.ALPHA_CHAR, RED, GREEN)
        buffer.set_spot(0, 0, tam_io.tam_buffer.ALPHA_CHAR, ALPHA, WHITE, True)
        buffer.replace_alpha_chars(tam_io.tam_buffer.ALPHA_CHAR)
        self.assertEqual(buffer.get_spot(0, 0), (" ", ALPHA, WHITE))
