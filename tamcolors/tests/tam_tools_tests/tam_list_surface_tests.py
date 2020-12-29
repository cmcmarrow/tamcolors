# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam_tools
from tamcolors.tam_io.tam_colors import *


class TAMListSurfaceTests(unittest.TestCase):
    def test_tam_list_surface(self):
        surface = [["1", "2", "3"],
                   ["4", "5", "6"]]

        tam_surface = tam_io.tam_surface.TAMSurface(3, 2, " ", RED, GREEN)
        for i in range(3):
            tam_surface.set_spot(i, 0, str(i + 1), RED, GREEN)
            tam_surface.set_spot(i, 1, str(i + 4), RED, GREEN)

        ret_tam_surface = tam_tools.tam_list_surface.tam_list_surface(surface, RED, GREEN)

        self.assertEqual(ret_tam_surface, tam_surface)

    def test_tam_list_surface_2(self):
        surface = [["1", "2", "3"],
                   ["4", "5", "6"],
                   ["1", "2", "3"]]

        tam_surface = tam_io.tam_surface.TAMSurface(3, 3, " ", RED, GREEN)
        for i in range(3):
            tam_surface.set_spot(i, 0, str(i + 1), RED, GREEN)
            tam_surface.set_spot(i, 1, str(i + 4), RED, GREEN)
            tam_surface.set_spot(i, 2, str(i + 1), RED, GREEN)

        ret_tam_surface = tam_tools.tam_list_surface.tam_list_surface(surface, RED, GREEN)

        self.assertEqual(ret_tam_surface, tam_surface)

    def test_tam_list_surface_3(self):
        surface = [["1", "2", "3"],
                   ["4", "5", "6"]]

        foreground_colors = [[RED, GREEN, YELLOW],
                             [BLUE, PURPLE, AQUA]]

        tam_surface = tam_io.tam_surface.TAMSurface(3, 2, " ", RED, GREEN)
        for i in range(3):
            tam_surface.set_spot(i, 0, str(i + 1), COLORS[i + 1], GREEN)
            tam_surface.set_spot(i, 1, str(i + 4), COLORS[i + 4], GREEN)

        ret_tam_surface = tam_tools.tam_list_surface.tam_list_surface(surface, foreground_colors, GREEN)

        self.assertEqual(ret_tam_surface, tam_surface)

    def test_tam_list_surface_4(self):
        surface = [["1", "2", "3"],
                   ["4", "5", "6"]]

        background_colors = [[RED, GREEN, YELLOW],
                             [BLUE, PURPLE, AQUA]]

        tam_surface = tam_io.tam_surface.TAMSurface(3, 2, " ", RED, GREEN)
        for i in range(3):
            tam_surface.set_spot(i, 0, str(i + 1), RED, COLORS[i + 1])
            tam_surface.set_spot(i, 1, str(i + 4), RED, COLORS[i + 4])

        ret_tam_surface = tam_tools.tam_list_surface.tam_list_surface(surface, RED, background_colors)

        self.assertEqual(ret_tam_surface, tam_surface)

    def test_tam_list_surface_5(self):
        surface = [["1", "2", "3"],
                   ["4", "5", "6"]]

        foreground_colors = [[GREEN, BLUE, AQUA],
                             [GRAY, LIGHT_GREEN, LIGHT_BLUE]]

        background_colors = [[RED, GREEN, YELLOW],
                             [BLUE, PURPLE, AQUA]]

        tam_surface = tam_io.tam_surface.TAMSurface(3, 2, " ", RED, GREEN)
        for i in range(3):
            tam_surface.set_spot(i, 0, str(i + 1), COLORS[(i + 1) * 2], COLORS[i + 1])
            tam_surface.set_spot(i, 1, str(i + 4), COLORS[(i + 4) * 2], COLORS[i + 4])

        ret_tam_surface = tam_tools.tam_list_surface.tam_list_surface(surface, foreground_colors, background_colors)

        self.assertEqual(ret_tam_surface, tam_surface)
