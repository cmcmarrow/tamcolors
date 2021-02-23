# built in libraries
import unittest

# tamcolors libraries
from tamcolors.utils import id_manager


class IDManagerTests(unittest.TestCase):
    def test_id_manager_init(self):
        self.assertIsInstance(id_manager.IDManager(), id_manager.IDManager)

    def test_free_and_get(self):
        manager = id_manager.IDManager()
        mid = manager.get_id()
        self.assertIsInstance(mid, int)
        self.assertEqual(mid, 0)
        self.assertTrue(manager.free_id(mid))
        for _ in range(10):
            self.assertFalse(manager.free_id(min))

    def test_flex_id_manger(self):
        manager = id_manager.IDManager()
        used_ids = set()

        for i in range(10000):
            mid = manager.get_id()
            self.assertIsInstance(mid, int)
            self.assertEqual(mid, i)
            used_ids.add(mid)

        for _ in range(1000):
            mid = used_ids.pop()
            self.assertTrue(manager.free_id(mid))
            for _ in range(10):
                self.assertFalse(manager.free_id(min))

        for _ in range(10000):
            mid = manager.get_id()
            self.assertIsInstance(mid, int)
            used_ids.add(mid)

        while used_ids:
            mid = used_ids.pop()
            self.assertTrue(manager.free_id(mid))
            for _ in range(10):
                self.assertFalse(manager.free_id(min))

        self.assertEqual(manager.get_id(), 0)
