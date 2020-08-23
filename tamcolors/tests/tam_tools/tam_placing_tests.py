# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors import tam_tools
from tamcolors.tam_io.tam_colors import *


class TAMPlacingTests(unittest.TestCase):
    def test__get_center(self):
        self.assertEqual(tam_tools.tam_placing._get_center(9, 3), 8)

    def test__get_center_2(self):
        self.assertEqual(tam_tools.tam_placing._get_center(90, 33), 74)

    def test__get_other_side(self):
        self.assertEqual(tam_tools.tam_placing._get_other_side(9, 3), 7)

    def test__get_other_side_2(self):
        self.assertEqual(tam_tools.tam_placing._get_other_side(90, 33), 58)

    def test__get_dimensions_wrapper(self):
        @tam_tools.tam_placing._get_dimensions
        def func(x, y, w, h):
            return x, y, w, h
        self.assertEqual(func(1, 2, 3, 4), (1, 2, 3, 4))

    def test__get_dimensions_wrapper_2(self):
        @tam_tools.tam_placing._get_dimensions
        def func(x, y, w, h):
            return x, y, w, h
        self.assertEqual(func(1, 2, None, None, tam_io.tam_buffer.TAMBuffer(3, 4, "c", GRAY, LIGHT_RED)), (1, 2, 3, 4))

    def test__get_dimensions_wrapper_3(self):
        @tam_tools.tam_placing._get_dimensions
        def func(x, y, w, h):
            return x, y, w, h
        self.assertEqual(func(1, 2, 12, 15, tam_io.tam_buffer.TAMBuffer(30, 40, "c", GRAY, LIGHT_RED)), (1, 2, 30, 40))

    def test_top_left(self):
        self.assertEqual(tam_tools.tam_placing.top_left(1, 2, 3, 4), (1, 2))

    def test_top_left_2(self):
        self.assertEqual(tam_tools.tam_placing.top_left(11, 23, 13, 24), (11, 23))

    def test_top_right(self):
        self.assertEqual(tam_tools.tam_placing.top_right(1, 2, 3, 4), (-1, 2))

    def test_top_right_2(self):
        self.assertEqual(tam_tools.tam_placing.top_right(11, 23, 15, 24), (-3, 23))

    def test_bottom_left(self):
        self.assertEqual(tam_tools.tam_placing.bottom_left(1, 2, 3, 4), (1, -1))

    def test_bottom_left_2(self):
        self.assertEqual(tam_tools.tam_placing.bottom_left(11, 23, 15, 24), (11, 0))

    def test_bottom_right(self):
        self.assertEqual(tam_tools.tam_placing.bottom_right(1, 2, 3, 4), (-1, -1))

    def test_bottom_right_2(self):
        self.assertEqual(tam_tools.tam_placing.bottom_right(11, 23, 15, 24), (-3, 0))

    def test_center(self):
        self.assertEqual(tam_tools.tam_placing.center(1, 2, 3, 4), (0, 0))

    def test_center_2(self):
        self.assertEqual(tam_tools.tam_placing.center(11, 23, 15, 24), (4, 11))
