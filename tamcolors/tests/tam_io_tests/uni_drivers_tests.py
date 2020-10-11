# built in libraries
import os
import unittest
import unittest.mock
import sys

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
        with unittest.mock.patch.object(io, "enable_console_keys", return_value=None) as enable_console_keys:
            with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                with unittest.mock.patch.object(io, "show_console_cursor", return_value=None) as show_console_cursor:
                    io.start()

                    enable_console_keys.assert_called_once_with(True)
                    clear.assert_called_once_with()
                    show_console_cursor.assert_called_once_with(False)

    @staticmethod
    def test_done():
        io = get_uni_io()
        with unittest.mock.patch.object(os, "system", return_value=None) as system:
            with unittest.mock.patch.object(io, "enable_console_keys", return_value=None) as enable_console_keys:
                with unittest.mock.patch.object(io, "clear", return_value=None) as clear:
                    with unittest.mock.patch.object(io, "show_console_cursor", return_value=None) as show_console_cursor:
                        io.done()

                        enable_console_keys.assert_called_once_with(False)
                        clear.assert_called_once_with()
                        show_console_cursor.assert_called_once_with(True)
                        system.assert_called_once_with("clear")

    def test_get_key(self):
        io = get_uni_io()
        try:
            with unittest.mock.patch.object(tam_io.uni_drivers.io, "_get_key", side_effect=[65, -1]) as _get_key:
                io.enable_console_keys(True)
                self.assertEqual(io.get_key(), ("A", "NORMAL"))

                self.assertEqual(_get_key.call_count, 2)
        finally:
            io.enable_console_keys(False)

    def test_get_key_2(self):
        io = get_uni_io()
        try:
            with unittest.mock.patch.object(tam_io.uni_drivers.io, "_get_key", side_effect=[27, 91, 65, -1]) as _get_key:
                io.enable_console_keys(True)
                self.assertEqual(io.get_key(), ("UP", "SPECIAL"))

                self.assertEqual(_get_key.call_count, 4)
        finally:
            io.enable_console_keys(False)

    def test_get_key_3(self):
        io = get_uni_io()
        try:
            with unittest.mock.patch.object(tam_io.uni_drivers.io, "_get_key", side_effect=[27, 91, 50, 52, 126, -1]) as _get_key:
                io.enable_console_keys(True)
                self.assertEqual(io.get_key(), ("F12", "SPECIAL"))

                self.assertEqual(_get_key.call_count, 6)
        finally:
            io.enable_console_keys(False)

    def test_get_key_4(self):
        io = get_uni_io()
        try:
            with unittest.mock.patch.object(tam_io.uni_drivers.io, "_get_key", side_effect=[155, 65, -1]) as _get_key:
                io.enable_console_keys(True)
                self.assertEqual(io.get_key(), False)

                self.assertEqual(_get_key.call_count, 3)
        finally:
            io.enable_console_keys(False)

    def test_get_key_5(self):
        io = get_uni_io()
        try:
            with unittest.mock.patch.object(tam_io.uni_drivers.io,
                                            "_get_key", side_effect=[66, -1, 27, 91, 51, 126, -1]) as _get_key:
                io.enable_console_keys(True)
                self.assertEqual(io.get_key(), ("B", "NORMAL"))
                self.assertEqual(io.get_key(), ("DELETE", "SPECIAL"))

                self.assertEqual(_get_key.call_count, 7)
        finally:
            io.enable_console_keys(False)

    def test_get_dimensions(self):
        with unittest.mock.patch.object(tam_io.uni_drivers.io, "_get_dimension", return_value=(20, 25)) as _get_dimension:
            io = get_uni_io()

            self.assertEqual(io.get_dimensions(), (20, 25))

            _get_dimension.assert_called_once_with()

    def test_get_key_dict(self):
        keys = get_uni_io().get_key_dict()
        for key in keys:
            self.assertIsInstance(key, str)
            self.assertIsInstance(keys.get(key), tuple)

    @staticmethod
    def test_show_console_cursor():
        io = get_uni_io()
        with unittest.mock.patch.object(sys.stdout, "write") as write:
            io.show_console_cursor(True)
            write.assert_called_once_with("\u001b[?25h")

    @staticmethod
    def test_hide_console_cursor():
        io = get_uni_io()
        with unittest.mock.patch.object(sys.stdout, "write") as write:
            io.show_console_cursor(False)
            write.assert_called_once_with("\u001b[?25l")

    def test_clear(self):
        io = get_uni_io()
        with unittest.mock.patch.object(sys.stdout, "write") as write:
            with unittest.mock.patch.object(os, "system", return_value=0) as system:
                io.clear()
                self.assertEqual(system.mock_calls, [unittest.mock.call("tput reset")])
                write.assert_called_once_with("\u001b[?25h")
