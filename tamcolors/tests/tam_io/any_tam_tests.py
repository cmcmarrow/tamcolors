# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


class AnyIOTests(unittest.TestCase):
    def test_get_io(self):
        self.assertTrue(tam_io.any_drivers.AnyIO.able_to_execute())

    def test_set_slash_get_mode(self):
        io = tam_io.any_drivers.AnyIO()
        io.set_mode(2)
        self.assertEqual(io.get_mode(), 2)

    def test_get_modes(self):
        io = tam_io.any_drivers.AnyIO()
        self.assertEqual(io.get_modes(), (2, 16))

    def test_get_key(self):
        self.assertEqual(tam_io.any_drivers.AnyIO().get_key(), False)

    def test_get_dimensions(self):
        self.assertEqual(tam_io.any_drivers.AnyIO().get_dimensions(), (85, 25))

    def test_get_color(self):
        io = tam_io.any_drivers.AnyIO()
        for spot in range(16):
            color = io.get_color(spot)
            self.assertIsInstance(color, (list, tuple))
            self.assertEqual(len(color), 3)
            for value in range(3):
                self.assertIsInstance(color[value], int)

    def test_set_color(self):
        io = tam_io.any_drivers.AnyIO()
        io.set_color(5, (55, 66, 77))
        color = io.get_color(5)

        self.assertEqual(color, (55, 66, 77))
        io.set_tam_color_defaults()

    def test_set_color_2(self):
        io = tam_io.any_drivers.AnyIO()

        io.set_color(1, (155, 166, 177))
        color = io.get_color(1)

        self.assertEqual(color, (155, 166, 177))
        io.set_tam_color_defaults()

    def test_reset_colors_to_console_defaults(self):
        io = tam_io.any_drivers.AnyIO()
        io.reset_colors_to_console_defaults()

    def test_set_tam_color_defaults(self):
        io = tam_io.any_drivers.AnyIO()
        io.set_tam_color_defaults()


class GetIOTests(unittest.TestCase):
    @staticmethod
    def test_get_io():
        tam_io.any_drivers.get_io()

    def test_get_io_2(self):
        io = tam_io.any_drivers.get_io(io_list=(), any_os=True)
        self.assertIsInstance(io, tam_io.any_drivers.AnyIO)

    def test_get_io_3(self):
        io = tam_io.any_drivers.get_io(io_list=(), any_os=False)
        self.assertEqual(io, None)
