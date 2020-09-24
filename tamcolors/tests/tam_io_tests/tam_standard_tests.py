# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_io


class StandardTest(unittest.TestCase):
    def test_same_keys(self):
        uni_key_dict = tam_io.uni_drivers.UNIKeyDriver.get_key_dict()
        win_key_dict = tam_io.win_drivers.WINKeyDriver.get_key_dict()

        uni_key_set = set([uni_key_dict[key] for key in uni_key_dict])
        win_key_set = set([win_key_dict[key] for key in win_key_dict])

        keys_sets = (uni_key_set, win_key_set, tam_io.tam_keys.KEYS)
        for key_set in keys_sets:
            for key in key_set:
                for other_key_set in keys_sets:
                    self.assertTrue(key in other_key_set)
