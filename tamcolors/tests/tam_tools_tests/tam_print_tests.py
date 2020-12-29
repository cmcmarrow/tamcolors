# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam_tools
from tamcolors.tam_io.tam_colors import *


class TAMPrintTests(unittest.TestCase):
    def test_tam_print(self):
        surface = tam_io.tam_surface.TAMSurface(6, 5, "@", RED, GREEN)
        tam_tools.tam_print.tam_print(surface, 0, 1, "Test", YELLOW, BLUE)
        self.assertEqual(surface.get_spot(0, 1), ("T", YELLOW, BLUE))
        self.assertEqual(surface.get_spot(1, 1), ("e", YELLOW, BLUE))
        self.assertEqual(surface.get_spot(2, 1), ("s", YELLOW, BLUE))
        self.assertEqual(surface.get_spot(3, 1), ("t", YELLOW, BLUE))
        self.assertEqual(surface.get_spot(4, 1), ("@", RED, GREEN))

    def test_tam_print_2(self):
        surface = tam_io.tam_surface.TAMSurface(7, 5, "@", RED, GREEN)
        surface.set_spot(3, 1, "E", GRAY, LIGHT_RED)
        tam_tools.tam_print.tam_print(surface, 2, 1, "Test", YELLOW, ALPHA)
        self.assertEqual(surface.get_spot(2, 1), ("T", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(3, 1), ("e", YELLOW, LIGHT_RED))
        self.assertEqual(surface.get_spot(4, 1), ("s", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(5, 1), ("t", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(6, 1), ("@", RED, GREEN))

    def test_tam_print_3(self):
        surface = tam_io.tam_surface.TAMSurface(7, 5, "@", RED, GREEN)
        surface.set_spot(3, 1, "E", GRAY, LIGHT_RED)
        tam_tools.tam_print.tam_print(surface, 2, 1, "Test\n\tcat", YELLOW, ALPHA)
        self.assertEqual(surface.get_spot(2, 1), ("T", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(3, 1), ("e", YELLOW, LIGHT_RED))
        self.assertEqual(surface.get_spot(4, 1), ("s", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(5, 1), ("t", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(6, 1), ("@", RED, GREEN))
        self.assertEqual(surface.get_spot(2, 2), (" ", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(3, 2), (" ", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(4, 2), (" ", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(5, 2), (" ", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(6, 2), ("c", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(7, 2), None)

    def test_tam_print_4(self):
        surface = tam_io.tam_surface.TAMSurface(7, 5, "@", RED, GREEN)
        surface.set_spot(3, 1, "E", GRAY, LIGHT_RED)
        tam_tools.tam_print.tam_print(surface, 2, 1, "Test\n\r\tcat", YELLOW, ALPHA)
        self.assertEqual(surface.get_spot(2, 1), ("T", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(3, 1), ("e", YELLOW, LIGHT_RED))
        self.assertEqual(surface.get_spot(4, 1), ("s", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(5, 1), ("t", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(6, 1), ("@", RED, GREEN))
        self.assertEqual(surface.get_spot(2, 2), (" ", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(3, 2), (" ", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(4, 2), (" ", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(5, 2), (" ", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(6, 2), ("c", YELLOW, GREEN))
        self.assertEqual(surface.get_spot(7, 2), None)

    def test_tam_print_5(self):
        surface = tam_io.tam_surface.TAMSurface(7, 5, "@", RED, GREEN)
        surface.set_spot(3, 1, "E", GRAY, LIGHT_RED)
        self.assertRaises(tam_tools.tam_str.TAMStrError,
                          tam_tools.tam_print.tam_print,
                          surface,
                          2,
                          1,
                          "Test\n\r\tcat",
                          3,
                          -1,
                          error_bad_char=True)
