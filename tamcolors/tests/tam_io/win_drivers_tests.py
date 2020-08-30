# built in libraries
import platform
import sys
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io
from tamcolors.tam_io.tam_colors import *


def get_win_io():
    return tam_io.tam_identifier.TAMIdentifier("win_driver_tests",
                                               tam_io.win_drivers.WINFullColorDriver,
                                               tam_io.win_drivers.WINKeyDriver,
                                               tam_io.win_drivers.WINUtilitiesDriver).get_io()


class WinGlobalsTests(unittest.TestCase):
    def test_win_stable(self):
        self.assertIsInstance(tam_io.win_drivers.WIN_STABLE, bool)


@unittest.skipIf(get_win_io() is None, "Console does not support WIN Drivers")
class WinDriversTests(unittest.TestCase):
    def test_able_to_execute(self):
        io = get_win_io()
        self.assertEqual(tam_io.win_drivers.WIN_STABLE, io.able_to_execute())

    def test_set_slash_get_mode(self):
        io = get_win_io()
        io.set_mode(tam_io.io_tam.MODE_2)
        self.assertEqual(io.get_mode(), tam_io.io_tam.MODE_2)

    def test_get_modes(self):
        io = get_win_io()
        modes = io.get_modes()
        self.assertIsInstance(modes, tuple)
        self.assertEqual(modes, (tam_io.io_tam.MODE_2, tam_io.io_tam.MODE_16))

    @staticmethod
    def test__draw_2():
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_dimension", return_value=(15, 10)) as _get_dimension:
            with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                with unittest.mock.patch.object(io, "_print", return_value=None) as _print:
                    io.set_mode(tam_io.io_tam.MODE_2)
                    buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", RED, GREEN)
                    buffer2 = tam_io.tam_buffer.TAMBuffer(15, 10, " ", RED, GREEN)

                    buffer.set_spot(1, 1, "B", PURPLE, WHITE)
                    buffer.set_spot(4, 4, "C", PURPLE, WHITE)
                    buffer.set_spot(4, 5, "D", PURPLE, WHITE)

                    buffer2.draw_onto(buffer, 5, 2)
                    io.draw(buffer)

                    _get_dimension.assert_called()
                    clear.assert_called_once_with()
                    _print.assert_called_once_with(0, 0, "".join(c for c in str(buffer2) if c != "\n"), 1, 2)

    def test__draw_16(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_dimension", return_value=(15, 10)) as _get_dimension:
            with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                with unittest.mock.patch.object(io, "_print", return_value=None) as _print:
                    io.set_mode(tam_io.io_tam.MODE_16)
                    buffer = tam_io.tam_buffer.TAMBuffer(5, 6, "A", RED, GREEN)
                    buffer2 = tam_io.tam_buffer.TAMBuffer(15, 10, " ", RED, GREEN)

                    buffer.set_spot(1, 1, "B", PURPLE, WHITE)
                    buffer.set_spot(3, 5, "C", PURPLE, WHITE)
                    buffer.set_spot(4, 5, "D", PURPLE, WHITE)
                    buffer.set_spot(1, 2, " ", PURPLE, GREEN)

                    buffer2.draw_onto(buffer, 5, 2)
                    io.draw(buffer)

                    _get_dimension.assert_called()
                    clear.assert_called_once_with()

                    self.assertEqual(_print.call_count, 16)

                    self.assertEqual(_print.mock_calls[0], unittest.mock.call(0, 0, "." * 35, 2, 2))
                    self.assertEqual(_print.mock_calls[1], unittest.mock.call(5, 2, "A" * 5, 1, 2))
                    self.assertEqual(_print.mock_calls[2], unittest.mock.call(10, 2, "." * 10, 2, 2))
                    self.assertEqual(_print.mock_calls[3], unittest.mock.call(5, 3, "A", 1, 2))
                    self.assertEqual(_print.mock_calls[4], unittest.mock.call(6, 3, "B", 5, 7))
                    self.assertEqual(_print.mock_calls[10], unittest.mock.call(10, 5, "." * 10, 2, 2))
                    self.assertEqual(_print.mock_calls[15], unittest.mock.call(10, 7, "." * 35, 2, 2))

    def test_start(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_clear", return_value=None) as _clear:
            with unittest.mock.patch.object(tam_io.win_drivers.io,
                                            "_show_console_cursor",
                                            return_value=None) as _show_console_cursor:
                io.start()

                _clear.assert_called_once_with()
                self.assertEqual(_show_console_cursor.call_count, 2)

    def test_done(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_default_color", return_value=2) as _get_default_color:
            with unittest.mock.patch.object(tam_io.win_drivers.io, "_set_cursor_info", return_value=None) as _set_cursor_info:
                with unittest.mock.patch.object(tam_io.win_drivers.io, "_clear", return_value=None) as _clear:
                    with unittest.mock.patch.object(tam_io.win_drivers.io,
                                                    "_show_console_cursor",
                                                    return_value=None) as _show_console_cursor:
                        io.done()

                        _get_default_color.assert_called_once_with()
                        _set_cursor_info.assert_called_once_with(0, 0, 2)
                        _clear.assert_called_once_with()
                        self.assertEqual(_show_console_cursor.call_count, 2)

    def test_get_key(self):
        io = get_win_io()
        io.enable_console_keys(True)
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_key", side_effect=[65, -1]) as _get_key:
            self.assertEqual(io.get_key(), ("A", "NORMAL"))

            self.assertEqual(_get_key.call_count, 2)

    def test_get_key_2(self):
        io = get_win_io()
        io.enable_console_keys(True)
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_key", side_effect=[224, 72, -1]) as _get_key:
            self.assertEqual(io.get_key(), ("UP", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 3)

    def test_get_key_3(self):
        io = get_win_io()
        io.enable_console_keys(True)
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_key", side_effect=[224, 134, -1]) as _get_key:
            self.assertEqual(io.get_key(), ("F12", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 3)

    def test_get_key_4(self):
        io = get_win_io()
        io.enable_console_keys(True)
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_key", side_effect=[155, 65, -1]) as _get_key:
            self.assertEqual(io.get_key(), False)

            self.assertEqual(_get_key.call_count, 3)

    def test_get_key_5(self):
        io = get_win_io()
        io.enable_console_keys(True)
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_key", side_effect=[66, -1, 224, 83, -1]) as _get_key:
            self.assertEqual(io.get_key(), ("B", "NORMAL"))
            self.assertEqual(io.get_key(), ("DELETE", "SPECIAL"))

            self.assertEqual(_get_key.call_count, 5)

    def test_get_dimensions(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_dimension", return_value=(20, 25)) as _get_dimension:
            self.assertEqual(io.get_dimensions(), (20, 25))

            _get_dimension.assert_called_once_with()

    def test_get_key_dict(self):
        io = get_win_io()
        keys = io.get_key_dict()
        for key in keys:
            self.assertIsInstance(key, str)
            self.assertIsInstance(keys.get(key), tuple)

    @staticmethod
    def test__print():
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_set_cursor_info", return_value=None) as _set_cursor_info:
            with unittest.mock.patch.object(sys.stdout, "write", return_value=None) as write:
                with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                    io._print(10, 12, "test", 2, 5)

                    _set_cursor_info.assert_called_once_with(10, 12, 82)
                    write.assert_called_once_with("test")
                    flush.assert_called_once_with()

    @staticmethod
    def test__print_2():
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_set_cursor_info", return_value=None) as _set_cursor_info:
            with unittest.mock.patch.object(sys.stdout, "write", return_value=None) as write:
                with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                    io._print(102, 124, "test123", 123, 5)

                    _set_cursor_info.assert_called_once_with(102, 124, 91)
                    write.assert_called_once_with("test123")
                    flush.assert_called_once_with()

    @staticmethod
    def test__print_3():
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_set_cursor_info", return_value=None) as _set_cursor_info:
            with unittest.mock.patch.object(sys.stdout, "write", return_value=None) as write:
                with unittest.mock.patch.object(sys.stdout, "flush", return_value=None) as flush:
                    io._print(-102, -124, "", -123, 5)

                    _set_cursor_info.assert_called_once_with(-102, -124, 85)
                    write.assert_called_once_with("")
                    flush.assert_called_once_with()

    def test__processes_special_color_1(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_default_color", return_value=55) as _get_default_color:
            colors = io._processes_special_color(4, 5)
            _get_default_color.assert_not_called()
            self.assertEqual(colors, (4, 5))

    def test__processes_special_color_2(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_default_color", return_value=55) as _get_default_color:
            colors = io._processes_special_color(-1, -1)
            _get_default_color.assert_called_once_with()
            self.assertEqual(colors, (7, 3))

    def test__processes_special_color_3(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_default_color", return_value=55) as _get_default_color:
            colors = io._processes_special_color(-1, 0)
            _get_default_color.assert_called_once_with()
            self.assertEqual(colors, (7, 0))

    def test__processes_special_color_4(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_default_color", return_value=43) as _get_default_color:
            colors = io._processes_special_color(4, -1)
            _get_default_color.assert_called_once_with()
            self.assertEqual(colors, (4, 2))

    def test__processes_special_color_5(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_default_color", return_value=55) as _get_default_color:
            colors = io._processes_special_color(-2, 0)
            _get_default_color.assert_called_once_with()
            self.assertEqual(colors, (7, 0))

    def test__processes_special_color_6(self):
        io = get_win_io()
        with unittest.mock.patch.object(tam_io.win_drivers.io, "_get_default_color", return_value=43) as _get_default_color:
            colors = io._processes_special_color(4, -2)
            _get_default_color.assert_called_once_with()
            self.assertEqual(colors, (4, 2))

    def test_reset_colors_to_console_defaults(self):
        io = get_win_io()
        io.reset_colors_to_console_defaults()

    def test_set_tam_color_defaults(self):
        io = get_win_io()
        io.set_tam_color_defaults()
        io.reset_colors_to_console_defaults()

    def test__console_color_count(self):
        io = get_win_io()
        self.assertEqual(io._console_color_count(), 16)

    def test__spot_swap(self):
        io = get_win_io()
        for spot in range(1000):
            self.assertIsInstance(io._spot_swap(spot), int)
