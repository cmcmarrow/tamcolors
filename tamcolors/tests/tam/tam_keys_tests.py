# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam


class TAMKeyTests(unittest.TestCase):
    def test_keys(self):
        self.assertIsInstance(tam.tam_keys.KEYS, set)
        for key in tam.tam_keys.KEYS:
            self.assertIsInstance(key, tuple)
            self.assertEqual(len(key), 2)
            self.assertIsInstance(key[0], str)
            self.assertIsInstance(key[1], str)
