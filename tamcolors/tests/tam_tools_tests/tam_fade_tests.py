# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam_tools
from tamcolors.tam_io.tam_colors import *


class TAMFilmFadeInTests(unittest.TestCase):
    def test_tam_fade_in(self):
        buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(4, 5, "&", YELLOW, WHITE)
        film = tam_tools.tam_fade.tam_fade_in(buffer, "&", YELLOW, WHITE)

        self.assertEqual(len(film), 24)
        self.assertEqual(buffer2, film[0])
        self.assertEqual(buffer, film[23])

    def test_tam_fade_in_2(self):
        buffer = tam_io.tam_buffer.TAMBuffer(4, 5, "A", RED, GREEN)
        buffer2 = tam_io.tam_buffer.TAMBuffer(4, 5, "&", YELLOW, WHITE)
        film = tam_tools.tam_fade.tam_fade_in(buffer, "&", YELLOW, WHITE, reverse=True)

        self.assertEqual(len(film), 24)
        self.assertEqual(buffer, film[0])
        self.assertEqual(buffer2, film[23])

    def test_tam_fade_in_3(self):
        buffer = tam_io.tam_buffer.TAMBuffer(2, 3, "A", RED, GREEN)
        buffer.set_spot(1, 1, "B", AQUA, LIGHT_RED)
        buffer2 = tam_io.tam_buffer.TAMBuffer(2, 3, "&", YELLOW, WHITE)
        film = tam_tools.tam_fade.tam_fade_in(buffer, "&", YELLOW, WHITE)

        self.assertEqual(len(film), 10)
        self.assertEqual(buffer2, film[0])
        self.assertEqual(buffer, film[9])

    def test_tam_fade_in_4(self):
        buffer = tam_io.tam_buffer.TAMBuffer(2, 3, "A", RED, GREEN)
        buffer.set_spot(1, 1, "B", AQUA, LIGHT_RED)
        buffer2 = tam_io.tam_buffer.TAMBuffer(2, 3, "&", YELLOW, WHITE)
        film = tam_tools.tam_fade.tam_fade_in(buffer, "&", YELLOW, WHITE, rand=[True])

        self.assertEqual(len(film), 9)
        self.assertEqual(buffer2, film[0])
        self.assertEqual(buffer, film[8])
