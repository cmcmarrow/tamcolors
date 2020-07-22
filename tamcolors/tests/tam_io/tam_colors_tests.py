# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


class TAMColorTests(unittest.TestCase):
    def test_colors(self):
        self.assertEqual(tam_io.tam_colors.BLACK, 0)
        self.assertEqual(tam_io.tam_colors.BLUE, 1)
        self.assertEqual(tam_io.tam_colors.GREEN, 2)
        self.assertEqual(tam_io.tam_colors.AQUA, 3)
        self.assertEqual(tam_io.tam_colors.RED, 4)
        self.assertEqual(tam_io.tam_colors.PURPLE, 5)
        self.assertEqual(tam_io.tam_colors.YELLOW, 6)
        self.assertEqual(tam_io.tam_colors.WHITE, 7)
        self.assertEqual(tam_io.tam_colors.GRAY, 8)
        self.assertEqual(tam_io.tam_colors.LIGHT_BLUE, 9)
        self.assertEqual(tam_io.tam_colors.LIGHT_GREEN, 10)
        self.assertEqual(tam_io.tam_colors.LIGHT_AQUA, 11)
        self.assertEqual(tam_io.tam_colors.LIGHT_RED, 12)
        self.assertEqual(tam_io.tam_colors.LIGHT_PURPLE, 13)
        self.assertEqual(tam_io.tam_colors.LIGHT_YELLOW, 14)
        self.assertEqual(tam_io.tam_colors.LIGHT_WHITE, 15)