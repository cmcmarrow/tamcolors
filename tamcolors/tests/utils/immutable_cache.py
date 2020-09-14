# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors.utils.immutable_cache import ImmutableCache


class DummyCache(ImmutableCache):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs


class ImmutableCacheTests(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(DummyCache(1, 2, 3, 4), DummyCache)

    def test_new(self):
        obj_1 = DummyCache.__new__(DummyCache)
        obj_2 = DummyCache.__new__(DummyCache)

        self.assertIsNot(obj_1, obj_2)

    def test_cache(self):
        obj_1 = DummyCache(1, 2, 3, 4)
        obj_2 = DummyCache(1, 2, 3, 4)
        obj_3 = DummyCache(1, 2, 4, 3)

        self.assertIs(obj_1, obj_2)
        self.assertIsNot(obj_1, obj_3)
