# built in libraries
import sys
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


class RAWIOTest(unittest.TestCase):
    def test_same_methods(self):
        for method in dir(tam_io.io_tam.IO):
            if method[0] != "_":
                self.assertTrue(hasattr(tam_io.io_tam.RawIO, method))

        for method in dir(tam_io.io_tam.RawIO):
            if method[0] != "_":
                self.assertTrue(hasattr(tam_io.io_tam.IO, method))

    def test_same_doc_string(self):
        for method in dir(tam_io.io_tam.IO):
            if method[0] != "_":
                self.assertTrue(getattr(tam_io.io_tam.IO, method), getattr(tam_io.io_tam.RawIO, method).__doc__)


class IOTAMTest(unittest.TestCase):
    def test__draw_onto(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "A", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)
        surface3 = tam_io.tam_surface.TAMSurface(5, 6, "A", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)

        tam_io.io_tam.IO._draw_onto(surface, surface2)
        surface3.draw_onto(surface2, 1, 1)

        self.assertEqual(str(surface), str(surface3))

    def test__draw_onto_2(self):
        surface = tam_io.tam_surface.TAMSurface(5, 6, "A", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(3, 4, "B", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)
        surface3 = tam_io.tam_surface.TAMSurface(5, 6, "A", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)

        surface2.set_spot(0, 0, "C", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)
        surface2.set_spot(1, 0, "D", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)
        surface2.set_spot(2, 1, "E", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)
        surface2.set_spot(2, 3, "F", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)
        surface2.set_spot(1, 1, "G", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)

        tam_io.io_tam.IO._draw_onto(surface, surface2)
        surface3.draw_onto(surface2, 1, 1)

        self.assertEqual(str(surface), str(surface3))

    def test__draw_onto_3(self):
        surface = tam_io.tam_surface.TAMSurface(50, 60, "A", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)
        surface2 = tam_io.tam_surface.TAMSurface(30, 40, "B", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)
        surface3 = tam_io.tam_surface.TAMSurface(50, 60, "A", tam_io.tam_colors.RED, tam_io.tam_colors.GREEN)

        surface2.set_spot(0, 0, "C", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)
        surface2.set_spot(1, 0, "D", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)
        surface2.set_spot(2, 1, "E", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)
        surface2.set_spot(2, 3, "F", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)
        surface2.set_spot(1, 1, "G", tam_io.tam_colors.BLUE, tam_io.tam_colors.PURPLE)

        tam_io.io_tam.IO._draw_onto(surface, surface2)

        surface3.draw_onto(surface2, 10, 10)

        self.assertEqual(str(surface), str(surface3))

    @staticmethod
    def test__write_to_output_stream():
        with unittest.mock.patch.object(sys.stdout, "write") as write_stdout:
            with unittest.mock.patch.object(sys.stdout, "flush") as flush_stdout:
                with unittest.mock.patch.object(sys.stderr, "write") as write_stderr:
                    with unittest.mock.patch.object(sys.stderr, "flush") as flush_stderr:
                        tam_io.io_tam.IO._write_to_output_stream("cats", True, False)
                        write_stdout.assert_called_once_with("cats")
                        flush_stdout.assert_called_once_with()
                        write_stderr.assert_not_called()
                        flush_stderr.assert_not_called()

    @staticmethod
    def test__write_to_output_stream_2():
        with unittest.mock.patch.object(sys.stdout, "write") as write_stdout:
            with unittest.mock.patch.object(sys.stdout, "flush") as flush_stdout:
                with unittest.mock.patch.object(sys.stderr, "write") as write_stderr:
                    with unittest.mock.patch.object(sys.stderr, "flush") as flush_stderr:
                        tam_io.io_tam.IO._write_to_output_stream("dogs", False, True)
                        write_stdout.assert_not_called()
                        flush_stdout.assert_not_called()
                        write_stderr.assert_called_once_with("dogs")
                        flush_stderr.assert_not_called()
