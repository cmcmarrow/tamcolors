# built in libraries
import unittest
import unittest.mock

# tamcolors libraries
from tamcolors import tam_basic
from tamcolors import tam_io


class IOTests(unittest.TestCase):
    def test_IO(self):
        self.assertIsInstance(tam_basic.basic.IO, tam_io.io_tam.IO)


class ColorNameToCodeTests(unittest.TestCase):
    def test_color_name_to_color_1(self):
        self.assertIsInstance(tam_basic.basic._COLOR_NAME_TO_CODE, dict)

    def test_color_name_to_color_2(self):
        self.assertEqual(tam_basic.basic._COLOR_NAME_TO_CODE["light aqua"], tam_io.tam_colors.LIGHT_AQUA)


class GetColorCodeTests(unittest.TestCase):
    def test__get_color_code_1(self):
        self.assertEqual(tam_basic.basic._get_color_code((tam_io.tam_colors.BLUE, "black")),
                         (tam_io.tam_colors.BLUE, tam_io.tam_colors.BLACK))

    def test__get_color_code_2(self):
        self.assertEqual(tam_basic.basic._get_color_code(["red", "gray"]), (tam_io.tam_colors.RED,
                                                                            tam_io.tam_colors.GRAY))

    def test__get_color_code_3(self):
        self.assertEqual(tam_basic.basic._get_color_code(("sahfjakslASDFsklf", tam_io.tam_colors.DEFAULT)),
                         ("sahfjakslASDFsklf", tam_io.tam_colors.DEFAULT))

    def test__get_color_code_4(self):
        self.assertEqual(tam_basic.basic._get_color_code(([4, 5, 6], (255, 0, 117))), ([4, 5, 6], (255, 0, 117)))


class PrintCTests(unittest.TestCase):
    @staticmethod
    def test_same_color():
        with unittest.mock.patch.object(tam_basic.basic.IO, "printc", return_value=None) as printc:
            tam_basic.basic.printc("cats", "dogs", "test", ("green", "gray"), same_color=True, sep="$$*", end="!\n")
            printc.assert_called_once_with("cats$$*dogs$$*test!\n",
                                           (tam_io.tam_colors.GREEN, tam_io.tam_colors.GRAY),
                                           True,
                                           False)

    def test_not_same_color(self):
        with unittest.mock.patch.object(tam_basic.basic.IO, "printc", return_value=None) as printc:
            tam_basic.basic.printc("cats",
                                   (tam_io.tam_colors.BLUE, tam_io.tam_colors.WHITE),
                                   "test",
                                   ("green", "gray"),
                                   sep="+!",
                                   end="\n!\n")
            self.assertEqual(printc.call_count, 2)
            self.assertEqual(printc.mock_calls[0], unittest.mock.call("cats+!",
                                                                      (tam_io.tam_colors.BLUE, tam_io.tam_colors.WHITE),
                                                                      True,
                                                                      False))
            self.assertEqual(printc.mock_calls[1], unittest.mock.call("test\n!\n",
                                                                      (tam_io.tam_colors.GREEN, tam_io.tam_colors.GRAY),
                                                                      True,
                                                                      False))

    def test_flush_and_stderr(self):
        with unittest.mock.patch.object(tam_basic.basic.IO, "printc", return_value=None) as printc:
            tam_basic.basic.printc("cats",
                                   (tam_io.tam_colors.BLUE, tam_io.tam_colors.WHITE),
                                   "test",
                                   ("green", "gray"),
                                   sep="+!",
                                   end="\n!\n",
                                   flush=False,
                                   stderr=True)
            self.assertEqual(printc.call_count, 2)
            self.assertEqual(printc.mock_calls[0], unittest.mock.call("cats+!",
                                                                      (tam_io.tam_colors.BLUE, tam_io.tam_colors.WHITE),
                                                                      False,
                                                                      True))
            self.assertEqual(printc.mock_calls[1], unittest.mock.call("test\n!\n",
                                                                      (tam_io.tam_colors.GREEN, tam_io.tam_colors.GRAY),
                                                                      False,
                                                                      True))


class InputCTests(unittest.TestCase):
    def test_inputc(self):
        with unittest.mock.patch.object(tam_basic.basic.IO, "inputc", return_value=None) as inputc:
            tam_basic.basic.inputc(">>> ", (tam_io.tam_colors.RED, "BluE"))
            inputc.asset_called_once_with(">>> ", (tam_io.tam_colors.RED, tam_io.tam_colors.LIGHT_BLUE))


class ClearTests(unittest.TestCase):
    @staticmethod
    def test_clear():
        with unittest.mock.patch.object(tam_basic.basic.IO, "clear", return_value=None) as clear:
            tam_basic.basic.clear()
            clear.assert_called_once_with()
