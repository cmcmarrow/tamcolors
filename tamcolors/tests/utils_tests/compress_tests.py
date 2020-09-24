# built in libraries
import unittest

# tamcolors libraries
from tamcolors.utils import compress


class CompressTests(unittest.TestCase):
    def test_1(self):
        self._compress_and_compare(bytes((12,)))

    def test_2(self):
        self._compress_and_compare(bytes(1237))

    def test_3(self):
        self._compress_and_compare(bytes((1, 2, 3, 4, 5, 6, 7, 44, 55, 66, 77)))

    def test_4(self):
        self._compress_and_compare(bytes([i % 256 for i in range(1000)]))

    def _compress_and_compare(self, data):
        self.assertEqual(compress.decompress(compress.compress(data)), data)
