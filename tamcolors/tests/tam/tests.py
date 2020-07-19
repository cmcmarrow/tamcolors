# built in libraries
import threading
import platform
import os
import sys
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam
from tamcolors import tam_io


"""
tests that checks tam library
"""


class TAMBufferTest(unittest.TestCase):
    def test_buffer_init(self):
        buffer = tam.tam_buffer.TAMBuffer(3, 4, "&", 1, 2)
        self.assertEqual(str(buffer), ("&&&\n"*4)[:-1])

    def test_buffer_str(self):
        buffer = tam.tam_buffer.TAMBuffer(3, 400, "&", 1, 2)
        self.assertEqual(str(buffer), ("&&&\n" * 400)[:-1])

    def test_buffer_len(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 4, "&", 1, 2)
        self.assertEqual(len(buffer), 20)

    def test_buffer_len_2(self):
        buffer = tam.tam_buffer.TAMBuffer(50, 6, "&", 1, 2)
        self.assertEqual(len(buffer), 300)

    def test_buffer_len_3(self):
        buffer = tam.tam_buffer.TAMBuffer(55, 65, "&", 1, 2)
        self.assertEqual(len(buffer), 3575)
        buffer.set_dimensions_and_clear(5, 7)
        self.assertEqual(len(buffer), 35)

    def test_buffer_len_4(self):
        buffer = tam.tam_buffer.TAMBuffer(0, 50, "&", 1, 2)
        self.assertEqual(len(buffer), 0)

    def test_buffer_eq(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        self.assertTrue(buffer == buffer2)

    def test_buffer_eq_2(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(26, 50, "&", 1, 2)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_3(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(25, 50, "c", 1, 2)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_4(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2.set_spot(12, 34, "b", 6, 7)
        self.assertFalse(buffer == buffer2)

    def test_buffer_eq_5(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        self.assertFalse(buffer == 34)

    def test_buffer_ne(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        self.assertFalse(buffer != buffer2)

    def test_buffer_ne_2(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(26, 50, "&", 1, 2)
        self.assertTrue(buffer != buffer2)

    def test_buffer_ne_3(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(25, 50, "c", 1, 2)
        self.assertTrue(buffer != buffer2)

    def test_buffer_ne_4(self):
        buffer = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(25, 50, "&", 1, 2)
        buffer2.set_spot(12, 34, "b", 6, 7)
        self.assertTrue(buffer != buffer2)

    def test_clear(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        for y in range(20):
            for x in range(5):
                buffer.set_spot(x, y, "@", 9, 10)

        buffer.clear()

        for y in range(20):
            for x in range(5):
                self.assertEqual(buffer.get_spot(x, y), (".", 1, 2))
        self.assertEqual(str(buffer), (".....\n" * 20)[:-1])

    def test_get_dimensions(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        self.assertEqual(buffer.get_dimensions(), (5, 20))

    def test_get_dimensions_2(self):
        buffer = tam.tam_buffer.TAMBuffer(3005, 2200, ".", 1, 2)
        self.assertEqual(buffer.get_dimensions(), (3005, 2200))

    def test_get_dimensions_3(self):
        buffer = tam.tam_buffer.TAMBuffer(0, 1, ".", 1, 2)
        self.assertEqual(buffer.get_dimensions(), (0, 1))

    def test_set_dimensions_and_clear(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        buffer.set_dimensions_and_clear(2, 3)
        self.assertEqual(str(buffer), ("..\n" * 3)[:-1])

    def test_set_dimensions_and_clear_2(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        buffer.set_dimensions_and_clear(6, 300)
        self.assertEqual(str(buffer), ("......\n" * 300)[:-1])

    def test_get_defaults(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        buffer.get_defaults()
        self.assertEqual(buffer.get_defaults(), (".", 1, 2))

    def test_set_defaults_and_clear(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 20, ".", 1, 2)
        buffer.set_defaults_and_clear("L", 5, 6)
        for y in range(20):
            for x in range(5):
                self.assertEqual(buffer.get_spot(x, y), ("L", 5, 6))

    def test_set_defaults_and_clear_2(self):
        buffer = tam.tam_buffer.TAMBuffer(50, 22, ".", 1, 2)
        buffer.set_defaults_and_clear("A", 7, 2)
        for y in range(22):
            for x in range(50):
                self.assertEqual(buffer.get_spot(x, y), ("A", 7, 2))

    def test_get_raw_buffers(self):
        buffer = tam.tam_buffer.TAMBuffer(50, 22, ".", 1, 2)
        length = 50 * 22
        self.assertEqual((["."] * length, [1] * length, [2] * length), buffer.get_raw_buffers())

    def test_get_raw_buffers_2(self):
        buffer = tam.tam_buffer.TAMBuffer(501, 222, ".", 1, 2)
        length = 501 * 222
        self.assertEqual((["."] * length, [1] * length, [2] * length), buffer.get_raw_buffers())

    def test_copy(self):
        buffer = tam.tam_buffer.TAMBuffer(50, 22, ".", 1, 2)
        buffer2 = buffer.copy()

        for y in range(22):
            for x in range(50):
                buffer2.set_spot(x, y, "H", 5, 2)

        self.assertNotEqual(str(buffer), str(buffer2))

    def test_copy_2(self):
        buffer = tam.tam_buffer.TAMBuffer(55, 23, ".", 1, 2)
        buffer2 = buffer.copy()

        for y in range(23):
            for x in range(55):
                buffer2.set_spot(x, y, "H", 5, 2)

        self.assertNotEqual(str(buffer), str(buffer2))

    def test_get_raw_spot(self):
        buffer = tam.tam_buffer.TAMBuffer(55, 23, ".", 1, 2)
        raw_spots = []

        for y in range(23):
            for x in range(55):
                raw_spot = buffer.get_raw_spot(x, y)
                self.assertTrue(raw_spot not in raw_spots)
                raw_spots.append(raw_spot)

        self.assertTrue(all([i in range(0, 55 * 23) for i in raw_spots]))

    def test_set_spot(self):
        buffer = tam.tam_buffer.TAMBuffer(3, 4, "&", 1, 2)
        for y in range(4):
            buffer.set_spot(0, y, 'T', 1, 2)
        self.assertEqual(str(buffer), ("T&&\n"*4)[:-1])

    def test_set_spot_2(self):
        buffer = tam.tam_buffer.TAMBuffer(3, 4, "&", 1, 2)
        for y in range(4):
            buffer.set_spot(y % 3, y, "T", 1, 2)
        self.assertEqual(str(buffer), "T&&\n&T&\n&&T\nT&&")

    def test_set_spot_3(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        for y in range(5):
            for x in range(5):
                buffer.set_spot(x, y, str(x), 1, 2)
        self.assertEqual(str(buffer), ("01234\n"*5)[:-1])

    def test_set_spot_4(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        buffer.set_spot(0, 1, "C", -1, -1)
        self.assertEqual(buffer.get_spot(0, 1), ("C", 1, 2))

    def test_set_spot_5(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 5, "&", 1, 2)
        buffer.set_spot(3, 2, "A", 4, -1)
        buffer.set_spot(3, 2, "C", -1, -1)
        self.assertEqual(buffer.get_spot(3, 2), ("C", 4, 2))

    def test_get_spot(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "&", 1, 2)

        buffer.set_spot(0, 0, "A", 2, 3)
        buffer.set_spot(1, 0, "B", 3, 4)
        buffer.set_spot(4, 0, "C", 4, 5)
        buffer.set_spot(3, 2, "D", 5, 6)
        buffer.set_spot(4, 5, "E", 6, 7)

        self.assertEqual(buffer.get_spot(0, 0), ("A", 2, 3))
        self.assertEqual(buffer.get_spot(1, 0), ("B", 3, 4))
        self.assertEqual(buffer.get_spot(4, 0), ("C", 4, 5))
        self.assertEqual(buffer.get_spot(3, 2), ("D", 5, 6))
        self.assertEqual(buffer.get_spot(4, 5), ("E", 6, 7))

        self.assertEqual(buffer.get_spot(0, 6), None)
        self.assertEqual(buffer.get_spot(-1, 0), None)

    def test_get_from_raw_spot(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "&", 1, 2)

        buffer.set_spot(0, 0, "A", 2, 3)
        buffer.set_spot(1, 0, "B", 3, 4)
        buffer.set_spot(4, 0, "C", 4, 5)
        buffer.set_spot(3, 2, "D", 5, 6)
        buffer.set_spot(4, 5, "E", 6, 7)

        self.assertEqual(buffer.get_from_raw_spot(0), ("A", 2, 3))
        self.assertEqual(buffer.get_from_raw_spot(1), ("B", 3, 4))
        self.assertEqual(buffer.get_from_raw_spot(4), ("C", 4, 5))
        self.assertEqual(buffer.get_from_raw_spot(13), ("D", 5, 6))
        self.assertEqual(buffer.get_from_raw_spot(29), ("E", 6, 7))

        self.assertEqual(buffer.get_from_raw_spot(-1), None)
        self.assertEqual(buffer.get_from_raw_spot(30), None)

    def test_draw_onto(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2)
        self.assertEqual(str(buffer), "BBBAA\n" * 4 + "AAAAA\nAAAAA")

    def test_draw_onto_2(self):
        buffer = tam.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, -1, -1)
        self.assertEqual(str(buffer), ("BBAAAA\n" * 3 + "AAAAAA\n" * 4)[:-1])

    def test_draw_onto_3(self):
        buffer = tam.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 0, 0, 1, 1)
        self.assertEqual(str(buffer), ("BBAAAA\n" * 3 + "AAAAAA\n" * 4)[:-1])

    def test_draw_onto_4(self):
        buffer = tam.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, -1, -1, 1, 1)
        self.assertEqual(str(buffer), ("BAAAAA\n" * 2 + "AAAAAA\n" * 5)[:-1])

    def test_draw_onto_5(self):
        buffer = tam.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 0, 0, 2, 2)
        self.assertEqual(str(buffer), ("BAAAAA\n" * 2 + "AAAAAA\n" * 5)[:-1])

    def test_draw_onto_6(self):
        buffer = tam.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 8, 8)
        self.assertEqual(str(buffer), ("AAAAAA\n" * 7)[:-1])

    def test_draw_onto_7(self):
        buffer = tam.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 5, 6)
        self.assertEqual(str(buffer), "AAAAAA\n" * 6 + "AAAAAB")

    def test_draw_onto_8(self):
        buffer = tam.tam_buffer.TAMBuffer(6, 7, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        buffer.draw_onto(buffer2, 1, 1, 0, 0, 2, 2)
        self.assertEqual(str(buffer), ("AAAAAA\n" + "ABBAAA\n" * 2 + "AAAAAA\n" * 4)[:-1])

    def test_get_cross_rect(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        self.assertEqual(buffer.get_cross_rect(buffer2, -2, -1, 0, 0), (0, 0, 2, 1, 1, 3))

    def test_get_cross_rect_2(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)

        self.assertEqual(buffer.get_cross_rect(buffer2, -6, -6, -12, -12, 100, 100), (6, 6, 0, 0, 0, 0))


class IOTAMTest(unittest.TestCase):
    def test__draw_onto(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)
        buffer3 = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)
        buffer3.draw_onto(buffer2, 1, 1)

        self.assertEqual(str(buffer), str(buffer3))

    def test__draw_onto_2(self):
        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(3, 4, "B", 1, 2)
        buffer3 = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)

        buffer2.set_spot(0, 0, "C", 4, 5)
        buffer2.set_spot(1, 0, "D", 4, 5)
        buffer2.set_spot(2, 1, "E", 4, 5)
        buffer2.set_spot(2, 3, "F", 4, 5)
        buffer2.set_spot(1, 1, "G", 4, 5)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)
        buffer3.draw_onto(buffer2, 1, 1)

        self.assertEqual(str(buffer), str(buffer3))

    def test__draw_onto_3(self):
        buffer = tam.tam_buffer.TAMBuffer(50, 60, "A", 1, 2)
        buffer2 = tam.tam_buffer.TAMBuffer(30, 40, "B", 1, 2)
        buffer3 = tam.tam_buffer.TAMBuffer(50, 60, "A", 1, 2)

        buffer2.set_spot(0, 0, "C", 4, 5)
        buffer2.set_spot(1, 0, "D", 4, 5)
        buffer2.set_spot(2, 1, "E", 4, 5)
        buffer2.set_spot(2, 3, "F", 4, 5)
        buffer2.set_spot(1, 1, "G", 4, 5)

        tam_io.io_tam.IO._draw_onto(buffer, buffer2)

        buffer3.draw_onto(buffer2, 10, 10)

        self.assertEqual(str(buffer), str(buffer3))


class AnyIOTest(unittest.TestCase):
    def test_get_io(self):
        self.assertIsInstance(tam_io.any_tam.AnyIO.get_io(), tam_io.any_tam.AnyIO)

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


class GetIOTest(unittest.TestCase):
    @staticmethod
    def test_get_io():
        tam_io.any_tam.get_io()

    def test_get_io_2(self):
        io = tam_io.any_tam.get_io(io_list=(), any_os=True)
        self.assertIsInstance(io, tam_io.any_tam.AnyIO)

    def test_get_io_3(self):
        io = tam_io.any_tam.get_io(io_list=(), any_os=False)
        self.assertEqual(io, None)


@unittest.skipIf(platform.system() not in ("Darwin", "Linux"), "Most be on Unix.")
class UniIOTest(unittest.TestCase):
    def test_get_io(self):
        with unittest.mock.patch.object(os,
                                        "system",
                                        return_value=256) as system:
            if hasattr(tam_io.uni_tam.UniIO, "uni_io"):
                del tam_io.uni_tam.UniIO.uni_io

            io = tam_io.uni_tam.UniIO.get_io()

            system.assert_called_once_with("test -t 0 -a -t 1 -a -t 2")

            self.assertEqual(io, None)

    def test_set_slash_get_mode(self):
        io = tam_io.uni_tam.UniIO()
        io.set_mode(2)
        self.assertEqual(io.get_mode(), 2)

    def test_get_modes(self):
        io = tam_io.uni_tam.UniIO()
        modes = io.get_modes()
        self.assertIsInstance(modes, tuple)
        modes = list(modes)
        modes.sort()
        self.assertEqual(modes, [2, 16])

    @staticmethod
    def test__draw_2():
        io = tam_io.uni_tam.UniIO()
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_enable_get_key", return_value=None) as _enable_get_key:
            with unittest.mock.patch.object(io, "_clear", return_value=None) as _clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    with unittest.mock.patch.object(sys.stdout, "write",
                                                    return_value=None) as write:
                        with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                            with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_dimension",
                                                            return_value=(15, 10)) as _get_dimension:
                                io.set_mode(2)
                                tam_buffer = tam.tam_buffer.TAMBuffer(5, 7, "A", 3, 4)
                                tam_buffer.set_spot(1, 1, "B", 7, 8)
                                tam_buffer.set_spot(1, 2, "C", 7, 7)
                                tam_buffer.set_spot(2, 2, "D", 4, 5)
                                tam_buffer.set_spot(2, 3, "E", 4, 5)
                                tam_buffer.set_spot(3, 3, "F", 5, 7)
                                io.draw(tam_buffer)

                                _enable_get_key.assert_called_once_with()
                                _clear.assert_called_once_with()
                                _show_console_cursor.assert_called_once_with(False)
                                _get_dimension.assert_called_once_with()
                                flush.assert_called_once_with()
                                write.assert_called_once()

    @staticmethod
    def test__draw_16():
        io = tam_io.uni_tam.UniIO()
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_enable_get_key", return_value=None) as _enable_get_key:
            with unittest.mock.patch.object(io, "_clear", return_value=None) as _clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    with unittest.mock.patch.object(sys.stdout, "write",
                                                    return_value=None) as write:
                        with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                            with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_dimension",
                                                            return_value=(15, 10)) as _get_dimension:
                                io.set_mode(16)
                                tam_buffer = tam.tam_buffer.TAMBuffer(5, 7, "A", 3, 4)
                                tam_buffer.set_spot(1, 1, "B", 7, 8)
                                tam_buffer.set_spot(1, 2, "C", 7, 7)
                                tam_buffer.set_spot(2, 2, "D", 4, 5)
                                tam_buffer.set_spot(2, 3, "E", 4, 5)
                                tam_buffer.set_spot(3, 3, "F", 5, 7)
                                io.draw(tam_buffer)

                                _enable_get_key.assert_called_once_with()
                                _clear.assert_called_once_with()
                                _show_console_cursor.assert_called_once_with(False)
                                _get_dimension.assert_called_once_with()
                                flush.assert_called_once_with()
                                write.assert_called_once()

    @staticmethod
    def test_start():
        io = tam_io.uni_tam.UniIO()
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_enable_get_key", return_value=None) as _enable_get_key:
            with unittest.mock.patch.object(io, "_clear", return_value=None) as _clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    io.start()

                    _enable_get_key.assert_called_once_with()
                    _clear.assert_called_once_with()
                    _show_console_cursor.assert_called_once_with(False)

    @staticmethod
    def test_done():
        io = tam_io.uni_tam.UniIO()
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_disable_get_key", return_value=None) as _disable_get_key:
            with unittest.mock.patch.object(io, "_clear", return_value=None) as _clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    io.done()

                    _disable_get_key.assert_called_once_with()
                    _clear.assert_called_once_with()
                    _show_console_cursor.assert_called_once_with(True)

    def test_get_key(self):
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_key", side_effect=[65, -1]) as _get_key:
            io = tam_io.uni_tam.UniIO()
            self.assertEqual(io.get_key(), ("A", "NORMAL"))

            self.assertEqual(_get_key.call_count, 2)

    def test_get_key_2(self):
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_key", side_effect=[27, 91, 65, -1]) as _get_key:
            io = tam_io.uni_tam.UniIO()
            self.assertEqual(io.get_key(), ("UP", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 4)

    def test_get_key_3(self):
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_key", side_effect=[27, 91, 50, 52, 126, -1]) as _get_key:
            io = tam_io.uni_tam.UniIO()
            self.assertEqual(io.get_key(), ("F12", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 6)

    def test_get_key_4(self):
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_key", side_effect=[155, 65, -1]) as _get_key:
            io = tam_io.uni_tam.UniIO()
            self.assertEqual(io.get_key(), False)

            self.assertEqual(_get_key.call_count, 3)

    def test_get_key_5(self):
        with unittest.mock.patch.object(tam_io.uni_tam.io,
                                        "_get_key", side_effect=[66, -1, 27, 91, 51, 126, -1]) as _get_key:
            io = tam_io.uni_tam.UniIO()
            self.assertEqual(io.get_key(), ("B", "NORMAL"))
            self.assertEqual(io.get_key(), ("DELETE", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 7)

    def test_get_dimensions(self):
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_dimension", return_value=(20, 25)) as _get_dimension:
            io = tam_io.uni_tam.UniIO()

            self.assertEqual(io.get_dimensions(), (20, 25))

            _get_dimension.assert_called_once_with()

    def test_get_key_dict(self):
        keys = tam_io.uni_tam.UniIO().get_key_dict()
        for key in keys:
            self.assertIsInstance(key, str)
            self.assertIsInstance(keys.get(key), tuple)

    @staticmethod
    def test__show_console_cursor():
        with unittest.mock.patch.object(os, "system", return_value=0) as system:
            io = tam_io.uni_tam.UniIO()
            io._show_console_cursor(True)
            if platform.system() != "Darwin":
                system.assert_called_once_with("setterm -cursor on")
            else:
                system.assert_not_called()

    def test__get_lin_tam_color(self):
        io = tam_io.uni_tam.UniIO()
        self.assertEqual(io._get_lin_tam_color(2, 5), (34, 90))

    @staticmethod
    def test__clear():
        with unittest.mock.patch.object(os, "system", return_value=0) as system:
            io = tam_io.uni_tam.UniIO()
            io._clear()
            system.assert_called_once_with("tput reset")


@unittest.skipIf(platform.system() != "Windows", "Most be on Windows.")
class WinIOTest(unittest.TestCase):
    def test_get_io(self):
        with unittest.mock.patch.object(tam_io.win_tam.io,
                                        "_init_default_color",
                                        return_value=0) as _init_default_color:

            if hasattr(tam_io.win_tam.WinIO, "win_io"):
                del tam_io.win_tam.WinIO.win_io

            io = tam_io.win_tam.WinIO.get_io()

            _init_default_color.assert_called_once_with()

            self.assertEqual(io, None)

    def test_set_slash_get_mode(self):
        io = tam_io.win_tam.WinIO()
        io.set_mode(2)
        self.assertEqual(io.get_mode(), 2)

    def test_get_modes(self):
        io = tam_io.win_tam.WinIO()
        modes = io.get_modes()
        self.assertIsInstance(modes, tuple)
        modes = list(modes)
        modes.sort()
        self.assertEqual(modes, [2, 16])

    @staticmethod
    def test__draw_2():
        io = tam_io.win_tam.WinIO()
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_dimension", return_value=(15, 10)) as _get_dimension:
            with unittest.mock.patch.object(tam_io.win_tam.io, "_clear", return_value=None) as _clear:
                with unittest.mock.patch.object(tam_io.win_tam.io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    with unittest.mock.patch.object(io, "_print", return_value=None) as _print:
                        io.set_mode(2)
                        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
                        buffer2 = tam.tam_buffer.TAMBuffer(15, 10, " ", 1, 2)

                        buffer.set_spot(1, 1, "B", 5, 7)
                        buffer.set_spot(4, 4, "C", 5, 7)
                        buffer.set_spot(4, 5, "D", 5, 7)

                        buffer2.draw_onto(buffer, 5, 2)
                        io.draw(buffer)

                        _get_dimension.assert_called()
                        _clear.assert_called_once_with()
                        _show_console_cursor.assert_called_once_with(False)
                        _print.assert_called_once_with(0, 0, "".join(c for c in str(buffer2) if c != "\n"), 1, 2)

    def test__draw_16(self):
        io = tam_io.win_tam.WinIO()
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_dimension", return_value=(15, 10)) as _get_dimension:
            with unittest.mock.patch.object(tam_io.win_tam.io, "_clear", return_value=None) as _clear:
                with unittest.mock.patch.object(tam_io.win_tam.io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    with unittest.mock.patch.object(io, "_print", return_value=None) as _print:
                        io.set_mode(16)
                        buffer = tam.tam_buffer.TAMBuffer(5, 6, "A", 1, 2)
                        buffer2 = tam.tam_buffer.TAMBuffer(15, 10, " ", 1, 2)

                        buffer.set_spot(1, 1, "B", 5, 7)
                        buffer.set_spot(3, 5, "C", 5, 7)
                        buffer.set_spot(4, 5, "D", 5, 7)
                        buffer.set_spot(1, 2, " ", 5, 2)

                        buffer2.draw_onto(buffer, 5, 2)
                        io.draw(buffer)

                        _get_dimension.assert_called()
                        _clear.assert_called_once_with()
                        _show_console_cursor.assert_called_once_with(False)

                        self.assertEqual(_print.call_count, 16)

                        self.assertEqual(_print.mock_calls[0], unittest.mock.call(0, 0, "." * 35, 2, 2))
                        self.assertEqual(_print.mock_calls[1], unittest.mock.call(5, 2, "A" * 5, 1, 2))
                        self.assertEqual(_print.mock_calls[2], unittest.mock.call(10, 2, "." * 10, 2, 2))
                        self.assertEqual(_print.mock_calls[3], unittest.mock.call(5, 3, "A", 1, 2))
                        self.assertEqual(_print.mock_calls[4], unittest.mock.call(6, 3, "B", 5, 7))
                        self.assertEqual(_print.mock_calls[10], unittest.mock.call(10, 5, "." * 10, 2, 2))
                        self.assertEqual(_print.mock_calls[15], unittest.mock.call(10, 7, "." * 35, 2, 2))

    @staticmethod
    def test_start():
        with unittest.mock.patch.object(tam_io.win_tam.io, "_clear", return_value=None) as _clear:
            with unittest.mock.patch.object(tam_io.win_tam.io,
                                            "_show_console_cursor",
                                            return_value=None) as _show_console_cursor:
                tam_io.win_tam.WinIO().start()

                _clear.assert_called_once_with()
                _show_console_cursor.assert_called_once_with(False)

    @staticmethod
    def test_done():
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_default_color", return_value=2) as _get_default_color:
            with unittest.mock.patch.object(tam_io.win_tam.io, "_set_cursor_info", return_value=None) as _set_cursor_info:
                with unittest.mock.patch.object(tam_io.win_tam.io, "_clear", return_value=None) as _clear:
                    with unittest.mock.patch.object(tam_io.win_tam.io,
                                                    "_show_console_cursor",
                                                    return_value=None) as _show_console_cursor:
                        tam_io.win_tam.WinIO().done()

                        _get_default_color.assert_called_once_with()
                        _set_cursor_info.assert_called_once_with(0, 0, 2)
                        _clear.assert_called_once_with()
                        _show_console_cursor.assert_called_once_with(True)

    def test_get_key(self):
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_key", side_effect=[65, -1]) as _get_key:
            io = tam_io.win_tam.WinIO()
            self.assertEqual(io.get_key(), ("A", "NORMAL"))

            self.assertEqual(_get_key.call_count, 2)

    def test_get_key_2(self):
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_key", side_effect=[224, 72, -1]) as _get_key:
            io = tam_io.win_tam.WinIO()
            self.assertEqual(io.get_key(), ("UP", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 3)

    def test_get_key_3(self):
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_key", side_effect=[224, 134, -1]) as _get_key:
            io = tam_io.win_tam.WinIO()
            self.assertEqual(io.get_key(), ("F12", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 3)

    def test_get_key_4(self):
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_key", side_effect=[155, 65, -1]) as _get_key:
            io = tam_io.win_tam.WinIO()
            self.assertEqual(io.get_key(), False)

            self.assertEqual(_get_key.call_count, 3)

    def test_get_key_5(self):
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_key", side_effect=[66, -1, 224, 83, -1]) as _get_key:
            io = tam_io.win_tam.WinIO()
            self.assertEqual(io.get_key(), ("B", "NORMAL"))
            self.assertEqual(io.get_key(), ("DELETE", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 5)

    def test_get_dimensions(self):
        with unittest.mock.patch.object(tam_io.win_tam.io, "_get_dimension", return_value=(20, 25)) as _get_dimension:
            io = tam_io.win_tam.WinIO()

            self.assertEqual(io.get_dimensions(), (20, 25))

            _get_dimension.assert_called_once_with()

    def test_get_key_dict(self):
        keys = tam_io.win_tam.WinIO().get_key_dict()
        for key in keys:
            self.assertIsInstance(key, str)
            self.assertIsInstance(keys.get(key), tuple)

    @staticmethod
    def test__print():
        with unittest.mock.patch.object(tam_io.win_tam.io, "_set_cursor_info", return_value=None) as _set_cursor_info:
            with unittest.mock.patch.object(sys.stdout, "write", return_value=None) as write:
                with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                    tam_io.win_tam.WinIO()._print(10, 12, "test", 2, 5)

                    _set_cursor_info.assert_called_once_with(10, 12, 82)
                    write.assert_called_once_with("test")
                    flush.assert_called_once_with()

    @staticmethod
    def test__print_2():
        with unittest.mock.patch.object(tam_io.win_tam.io, "_set_cursor_info", return_value=None) as _set_cursor_info:
            with unittest.mock.patch.object(sys.stdout, "write", return_value=None) as write:
                with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                    tam_io.win_tam.WinIO()._print(102, 124, "test123", 123, 5)

                    _set_cursor_info.assert_called_once_with(102, 124, 91)
                    write.assert_called_once_with("test123")
                    flush.assert_called_once_with()

    @staticmethod
    def test__print_3():
        with unittest.mock.patch.object(tam_io.win_tam.io, "_set_cursor_info", return_value=None) as _set_cursor_info:
            with unittest.mock.patch.object(sys.stdout, "write", return_value=None) as write:
                with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                    tam_io.win_tam.WinIO()._print(-102, -124, "", -123, 5)

                    _set_cursor_info.assert_called_once_with(-102, -124, 85)
                    write.assert_called_once_with("")
                    flush.assert_called_once_with()


class TAMColorTest(unittest.TestCase):
    def test_colors(self):
        self.assertEqual(tam.tam_colors.BLACK, 0)
        self.assertEqual(tam.tam_colors.BLUE, 1)
        self.assertEqual(tam.tam_colors.GREEN, 2)
        self.assertEqual(tam.tam_colors.AQUA, 3)
        self.assertEqual(tam.tam_colors.RED, 4)
        self.assertEqual(tam.tam_colors.PURPLE, 5)
        self.assertEqual(tam.tam_colors.YELLOW, 6)
        self.assertEqual(tam.tam_colors.WHITE, 7)
        self.assertEqual(tam.tam_colors.GRAY, 8)
        self.assertEqual(tam.tam_colors.LIGHT_BLUE, 9)
        self.assertEqual(tam.tam_colors.LIGHT_GREEN, 10)
        self.assertEqual(tam.tam_colors.LIGHT_AQUA, 11)
        self.assertEqual(tam.tam_colors.LIGHT_RED, 12)
        self.assertEqual(tam.tam_colors.LIGHT_PURPLE, 13)
        self.assertEqual(tam.tam_colors.LIGHT_YELLOW, 14)
        self.assertEqual(tam.tam_colors.LIGHT_WHITE, 15)


class TAMKeyTest(unittest.TestCase):
    def test_keys(self):
        self.assertIsInstance(tam.tam_keys.KEYS, set)
        for key in tam.tam_keys.KEYS:
            self.assertIsInstance(key, tuple)
            self.assertEqual(len(key), 2)
            self.assertIsInstance(key[0], str)
            self.assertIsInstance(key[1], str)


class TAMLoopTest(unittest.TestCase):
    def test_loop_init(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        tam.tam_loop.TAMLoop(frame, only_any_os=True)

    def test_run(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(threading.Thread, "start", return_value=None) as start:
            with unittest.mock.patch.object(threading.Thread, "join", return_value=None) as join:
                with unittest.mock.patch.object(dummy, "done", return_value=None) as done:
                    loop.run()

                    self.assertEqual(start.call_count, 2)
                    self.assertEqual(start.mock_calls[0], unittest.mock.call())
                    self.assertEqual(start.mock_calls[1], unittest.mock.call())

                    self.assertEqual(join.call_count, 2)
                    self.assertEqual(join.mock_calls[0], unittest.mock.call())
                    self.assertEqual(join.mock_calls[1], unittest.mock.call())

                    done.assert_called_once_with(loop, {})

    def test_stack(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        dummy2 = self._get_dummy_frame()
        frame2 = tam.tam_loop.TAMFrame(dummy2, 5, "B", 3, 4, 25, 35, 26, 36)

        with unittest.mock.patch.object(dummy2, "done", return_value=True) as done:
            loop.add_frame_stack(frame2)
            loop.pop_frame_stack()

            done.assert_called_once_with(loop, {})

    @staticmethod
    def _get_dummy_frame():
        class Dummy:
            def __init__(self):
                pass

            def update(self, tam_loop, keys, loop_data):
                tam_loop.done()

            def draw(self, tam_buffer, loop_data):
                pass

            def done(self, tam_loop, loop_data):
                pass

        return Dummy()


class TAMFrameTest(unittest.TestCase):
    def test_frame_init(self):
        tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)

    def test_get_fps(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        self.assertEqual(frame.get_fps(), 5)

    def test_get_fps_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "A", 3, 4, 25, 35, 26, 36)
        self.assertEqual(frame.get_fps(), 10)

    def test_get_defaults(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "A", 3, 4, 25, 35, 26, 36)
        self.assertEqual(frame.get_defaults(), ("A", 3, 4))

    def test_get_defaults_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 25, 35, 26, 36)
        self.assertEqual(frame.get_defaults(), ("C", 5, 8))

    def test_get_width_min_and_max(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 25, 35, 26, 36)
        self.assertEqual(frame.get_width_min_and_max(), (25, 35))

    def test_get_width_min_and_max_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 26, 36)
        self.assertEqual(frame.get_width_min_and_max(), (15, 45))

    def test_get_height_min_and_max(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 25, 35, 26, 36)
        self.assertEqual(frame.get_height_min_and_max(), (26, 36))

    def test_get_height_min_and_max_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 47, 58)
        self.assertEqual(frame.get_height_min_and_max(), (47, 58))

    def test_make_buffer_ready(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 47, 58)
        buffer = tam.tam_buffer.TAMBuffer(30, 32, "C", 1, 2)
        frame.make_buffer_ready(buffer, 46, 59)
        self.assertEqual(buffer.get_dimensions(), (45, 58))

    def test_make_buffer_ready_2(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 47, 58)
        buffer = tam.tam_buffer.TAMBuffer(30, 32, "C", 1, 2)
        frame.make_buffer_ready(buffer, 1, 2)
        self.assertEqual(buffer.get_dimensions(), (15, 47))

    def test_make_buffer_ready_3(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 10, "C", 5, 8, 15, 45, 47, 58)
        buffer = tam.tam_buffer.TAMBuffer(30, 32, "C", 1, 2)
        frame.make_buffer_ready(buffer, 33, 48)
        self.assertEqual(buffer.get_dimensions(), (33, 48))

    def test_update(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 10, "C", 5, 8, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(dummy, "update", return_value=None) as update:
            frame.update(loop, (), {})
            update.assert_called_once_with(loop, (), {})

    def test_draw(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 10, "C", 5, 8, 15, 45, 47, 58)
        buffer = tam.tam_buffer.TAMBuffer(30, 32, "C", 1, 2)
        with unittest.mock.patch.object(dummy, "draw", return_value=None) as draw:
            frame.draw(buffer, {})
            draw.assert_called_once_with(buffer, {})

    def test_done(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 10, "C", 5, 8, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(dummy, "done", return_value=None) as done:
            frame.done(loop, {})
            done.assert_called_once_with(loop, {})

    def test_done_2(self):
        dummy = self._get_dummy_frame()
        frame = tam.tam_loop.TAMFrame(dummy, 10, "C", 5, 8, 15, 45, 47, 58)
        loop = tam.tam_loop.TAMLoop(frame, only_any_os=True)
        with unittest.mock.patch.object(dummy, "done", return_value=None) as done:
            frame.done(loop, {})
            frame.done(loop, {})
            done.assert_called_once_with(loop, {})

    @staticmethod
    def _get_dummy_frame():
        class Dummy:
            def __init__(self):
                pass

            def update(self, tam_loop, keys, loop_data):
                pass

            def draw(self, tam_buffer, loop_data):
                pass

            def done(self, tam_loop, loop_data):
                pass

        return Dummy()


class TAMLoopTestTest(unittest.TestCase):
    def test_loop_init(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)

        self.assertIsInstance(loop, tam.tam_loop_test.TAMLoopTest)

    def test_loop_call(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        self.assertEqual(loop.get_running(), None)
        loop()
        self.assertEqual(loop.get_running(), True)
        loop.done()
        loop()
        self.assertEqual(loop.get_running(), False)
        loop()
        self.assertEqual(loop.get_running(), False)

    def test_done(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        self.assertEqual(loop.get_running(), None)
        loop.done()
        self.assertEqual(loop.get_running(), None)
        loop()
        loop.done()
        self.assertEqual(loop.get_running(), False)

    def test_run(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        self.assertEqual(loop.get_running(), None)
        loop.run()
        self.assertEqual(loop.get_running(), True)
        loop.done()
        loop.run()
        self.assertEqual(loop.get_running(), False)
        loop.run()
        self.assertEqual(loop.get_running(), False)

    def test_get_runner(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        self.assertEqual(loop.get_running(), None)
        loop()
        self.assertEqual(loop.get_running(), True)

    def test_add_frame_stack(self):
        frame_1 = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        frame_2 = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        frame_3 = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame_1)

        loop.add_frame_stack(frame_2)
        loop.add_frame_stack(frame_3)

        self.assertIs(loop.pop_frame_stack(), frame_3)
        self.assertIs(loop.pop_frame_stack(), frame_2)
        self.assertIs(loop.pop_frame_stack(), frame_1)
        self.assertIs(loop.pop_frame_stack(), None)

    def test_pop_frame_stack(self):
        frame = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)

        self.assertIs(loop.pop_frame_stack(), frame)
        self.assertIs(loop.pop_frame_stack(), None)

    def test_update(self):
        class Dummy:
            def __init__(self, update_func, draw_func, done_func):
                self.__update_func = update_func
                self.__draw_func = draw_func
                self.__done_func = done_func

            def update(self, tam_loop, keys, loop_data):
                self.__update_func()

            def draw(self, tam_buffer, loop_data):
                self.__draw_func()

            def done(self, tam_loop, loop_data):
                self.__done_func()

        update_func = unittest.mock.Mock()
        draw_func = unittest.mock.Mock()
        done_func = unittest.mock.Mock()
        frame = tam.tam_loop.TAMFrame(Dummy(update_func, draw_func, done_func), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)

        loop()
        buffer_1 = loop.update((), 26, 35)[0]

        update_func.assert_called_once_with()
        draw_func.assert_called_once_with()
        self.assertEqual(done_func.call_count, 0)

        self.assertEqual(buffer_1.get_dimensions(), (26, 35))

        loop.update((), 26, 35)

        self.assertEqual(update_func.call_count, 2)
        self.assertEqual(draw_func.call_count, 2)
        self.assertEqual(done_func.call_count, 0)

        loop.update((), 0, 0)

        self.assertEqual(update_func.call_count, 3)
        self.assertEqual(draw_func.call_count, 3)
        self.assertEqual(done_func.call_count, 0)

        loop.done()
        loop.update((), 3, 4)

        self.assertEqual(update_func.call_count, 3)
        self.assertEqual(draw_func.call_count, 3)
        self.assertEqual(done_func.call_count, 1)

        loop.update((), 3, 4)

        self.assertEqual(update_func.call_count, 3)
        self.assertEqual(draw_func.call_count, 3)
        self.assertEqual(done_func.call_count, 1)

    def test_update_2(self):
        class Dummy:
            def __init__(self, update_func, draw_func, done_func):
                self.__update_func = update_func
                self.__draw_func = draw_func
                self.__done_func = done_func

            def update(self, tam_loop, keys, loop_data):
                self.__update_func()

            def draw(self, tam_buffer, loop_data):
                self.__draw_func()
                raise TypeError()

            def done(self, tam_loop, loop_data):
                self.__done_func()

        update_func = unittest.mock.Mock()
        draw_func = unittest.mock.Mock()
        done_func = unittest.mock.Mock()
        frame = tam.tam_loop.TAMFrame(Dummy(update_func, draw_func, done_func), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)

        loop()
        self.assertRaises(TypeError, loop.update, (), 34, 34)

        self.assertEqual(update_func.call_count, 1)
        self.assertEqual(draw_func.call_count, 1)
        self.assertEqual(done_func.call_count, 1)

        loop.update((), 34, 34)

        self.assertEqual(update_func.call_count, 1)
        self.assertEqual(draw_func.call_count, 1)
        self.assertEqual(done_func.call_count, 1)

    def test_update_3(self):
        class Dummy:
            def __init__(self):
                pass

            def update(self, tam_loop, keys, loop_data):
                for key in keys:
                    if key == ("Q", "NORMAL"):
                        tam_loop.done()

            def draw(self, tam_buffer, loop_data):
                pass

            def done(self, tam_loop, loop_data):
                pass

        frame = tam.tam_loop.TAMFrame(Dummy(), 5, "A", 3, 4, 25, 35, 26, 36)
        loop = tam.tam_loop_test.TAMLoopTest(frame)
        loop()

        loop.update((), 23, 23)
        self.assertTrue(loop.get_running())

        loop.update((("q", "NORMAL"), ("1", "NORMAL")), 23, 23)
        self.assertTrue(loop.get_running())

        loop.update((("q", "NORMAL"),), 23, 23)
        self.assertTrue(loop.get_running())

        loop.update((("Q", "NORMAL"),), 23, 23)
        self.assertFalse(loop.get_running())

    def test_update_4(self):
        frame_1 = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        frame_2 = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)
        frame_3 = tam.tam_loop.TAMFrame(self._get_dummy_frame(), 5, "A", 3, 4, 25, 35, 26, 36)

        loop = tam.tam_loop_test.TAMLoopTest(frame_1)

        loop()
        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_1)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_1)

        loop.add_frame_stack(frame_2)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        loop.add_frame_stack(frame_3)
        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_3)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_3)

        loop.pop_frame_stack()

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_2)

        loop.pop_frame_stack()

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_1)

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, frame_1)

        loop.pop_frame_stack()

        _, frame = loop.update((), 23, 24)
        self.assertIs(frame, None)

    @staticmethod
    def _get_dummy_frame():
        class Dummy:
            def __init__(self):
                pass

            def update(self, tam_loop, keys, loop_data):
                pass

            def draw(self, tam_buffer, loop_data):
                pass

            def done(self, tam_loop, loop_data):
                pass

        return Dummy()


class StandardTest(unittest.TestCase):
    def test_same_keys(self):
        uni_key_dict = tam_io.uni_tam.UniIO.get_key_dict()
        win_key_dict = tam_io.win_tam.WinIO.get_key_dict()

        uni_key_set = set([uni_key_dict[key] for key in uni_key_dict])
        win_key_set = set([win_key_dict[key] for key in win_key_dict])

        keys_sets = (uni_key_set, win_key_set, tam.tam_keys.KEYS)
        for key_set in keys_sets:
            for key in key_set:
                for other_key_set in keys_sets:
                    self.assertTrue(key in other_key_set)
