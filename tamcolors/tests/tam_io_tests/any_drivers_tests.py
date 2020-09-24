# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


def get_any_io():
    return tam_io.tam_identifier.TAMIdentifier("any_driver_tests",
                                               tam_io.any_drivers.ANYColorDriver,
                                               tam_io.any_drivers.ANYColorChangerDriver,
                                               tam_io.any_drivers.ANYKeyDriver,
                                               tam_io.any_drivers.ANYUtilitiesDriver).get_io()


class AnyIOTests(unittest.TestCase):
    def test_get_io(self):
        io = get_any_io()
        self.assertTrue(io.able_to_execute())

    def test_set_slash_get_mode(self):
        io = get_any_io()
        io.set_mode(tam_io.io_tam.MODE_2)
        self.assertEqual(io.get_mode(), tam_io.io_tam.MODE_2)

    def test_get_modes(self):
        io = get_any_io()
        self.assertEqual(io.get_modes(), (tam_io.io_tam.MODE_2,))

    def test_get_key(self):
        io = get_any_io()
        self.assertEqual(io.get_key(), False)

    def test_get_dimensions(self):
        io = get_any_io()
        self.assertEqual(io.get_dimensions(), (85, 25))

    @staticmethod
    def test_reset_colors_to_console_defaults():
        io = get_any_io()
        io.reset_colors_to_console_defaults()

    @staticmethod
    def test_set_tam_color_defaults():
        io = get_any_io()
        io.set_tam_color_defaults()
