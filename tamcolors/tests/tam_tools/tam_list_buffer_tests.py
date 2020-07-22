# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam
from tamcolors import tam_tools


class TAMListBufferTests(unittest.TestCase):
    def test_tam_list_buffer(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 2, " ", 1, 2)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), 1, 2)
            tam_buffer.set_spot(i, 1, str(i + 4), 1, 2)

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, 1, 2)

        self.assertEqual(ret_tam_buffer, tam_buffer)

    def test_tam_list_buffer_2(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"],
                  ["1", "2", "3"]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 3, " ", 1, 2)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), 1, 2)
            tam_buffer.set_spot(i, 1, str(i + 4), 1, 2)
            tam_buffer.set_spot(i, 2, str(i + 1), 1, 2)

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, 1, 2)

        self.assertEqual(ret_tam_buffer, tam_buffer)

    def test_tam_list_buffer_3(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"]]

        foreground_colors = [[1, 2, 3],
                             [4, 5, 6]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 2, " ", 1, 2)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), i + 1, 2)
            tam_buffer.set_spot(i, 1, str(i + 4), i + 4, 2)

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, foreground_colors, 2)

        self.assertEqual(ret_tam_buffer, tam_buffer)

    def test_tam_list_buffer_4(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"]]

        background_colors = [[1, 2, 3],
                             [4, 5, 6]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 2, " ", 1, 2)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), 1, i + 1)
            tam_buffer.set_spot(i, 1, str(i + 4), 1, i + 4)

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, 1, background_colors)

        self.assertEqual(ret_tam_buffer, tam_buffer)

    def test_tam_list_buffer_5(self):
        buffer = [["1", "2", "3"],
                  ["4", "5", "6"]]

        foreground_colors = [[2, 4, 6],
                             [8, 10, 12]]

        background_colors = [[1, 2, 3],
                             [4, 5, 6]]

        tam_buffer = tam_io.tam_buffer.TAMBuffer(3, 2, " ", 1, 2)
        for i in range(3):
            tam_buffer.set_spot(i, 0, str(i + 1), (i + 1) * 2, i + 1)
            tam_buffer.set_spot(i, 1, str(i + 4), (i + 4) * 2, i + 4)

        ret_tam_buffer = tam_tools.tam_list_buffer.tam_list_buffer(buffer, foreground_colors, background_colors)

        self.assertEqual(ret_tam_buffer, tam_buffer)
