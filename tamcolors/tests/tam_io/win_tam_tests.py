# built in libraries
import platform
import sys
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam
from tamcolors import tam_io


@unittest.skipIf(platform.system() != "Windows", "Most be on Windows.")
class WinIOTests(unittest.TestCase):
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
