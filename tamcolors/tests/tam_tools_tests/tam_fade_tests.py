# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam_tools
from tamcolors.tam_io.tam_colors import *


class TAMFilmFadeInTests(unittest.TestCase):
    def test_tam_fade_in(self):
        surface = tam_io.tam_surface.TAMSurface(4, 5, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(4, 5, "&", YELLOW, WHITE)
        film = tam_tools.tam_fade.tam_fade_in(surface, "&", YELLOW, WHITE)

        self.assertEqual(len(film), 24)
        self.assertEqual(surface2, film[0])
        self.assertEqual(surface, film[23])

    def test_tam_fade_in_2(self):
        surface = tam_io.tam_surface.TAMSurface(4, 5, "A", RED, GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(4, 5, "&", YELLOW, WHITE)
        film = tam_tools.tam_fade.tam_fade_in(surface, "&", YELLOW, WHITE, reverse=True)

        self.assertEqual(len(film), 24)
        self.assertEqual(surface, film[0])
        self.assertEqual(surface2, film[23])

    def test_tam_fade_in_3(self):
        surface = tam_io.tam_surface.TAMSurface(2, 3, "A", RED, GREEN)
        surface.set_spot(1, 1, "B", AQUA, LIGHT_RED)
        surface2 = tam_io.tam_surface.TAMSurface(2, 3, "&", YELLOW, WHITE)
        film = tam_tools.tam_fade.tam_fade_in(surface, "&", YELLOW, WHITE)

        self.assertEqual(len(film), 10)
        self.assertEqual(surface2, film[0])
        self.assertEqual(surface, film[9])

    def test_tam_fade_in_4(self):
        surface = tam_io.tam_surface.TAMSurface(2, 3, "A", RED, GREEN)
        surface.set_spot(1, 1, "B", AQUA, LIGHT_RED)
        surface2 = tam_io.tam_surface.TAMSurface(2, 3, "&", YELLOW, WHITE)
        film = tam_tools.tam_fade.tam_fade_in(surface, "&", YELLOW, WHITE, rand=[True])

        self.assertEqual(len(film), 9)
        self.assertEqual(surface2, film[0])
        self.assertEqual(surface, film[8])
