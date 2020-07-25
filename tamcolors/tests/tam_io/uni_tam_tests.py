# built in libraries
import platform
import os
import sys
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


@unittest.skipIf(platform.system() not in ("Darwin", "Linux"), "Most be on Unix.")
class UniIOTests(unittest.TestCase):
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
            with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    with unittest.mock.patch.object(sys.stdout, "write",
                                                    return_value=None) as write:
                        with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                            with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_dimension",
                                                            return_value=(15, 10)) as _get_dimension:
                                io.set_mode(2)
                                tam_buffer = tam_io.tam_buffer.TAMBuffer(5, 7, "A", 3, 4)
                                tam_buffer.set_spot(1, 1, "B", 7, 8)
                                tam_buffer.set_spot(1, 2, "C", 7, 7)
                                tam_buffer.set_spot(2, 2, "D", 4, 5)
                                tam_buffer.set_spot(2, 3, "E", 4, 5)
                                tam_buffer.set_spot(3, 3, "F", 5, 7)
                                io.draw(tam_buffer)

                                _enable_get_key.assert_called_once_with()
                                clear.assert_called_once_with()
                                _show_console_cursor.assert_called_once_with(False)
                                _get_dimension.assert_called_once_with()
                                flush.assert_called_once_with()
                                write.assert_called_once()

    @staticmethod
    def test__draw_16():
        io = tam_io.uni_tam.UniIO()
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_enable_get_key", return_value=None) as _enable_get_key:
            with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    with unittest.mock.patch.object(sys.stdout, "write",
                                                    return_value=None) as write:
                        with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                            with unittest.mock.patch.object(tam_io.uni_tam.io, "_get_dimension",
                                                            return_value=(15, 10)) as _get_dimension:
                                io.set_mode(16)
                                tam_buffer = tam_io.tam_buffer.TAMBuffer(5, 7, "A", 3, 4)
                                tam_buffer.set_spot(1, 1, "B", 7, 8)
                                tam_buffer.set_spot(1, 2, "C", 7, 7)
                                tam_buffer.set_spot(2, 2, "D", 4, 5)
                                tam_buffer.set_spot(2, 3, "E", 4, 5)
                                tam_buffer.set_spot(3, 3, "F", 5, 7)
                                io.draw(tam_buffer)

                                _enable_get_key.assert_called_once_with()
                                clear.assert_called_once_with()
                                _show_console_cursor.assert_called_once_with(False)
                                _get_dimension.assert_called_once_with()
                                flush.assert_called_once_with()
                                write.assert_called_once()

    @staticmethod
    def test_start():
        io = tam_io.uni_tam.UniIO()
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_enable_get_key", return_value=None) as _enable_get_key:
            with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    io.start()

                    _enable_get_key.assert_called_once_with()
                    clear.assert_called_once_with()
                    _show_console_cursor.assert_called_once_with(False)

    @staticmethod
    def test_done():
        io = tam_io.uni_tam.UniIO()
        with unittest.mock.patch.object(tam_io.uni_tam.io, "_disable_get_key", return_value=None) as _disable_get_key:
            with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    io.done()

                    _disable_get_key.assert_called_once_with()
                    clear.assert_called_once_with()
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

    def test__get_lin_tam_color_1(self):
        io = tam_io.uni_tam.UniIO()
        self.assertEqual(io._get_lin_tam_color(2, 5), ("38;5;34", "48;5;90"))

    def test__get_lin_tam_color_2(self):
        io = tam_io.uni_tam.UniIO()
        self.assertEqual(io._get_lin_tam_color(-1, -1), ("0", "0"))

    @staticmethod
    def test_clear():
        with unittest.mock.patch.object(os, "system", return_value=0) as system:
            io = tam_io.uni_tam.UniIO()
            io.clear()
            system.assert_called_once_with("tput reset")
