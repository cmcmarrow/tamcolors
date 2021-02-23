# built in libraries
import unittest

# tamcolors libraries
from tamcolors.utils import path


class PathTests(unittest.TestCase):
    def test_abspath(self):
        self.assertIn("cats", path.abspath("cats"))

    def test_abspath2(self):
        self.assertIn("cats", path.abspath("tamcolors", "d", "cats"))
