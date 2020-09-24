# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam_tools
from tamcolors.tam_io.tam_colors import *


class TAMListBufferTests(unittest.TestCase):
    def test_tam_list_buffer(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 2, " ", RED, GREEN)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), RED, GREEN)
            tam_buffer.set_spot(i, 1, str(i + 4), RED, GREEN)

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, RED, GREEN)

        self.assertEqual(ret_tam_buffer, tam_buffer)

    def test_tam_list_buffer_2(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"],
                  ["1", "2", "3"]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 3, " ", RED, GREEN)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), RED, GREEN)
            tam_buffer.set_spot(i, 1, str(i + 4), RED, GREEN)
            tam_buffer.set_spot(i, 2, str(i + 1), RED, GREEN)

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, RED, GREEN)

        self.assertEqual(ret_tam_buffer, tam_buffer)

    def test_tam_list_buffer_3(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"]]

        foreground_colors = [[RED, GREEN, YELLOW],
                             [BLUE, PURPLE, AQUA]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 2, " ", RED, GREEN)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), COLORS[i + 1], GREEN)
            tam_buffer.set_spot(i, 1, str(i + 4), COLORS[i + 4], GREEN)

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, foreground_colors, GREEN)

        self.assertEqual(ret_tam_buffer, tam_buffer)

    def test_tam_list_buffer_4(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"]]

        background_colors = [[RED, GREEN, YELLOW],
                             [BLUE, PURPLE, AQUA]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 2, " ", RED, GREEN)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), RED, COLORS[i + 1])
            tam_buffer.set_spot(i, 1, str(i + 4), RED, COLORS[i + 4])

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, RED, background_colors)

        self.assertEqual(ret_tam_buffer, tam_buffer)

    def test_tam_list_buffer_5(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"]]

        foreground_colors = [[GREEN, BLUE, AQUA],
                             [GRAY, LIGHT_GREEN, LIGHT_BLUE]]

        background_colors = [[RED, GREEN, YELLOW],
                             [BLUE, PURPLE, AQUA]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 2, " ", RED, GREEN)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), COLORS[(i + 1) * 2], COLORS[i + 1])
            tam_buffer.set_spot(i, 1, str(i + 4), COLORS[(i + 4) * 2], COLORS[i + 4])

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, foreground_colors, background_colors)

        self.assertEqual(ret_tam_buffer, tam_buffer)
