# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_tools


class MakeTAMStrTests(unittest.TestCase):
    def test_make_tam_str(self):
        tam_str = tam_tools.tam_str.make_tam_str("test\t123")
        self.assertEqual(tam_str, "test    123")

    def test_make_tam_str_2(self):
        tam_str = tam_tools.tam_str.make_tam_str("test\t12\n3")
        self.assertEqual(tam_str, "test    12\n3")

    def test_make_tam_str_3(self):
        self.assertRaises(tam_tools.tam_str.TAMStrError, tam_tools.tam_str.make_tam_str, "123\r123")

    def test_make_tam_str_4(self):
        tam_str = tam_tools.tam_str.make_tam_str("test\r12\n3", bad_char="%^&")
        self.assertEqual(tam_str, "test%^&12\n3")

    def test_make_tam_str_5(self):
        tam_str = tam_tools.tam_str.make_tam_str("\r\\\n\ng\n", end_line="45", bad_char="@")
        self.assertEqual(tam_str, "@\\4545g45")
