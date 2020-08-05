# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


class TAMBufferTests(unittest.TestCase):
    def test_buffer_init(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 4, "&", 1, 2)
        self.assertEqual(str(buffer), ("&&&\n"*4)[:-1])

    def test_buffer_str(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 400, "&", 1, 2)
        self.assertEqual(str(buffer), ("&&&\n" * 400)[:-1])

    def test_buffer_str_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 400, "&", 1, 2)
        buffer.set_spot(1, 2, tam_io.tam_buffer.ALPHA_CHAR, -2, -2, False)
        self.assertEqual(str(buffer), ("&&&\n" * 400)[:-1])

    def test_buffer_str_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 2, tam_io.tam_buffer.ALPHA_CHAR, 1, 2)
        buffer.set_spot(2, 1, "#", -2, -2, False)
        self.assertEqual(str(buffer), "   \n  #")

    def test_buffer_len(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 4, "&", 1, 2)
        self.assertEqual(len(buffer), 20)

    def test_buffer_len_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 6, "&", 1, 2)
        self.assertEqual(len(buffer), 300)

    def test_buffer_len_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(55, 65, "&", 1, 2)
        self.assertEqual(len(buffer), 3575)
        buffer.set_dimensions_and_clear(5, 7)
        self.assertEqual(len(buffer), 35)

    def test_buffer_len_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(0, 50, "&", 1, 2)
        self.assertEqual(len(buffer), 0)

    def test_buffer_eq(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        self.assertTrue(buffer == buffer2)

    def test_buffer_eq_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(26, 50, "&", 1, 2)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "c", 1, 2)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2.set_spot(12, 34, "b", 6, 7)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_5(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        self.assertFalse(buffer == 34)

    def test_buffer_ne(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        self.assertFalse(buffer != buffer2)

    def test_buffer_ne_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(26, 50, "&", 1, 2)
        self.assertTrue(buffer != buffer2)

    def test_buffer_ne_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "c", 1, 2)
        self.assertTrue(buffer != buffer2)

    def test_buffer_ne_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2.set_spot(12, 34, "b", 6, 7)
        self.assertTrue(buffer != buffer2)

    def test_clear(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        for y in range(20):
            for x in range(5):
                buffer.set_spot(x, y, "@", 9, 10)

        buffer.clear()

        for y in range(20):
            for x in range(5):
                self.assertEqual(buffer.get_spot(x, y), (".", 1, 2))
        self.assertEqual(str(buffer), (".....\n" * 20)[:-1])

    def test_get_dimensions(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        self.assertEqual(buffer.get_dimensions(), (5, 20))

    def test_get_dimensions_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3005, 2200, ".", 1, 2)
        self.assertEqual(buffer.get_dimensions(), (3005, 2200))

    def test_get_dimensions_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(0, 1, ".", 1, 2)
        self.assertEqual(buffer.get_dimensions(), (0, 1))

    def test_set_dimensions_and_clear(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        buffer.set_dimensions_and_clear(2, 3)
        self.assertEqual(str(buffer), ("..\n" * 3)[:-1])

    def test_set_dimensions_and_clear_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        buffer.set_dimensions_and_clear(6, 300)
        self.assertEqual(str(buffer), ("......\n" * 300)[:-1])

    def test_get_defaults(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        buffer.get_defaults()
        self.assertEqual(buffer.get_defaults(), (".", 1, 2))

    def test_set_defaults_and_clear(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        buffer.set_defaults_and_clear("L", 5, 6)
        for y in range(20):
            for x in range(5):
                self.assertEqual(buffer.get_spot(x, y), ("L", 5, 6))

    def test_set_defaults_and_clear_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 22, ".", 1, 2)
        buffer.set_defaults_and_clear("A", 7, 2)
        for y in range(22):
            for x in range(50):
                self.assertEqual(buffer.get_spot(x, y), ("A", 7, 2))

    def test_get_raw_buffers(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 22, ".", 1, 2)
        length = 50 * 22
        self.assertEqual((["."] * length, [1] * length, [2] * length), buffer.get_raw_buffers())

    def test_get_raw_buffers_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(501, 222, ".", 1, 2)
        length = 501 * 222
        self.assertEqual((["."] * length, [1] * length, [2] * length), buffer.get_raw_buffers())

    def test_copy(self):
        buffer = tam_io.tam_buffer.TAMBuffer(50, 22, ".", 1, 2)
        buffer2 = buffer.copy()

        for y in range(22):
            for x in range(50):
                buffer2.set_spot(x, y, "H", 5, 2)

        self.assertNotEqual(str(buffer), str(buffer2))

    def test_copy_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(55, 23, ".", 1, 2)
        buffer2 = buffer.copy()

        for y in range(23):
            for x in range(55):
                buffer2.set_spot(x, y, "H", 5, 2)

        self.assertNotEqual(str(buffer), str(buffer2))

    def test_get_raw_spot(self):
        buffer = tam_io.tam_buffer.TAMBuffer(55, 23, ".", 1, 2)
        raw_spots = []

        for y in range(23):
            for x in range(55):
                raw_spot = buffer.get_raw_spot(x, y)
                self.assertTrue(raw_spot not in raw_spots)
                raw_spots.append(raw_spot)

        self.assertTrue(all([i in range(0, 55 * 23) for i in raw_spots]))

    def test_set_spot(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 4, "&", 1, 2)
        for y in range(4):
            buffer.set_spot(0, y, 'T', 1, 2)
        self.assertEqual(str(buffer), ("T&&\n"*4)[:-1])

    def test_set_spot_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(3, 4, "&", 1, 2)
        for y in range(4):
            buffer.set_spot(y % 3, y, "T", 1, 2)
        self.assertEqual(str(buffer), "T&&\n&T&\n&&T\nT&&")

    def test_set_spot_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        for y in range(5):
            for x in range(5):
                buffer.set_spot(x, y, str(x), 1, 2)
        self.assertEqual(str(buffer), ("01234\n"*5)[:-1])

    def test_set_spot_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        buffer.set_spot(0, 1, "C", -2, -2)
        self.assertEqual(buffer.get_spot(0, 1), ("C", 1, 2))

    def test_set_spot_5(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        buffer.set_spot(3, 2, "A", 4, -2)
        buffer.set_spot(3, 2, "C", -2, -2)
        self.assertEqual(buffer.get_spot(3, 2), ("C", 4, 2))

    def test_set_spot_6(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        buffer.set_spot(3, 2, "A", 4, -1)
        buffer.set_spot(3, 2, "C", -1, -1)
        self.assertEqual(buffer.get_spot(3, 2), ("C", -1, -1))

    def test_set_spot_7(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        buffer.set_spot(3, 2, "C", -1, 9)
        self.assertEqual(buffer.get_spot(3, 2), ("C", -1, 9))

    def test_set_spot_8(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        buffer.set_spot(3, 2, tam_io.tam_buffer.ALPHA_CHAR, -2, -2, False)
        self.assertEqual(buffer.get_spot(3, 2), (tam_io.tam_buffer.ALPHA_CHAR, -2, -2))

    def test_set_spot_9(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        buffer.set_spot(3, 2, tam_io.tam_buffer.ALPHA_CHAR, -2, -2)
        self.assertEqual(buffer.get_spot(3, 2), ("&", 1, 2))

    def test_get_spot(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "&", 1, 2)

        buffer.set_spot(0, 0, "A", 2, 3)
        buffer.set_spot(1, 0, "B", 3, 4)
        buffer.set_spot(4, 0, "C", 4, 5)
        buffer.set_spot(3, 2, "D", 5, 6)
        buffer.set_spot(4, 5, "E", 6, 7)

        self.assertEqual(buffer.get_spot(0, 0), ("A", 2, 3))
        self.assertEqual(buffer.get_spot(1, 0), ("B", 3, 4))
        self.assertEqual(buffer.get_spot(4, 0), ("C", 4, 5))
        self.assertEqual(buffer.get_spot(3, 2), ("D", 5, 6))
        self.assertEqual(buffer.get_spot(4, 5), ("E", 6, 7))

        self.assertEqual(buffer.get_spot(0, 6), None)
        self.assertEqual(buffer.get_spot(-1, 0), None)

    def test_get_from_raw_spot(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "&", 1, 2)

        buffer.set_spot(0, 0, "A", 2, 3)
        buffer.set_spot(1, 0, "B", 3, 4)
        buffer.set_spot(4, 0, "C", 4, 5)
        buffer.set_spot(3, 2, "D", 5, 6)
        buffer.set_spot(4, 5, "E", 6, 7)

        self.assertEqual(buffer.get_from_raw_spot(0), ("A", 2, 3))
        self.assertEqual(buffer.get_from_raw_spot(1), ("B", 3, 4))
        self.assertEqual(buffer.get_from_raw_spot(4), ("C", 4, 5))
        self.assertEqual(buffer.get_from_raw_spot(13), ("D", 5, 6))
        self.assertEqual(buffer.get_from_raw_spot(29), ("E", 6, 7))

        self.assertEqual(buffer.get_from_raw_spot(-1), None)
        self.assertEqual(buffer.get_from_raw_spot(30), None)

    def test_draw_onto(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2)
        self.assertEqual(str(buffer), "BBBAA\n" * 4 + "AAAAA\nAAAAA")

    def test_draw_onto_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, -1, -1)
        self.assertEqual(str(buffer), ("BBAAAA\n" * 3 + "AAAAAA\n" * 4)[:-1])

    def test_draw_onto_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 0, 0, 1, 1)
        self.assertEqual(str(buffer), ("BBAAAA\n" * 3 + "AAAAAA\n" * 4)[:-1])

    def test_draw_onto_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, -1, -1, 1, 1)
        self.assertEqual(str(buffer), ("BAAAAA\n" * 2 + "AAAAAA\n" * 5)[:-1])

    def test_draw_onto_5(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 0, 0, 2, 2)
        self.assertEqual(str(buffer), ("BAAAAA\n" * 2 + "AAAAAA\n" * 5)[:-1])

    def test_draw_onto_6(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 8, 8)
        self.assertEqual(str(buffer), ("AAAAAA\n" * 7)[:-1])

    def test_draw_onto_7(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 5, 6)
        self.assertEqual(str(buffer), "AAAAAA\n" * 6 + "AAAAAB")

    def test_draw_onto_8(self):
        buffer = tam_io.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 1, 1, 0, 0, 2, 2)
        self.assertEqual(str(buffer), ("AAAAAA\n" + "ABBAAA\n" * 2 + "AAAAAA\n" * 4)[:-1])

    def test_get_cross_rect(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        self.assertEqual(buffer.get_cross_rect(buffer2, -2, -1, 0, 0), (0, 0, 2, 1, 1, 3))

    def test_get_cross_rect_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam_io.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        self.assertEqual(buffer.get_cross_rect(buffer2, -6, -6, -12, -12, 100, 100), (6, 6, 0, 0, 0, 0))

    def test_replace_alpha_chars_1(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer.set_spot(0, 0, tam_io.tam_buffer.ALPHA_CHAR, 5, 7, False)
        buffer.replace_alpha_chars()
        self.assertEqual(buffer.get_spot(0, 0), ("A", 5, 7))

    def test_replace_alpha_chars_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer.set_spot(0, 0, tam_io.tam_buffer.ALPHA_CHAR, -2, 7, False)
        buffer.replace_alpha_chars("C")
        self.assertEqual(buffer.get_spot(0, 0), ("C", -2, 7))

    def test_replace_alpha_chars_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(5, 6, tam_io.tam_buffer.ALPHA_CHAR, 1, 2)
        buffer.set_spot(0, 0, tam_io.tam_buffer.ALPHA_CHAR, -2, 7, False)
        buffer.replace_alpha_chars(tam_io.tam_buffer.ALPHA_CHAR)
        self.assertEqual(buffer.get_spot(0, 0), (" ", -2, 7))
