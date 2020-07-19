# built in libraries
import unittest.mock

# tamcolors libraries
from tamcolors import tam_tools


class TAMKeyManagerTests(unittest.TestCase):
    def test_init_key_manger(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        self.assertIsInstance(key_manger, tam_tools.tam_key_manager.TAMKeyManager)

    def test_iter(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("a", "NORMAL"), ("B", "NORMAL")))
        count = None
        for count, key in enumerate(key_manger):
            self.assertIsInstance(key, tuple)
        self.assertEqual(count, 1)

    def test_update(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("a", "NORMAL"), ("B", "NORMAL")))

        self.assertEqual(key_manger.get_raw_user_input(), (("a", "NORMAL"), ("B", "NORMAL")))

    def test_update_2(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("!", "NORMAL"),))

        self.assertEqual(key_manger.get_raw_user_input(), (("!", "NORMAL"),))

    def test_get_key_state(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        self.assertFalse(key_manger.get_key_state("A"))

    def test_get_key_state_2(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("a", "NORMAL"), ("B", "NORMAL")))

        self.assertFalse(key_manger.get_key_state("A"))
        self.assertTrue(key_manger.get_key_state("a"))
        self.assertTrue(key_manger.get_key_state("B"))

    def test_silent_key_state(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()

        self.assertFalse(key_manger.silent_key_state("A"))
        self.assertFalse(key_manger.silent_key_state("A"))

    def test_silent_key_state_2(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("a", "NORMAL"), ("B", "NORMAL")))

        self.assertTrue(key_manger.silent_key_state("B"))
        self.assertFalse(key_manger.silent_key_state("B"))

    def test_silent_key_state_3(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("A", "NORMAL"), ("C", "NORMAL")))

        self.assertTrue(key_manger.silent_key_state("C"))
        self.assertFalse(key_manger.silent_key_state("C"))
        self.assertTrue(key_manger.silent_key_state("A"))
        self.assertFalse(key_manger.silent_key_state("A"))
        self.assertFalse(key_manger.silent_key_state("B"))
        self.assertFalse(key_manger.silent_key_state("B"))

        key_manger.update((("a", "NORMAL"), ("B", "NORMAL")))

        self.assertTrue(key_manger.silent_key_state("B"))
        self.assertFalse(key_manger.silent_key_state("B"))

    def test_get_user_input(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()

        self.assertIs(key_manger.get_user_input(), None)
        self.assertIs(key_manger.get_user_input(), None)

    def test_get_user_input_2(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("A", "NORMAL"), ("C", "NORMAL")))

        self.assertEqual(key_manger.get_user_input(), ("A", "NORMAL"))
        self.assertEqual(key_manger.get_user_input(), ("C", "NORMAL"))
        self.assertIs(key_manger.get_user_input(), None)

    def test_get_user_input_3(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("X", "NORMAL"),))

        self.assertEqual(key_manger.get_user_input(), ("X", "NORMAL"))
        self.assertIs(key_manger.get_user_input(), None)

        key_manger.update((("A", "NORMAL"), ("C", "NORMAL")))

        self.assertEqual(key_manger.get_user_input(), ("A", "NORMAL"))
        self.assertEqual(key_manger.get_user_input(), ("C", "NORMAL"))
        self.assertIs(key_manger.get_user_input(), None)

    def test_get_raw_user_input(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()

        self.assertEqual(list(key_manger.get_raw_user_input()), [])

    def get_raw_user_input_2(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("A", "NORMAL"), ("C", "NORMAL")))

        self.assertEqual(list(key_manger.get_raw_user_input()), [("A", "NORMAL"), ("C", "NORMAL")])

    def get_raw_user_input_3(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()
        key_manger.update((("A", "NORMAL"), ("C", "NORMAL")))

        self.assertEqual(list(key_manger.get_raw_user_input()), [("A", "NORMAL"), ("C", "NORMAL")])

        key_manger.update((("4", "NORMAL"), ("1", "NORMAL")))
        self.assertEqual(list(key_manger.get_raw_user_input()), [("4", "NORMAL"), ("1", "NORMAL")])

    def test_get_user_input_generator(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()

        key_generator = key_manger.get_user_input_generator()
        self.assertRaises(StopIteration, next, key_generator)

    def test_get_user_input_generator_2(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()

        key_generator = key_manger.get_user_input_generator()
        self.assertRaises(StopIteration, next, key_generator)

        key_manger.update((("A", "NORMAL"), ("C", "NORMAL")))

        key_generator = key_manger.get_user_input_generator()
        self.assertEqual(next(key_generator), ("A", "NORMAL"))
        self.assertEqual(next(key_generator), ("C", "NORMAL"))
        self.assertRaises(StopIteration, next, key_generator)

    def test_get_user_input_generator_3(self):
        key_manger = tam_tools.tam_key_manager.TAMKeyManager()

        key_generator = key_manger.get_user_input_generator()
        self.assertRaises(StopIteration, next, key_generator)

        key_manger.update((("B", "NORMAL"), ("C", "NORMAL")))

        key_generator = key_manger.get_user_input_generator()
        self.assertEqual(next(key_generator), ("B", "NORMAL"))
        self.assertEqual(next(key_generator), ("C", "NORMAL"))
        self.assertRaises(StopIteration, next, key_generator)

        key_manger.update((("B", "NORMAL"), ("C", "NORMAL"), ("5", "NORMAL")))

        key_generator = key_manger.get_user_input_generator()
        self.assertEqual(next(key_generator), ("B", "NORMAL"))
        self.assertEqual(next(key_generator), ("C", "NORMAL"))
        self.assertEqual(next(key_generator), ("5", "NORMAL"))
        self.assertRaises(StopIteration, next, key_generator)
