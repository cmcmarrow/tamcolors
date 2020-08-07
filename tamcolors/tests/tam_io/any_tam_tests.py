# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


class AnyIOTests(unittest.TestCase):
    def test_get_io(self):
        self.assertTrue(tam_io.any_tam.AnyIO.able_to_execute())

    def test_set_slash_get_mode(self):
        io = tam_io.any_tam.AnyIO()
        io.set_mode(2)
        self.assertEqual(io.get_mode(), 2)

    def test_get_modes(self):
        io = tam_io.any_tam.AnyIO()
        self.assertEqual(io.get_modes(), (2, 16))

    def test_get_key(self):
        self.assertEqual(tam_io.any_tam.AnyIO().get_key(), False)

    def test_get_dimensions(self):
        self.assertEqual(tam_io.any_tam.AnyIO().get_dimensions(), (85, 25))


class GetIOTests(unittest.TestCase):
    @staticmethod
    def test_get_io():
        tam_io.any_tam.get_io()

    def test_get_io_2(self):
        io = tam_io.any_tam.get_io(io_list=(), any_os=True)
        self.assertIsInstance(io, tam_io.any_tam.AnyIO)

    def test_get_io_3(self):
        io = tam_io.any_tam.get_io(io_list=(), any_os=False)
        self.assertEqual(io, None)
