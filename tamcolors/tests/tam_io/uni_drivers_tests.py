# built in libraries
import platform
import os
import sys
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


def get_uni_io():
    return tam_io.tam_identifier.TAMIdentifier("uni_driver_tests",
                                               tam_io.any_drivers.ANYColorDriver,
                                               tam_io.any_drivers.ANYColorChangerDriver,
                                               tam_io.uni_drivers.UNIKeyDriver,
                                               tam_io.uni_drivers.UNIUtilitiesDriver).get_io()


@unittest.skipIf(get_uni_io() is None, "Console does not support UNI Drivers")
class UniIOTests(unittest.TestCase):
    def test_able_to_execute(self):
        io = get_uni_io()
        self.assertEqual(tam_io.uni_drivers.UNI_STABLE, io.able_to_execute())

    def test_set_slash_get_mode(self):
        io = get_uni_io()
        io.set_mode(tam_io.io_tam.MODE_2)
        self.assertEqual(io.get_mode(), tam_io.io_tam.MODE_2)

    def test_get_modes(self):
        io = get_uni_io()
        modes = io.get_modes()
        self.assertIsInstance(modes, tuple)

    @staticmethod
    def test_start():
        io = get_uni_io()
        with unittest.mock.patch.object(tam_io.uni_drivers.io, "_enable_get_key", return_value=None) as _enable_get_key:
            with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                    io.start()

                    _enable_get_key.assert_called_once_with()
                    clear.assert_called_once_with()
                    _show_console_cursor.assert_called_once_with(False)

    @staticmethod
    def test_done():
        io = get_uni_io()
        with unittest.mock.patch.object(os, "system", return_value=None) as system:
            with unittest.mock.patch.object(tam_io.uni_drivers.io, "_disable_get_key", return_value=None) as _disable_get_key:
                with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                    with unittest.mock.patch.object(io, "_show_console_cursor", return_value=None) as _show_console_cursor:
                        io.done()

                        _disable_get_key.assert_called_once_with()
                        clear.assert_called_once_with()
                        _show_console_cursor.assert_called_once_with(True)
                        system.assert_called_once_with("clear")

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
        self.assertEqual(io._get_lin_tam_color(2, 5), ("38;2;19;161;14", "48;2;136;23;152"))

    def test__get_lin_tam_color_2(self):
        io = tam_io.uni_tam.UniIO()
        self.assertEqual(io._get_lin_tam_color(-1, -1), ("39", "49"))

    def test__get_lin_tam_color_3(self):
        io = tam_io.uni_tam.UniIO()
        self.assertEqual(io._get_lin_tam_color(-2, -2), ("39", "49"))

    @staticmethod
    def test_clear():
        with unittest.mock.patch.object(os, "system", return_value=0) as system:
            io = tam_io.uni_tam.UniIO()
            io.clear()
            system.assert_called_once_with("tput reset")

    def test_reset_colors_to_console_defaults(self):
        io = tam_io.uni_tam.UniIO()
        io.reset_colors_to_console_defaults()

    def test_set_tam_color_defaults(self):
        io = tam_io.uni_tam.UniIO()
        io.set_tam_color_defaults()
