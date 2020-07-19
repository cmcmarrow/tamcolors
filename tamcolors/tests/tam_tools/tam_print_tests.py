# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam
from tamcolors import tam_tools


class TAMPrintTests(unittest.TestCase):
    def test_tam_print(self):
        buffer = tam.tam_buffer.TAMBuffer(6, 5, "@", 1, 2)
        tam_tools.tam_print.tam_print(buffer, 0, 1, "Test", 3, 4)
        self.assertEqual(buffer.get_spot(0, 1), ("T", 3, 4))
        self.assertEqual(buffer.get_spot(1, 1), ("e", 3, 4))
        self.assertEqual(buffer.get_spot(2, 1), ("s", 3, 4))
        self.assertEqual(buffer.get_spot(3, 1), ("t", 3, 4))
        self.assertEqual(buffer.get_spot(4, 1), ("@", 1, 2))

    def test_tam_print_2(self):
        buffer = tam.tam_buffer.TAMBuffer(7, 5, "@", 1, 2)
        buffer.set_spot(3, 1, "E", 8, 9)
        tam_tools.tam_print.tam_print(buffer, 2, 1, "Test", 3, -1)
        self.assertEqual(buffer.get_spot(2, 1), ("T", 3, 2))
        self.assertEqual(buffer.get_spot(3, 1), ("e", 3, 9))
        self.assertEqual(buffer.get_spot(4, 1), ("s", 3, 2))
        self.assertEqual(buffer.get_spot(5, 1), ("t", 3, 2))
        self.assertEqual(buffer.get_spot(6, 1), ("@", 1, 2))

    def test_tam_print_3(self):
        buffer = tam.tam_buffer.TAMBuffer(7, 5, "@", 1, 2)
        buffer.set_spot(3, 1, "E", 8, 9)
        tam_tools.tam_print.tam_print(buffer, 2, 1, "Test\n\tcat", 3, -1)
        self.assertEqual(buffer.get_spot(2, 1), ("T", 3, 2))
        self.assertEqual(buffer.get_spot(3, 1), ("e", 3, 9))
        self.assertEqual(buffer.get_spot(4, 1), ("s", 3, 2))
        self.assertEqual(buffer.get_spot(5, 1), ("t", 3, 2))
        self.assertEqual(buffer.get_spot(6, 1), ("@", 1, 2))
        self.assertEqual(buffer.get_spot(2, 2), (" ", 3, 2))
        self.assertEqual(buffer.get_spot(3, 2), (" ", 3, 2))
        self.assertEqual(buffer.get_spot(4, 2), (" ", 3, 2))
        self.assertEqual(buffer.get_spot(5, 2), (" ", 3, 2))
        self.assertEqual(buffer.get_spot(6, 2), ("c", 3, 2))
        self.assertEqual(buffer.get_spot(7, 2), None)

    def test_tam_print_4(self):
        buffer = tam.tam_buffer.TAMBuffer(7, 5, "@", 1, 2)
        buffer.set_spot(3, 1, "E", 8, 9)
        tam_tools.tam_print.tam_print(buffer, 2, 1, "Test\n\r\tcat", 3, -1)
        self.assertEqual(buffer.get_spot(2, 1), ("T", 3, 2))
        self.assertEqual(buffer.get_spot(3, 1), ("e", 3, 9))
        self.assertEqual(buffer.get_spot(4, 1), ("s", 3, 2))
        self.assertEqual(buffer.get_spot(5, 1), ("t", 3, 2))
        self.assertEqual(buffer.get_spot(6, 1), ("@", 1, 2))
        self.assertEqual(buffer.get_spot(2, 2), (" ", 3, 2))
        self.assertEqual(buffer.get_spot(3, 2), (" ", 3, 2))
        self.assertEqual(buffer.get_spot(4, 2), (" ", 3, 2))
        self.assertEqual(buffer.get_spot(5, 2), (" ", 3, 2))
        self.assertEqual(buffer.get_spot(6, 2), ("c", 3, 2))
        self.assertEqual(buffer.get_spot(7, 2), None)

    def test_tam_print_5(self):
        buffer = tam.tam_buffer.TAMBuffer(7, 5, "@", 1, 2)
        buffer.set_spot(3, 1, "E", 8, 9)
        self.assertRaises(tam_tools.tam_str.TAMStrError,
                          tam_tools.tam_print.tam_print,
                          buffer,
                          2,
                          1,
                          "Test\n\r\tcat",
                          3,
                          -1,
                          error_bad_char=True)
