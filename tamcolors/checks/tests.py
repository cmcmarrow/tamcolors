# built in library
import unittest

# Charles McMarrow library
from tamcolors import checks

# Charles McMarrow

"""
test that checks all checks functions 
"""


class RangeCheckTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(checks.checks.range_check(0, 0, 2), True)

    def test_2(self):
        self.assertEqual(checks.checks.range_check(1, 0, 2), True)

    def test_3(self):
        self.assertEqual(checks.checks.range_check(2, 0, 3), True)

    def test_4(self):
        self.assertEqual(checks.checks.range_check(100, 0, None), True)

    def test_5(self):
        self.assertEqual(checks.checks.range_check(-100, None, 2), True)

    def test_6(self):
        self.assertEqual(checks.checks.range_check(0, None, None), True)

    def test_7(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.range_check, -1, 0, 2)

    def test_8(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.range_check, 2, 0, 2)

    def test_9(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.range_check, -1, 0, None)

    def test_10(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.range_check, 3, None, 2)

    def test_11(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.range_check, [], 0, 2)

    def test_12(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.range_check, int, 0, 2)


class CharCheckTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(checks.checks.char_check("$"), True)

    def test_2(self):
        self.assertEqual(checks.checks.char_check(" "), True)

    def test_3(self):
        self.assertEqual(checks.checks.char_check("\n"), True)

    def test_4(self):
        self.assertEqual(checks.checks.char_check("\t"), True)

    def test_5(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.char_check, "$$")

    def test_6(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.char_check, "")

    def test_7(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.char_check, "$"*100)

    def test_8(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.char_check, [])

    def test_9(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.char_check, None)

    def test_10(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.char_check, str)


class FunctionCheckTest(unittest.TestCase):
    def test_1(self):
        def func(a, b, c):
            pass
        self.assertEqual(checks.checks.function_check(func, 3, False, False), True)

    def test_2(self):
        def func(a, b, c, *args):
            pass
        self.assertEqual(checks.checks.function_check(func, 3, True, False), True)

    def test_3(self):
        def func(a, b, c, **kwargs):
            pass
        self.assertEqual(checks.checks.function_check(func, 3, False, True), True)

    def test_4(self):
        def func(a, b, c, *args, **kwargs):
            pass
        self.assertEqual(checks.checks.function_check(func, 3, True, True), True)

    def test_5(self):
        def func(*args, **kwargs):
            pass
        self.assertEqual(checks.checks.function_check(func, 0, True, True), True)

    def test_6(self):
        def func():
            pass
        self.assertEqual(checks.checks.function_check(func, 0, False, False), True)

    def test_7(self):
        def func(a, b, c, d, e):
            pass
        self.assertEqual(checks.checks.function_check(func, 5, False, False), True)

    def test_8(self):
        def func(a, b, c, d, e):
            pass
        self.assertRaises(checks.checks.ChecksError, checks.checks.function_check, func, 5, True, False)

    def test_9(self):
        def func(a, b, c, d, e):
            pass
        self.assertRaises(checks.checks.ChecksError, checks.checks.function_check, func, 5, False, True)

    def test_10(self):
        def func(a, b, c, d, e):
            pass
        self.assertRaises(checks.checks.ChecksError, checks.checks.function_check, func, 6, False, False)

    def test_11(self):
        def func(a, b, c, *args):
            pass
        self.assertRaises(checks.checks.ChecksError, checks.checks.function_check, func, 3, True, True)

    def test_12(self):
        def func(a, b, c, *args):
            pass

        self.assertEqual(checks.checks.function_check(func, 3, None, False), True)

    def test_13(self):
        def func(a, b, c, **kwargs):
            pass

        self.assertEqual(checks.checks.function_check(func, 3, False, None), True)

    def test_14(self):
        def func(a, b, c):
            pass

        self.assertEqual(checks.checks.function_check(func, 3, None, False), True)

    def test_15(self):
        def func(a, b, c):
            pass

        self.assertEqual(checks.checks.function_check(func, 3, False, None), True)

    def test_16(self):
        def func(a, b, c):
            pass

        self.assertEqual(checks.checks.function_check(func, 3, None, None), True)


class ListKeyCheckTest(unittest.TestCase):
    def test_1(self):
        list_of_dicts = [{"a": 1, "b": 2, "c": 3},
                         {"a": 1, "b": 2, "c": 3},
                         {"a": 1, "b": 2, "c": 3}]
        self.assertEqual(checks.checks.list_key_check(list_of_dicts, ["a", "b", "c"]), True)

    def test_2(self):
        list_of_dicts = [{"a": 1, "b": 2, "c": 3},
                         {"a": 1, "b": 2, "c": 3},
                         {"a": 1, "b": 2, "c": 3}]
        self.assertEqual(checks.checks.list_key_check(list_of_dicts, ["a", "b"]), True)

    def test_3(self):
        list_of_dicts = [{"a": 1, "b": 2, "c": 3},
                         {"a": 1, "b": 2, "c": 3},
                         {"a": 1, "b": 2, "c": 3}]
        self.assertRaises(checks.checks.ChecksError, checks.checks.list_key_check, list_of_dicts, ["d"])

    def test_4(self):
        list_of_dicts = [{"a": 1, "b": 2, "c": 3},
                         {"a": 1, "b": 2, "c": 3},
                         {"a": 1, "b": 2}]
        self.assertRaises(checks.checks.ChecksError, checks.checks.list_key_check, list_of_dicts, ["a", "b", "c"])


class TypeCheckTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(checks.checks.type_check(1, int), True)

    def test_2(self):
        self.assertEqual(checks.checks.type_check("cats", str), True)

    def test_3(self):
        self.assertEqual(checks.checks.type_check({1: 2, "cats": "yes"}, dict), True)

    def test_4(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.type_check, 1, str)

    def test_5(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.type_check, "cats", int)

    def test_6(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.type_check, {1: 2, "cats": "yes"}, list)


class ItemInObjectTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(checks.checks.item_in_object(1, [4, 2, 6, 1]), True)

    def test_2(self):
        self.assertEqual(checks.checks.item_in_object(1, (4, 2, 6, 1)), True)

    def test_3(self):
        self.assertEqual(checks.checks.item_in_object(1, {1: 2, 5: 6}), True)

    def test_4(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.item_in_object, 1, [4, 2, 6, "cats"])

    def test_5(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.item_in_object, 1, (4, 2, 6, 9))

    def test_6(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.item_in_object, 1, {3: 2, 5: 6})


class InstanceCheckTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(checks.checks.instance_check([], list), True)

    def test_2(self):
        self.assertEqual(checks.checks.instance_check(5, int), True)

    def test_3(self):
        self.assertEqual(checks.checks.instance_check("cats", object), True)

    def test_4(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.instance_check, [], str)

    def test_5(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.instance_check, [], int)


class InInstancesCheck(unittest.TestCase):
    def test_1(self):
        self.assertTrue(checks.checks.in_instances_check(3, (float, int)))

    def test_2(self):
        self.assertTrue(checks.checks.in_instances_check((), [tuple, list, int, float]))

    def test_3(self):
        self.assertTrue(checks.checks.in_instances_check("cats", (str,)))

    def test_4(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.in_instances_check, "cats", [])

    def test_5(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.in_instances_check, 117, [float, dict, tuple, set])


class SingleBlockCharCheckTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(checks.checks.single_block_char_check("$"), True)

    def test_2(self):
        self.assertEqual(checks.checks.single_block_char_check(" "), True)

    def test_3(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.single_block_char_check, "\n")

    def test_4(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.single_block_char_check, "\t")

    def test_5(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.single_block_char_check, "$$")

    def test_6(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.single_block_char_check, "")

    def test_7(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.single_block_char_check, "$"*100)

    def test_8(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.single_block_char_check, [])

    def test_9(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.single_block_char_check, None)

    def test_10(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.single_block_char_check, str)


class HasMethodCheckTest(unittest.TestCase):
    def test_1(self):
        self.assertTrue(checks.checks.has_method_check(32, "conjugate"))

    def test_2(self):
        self.assertTrue(checks.checks.has_method_check("cats", "split"))

    def test_3(self):
        class Blank:
            pass
        self.assertRaises(checks.checks.ChecksError, checks.checks.has_method_check, Blank(), "blank")


class IsEqualCheckTest(unittest.TestCase):
    def test_1(self):
        self.assertTrue(checks.checks.is_equal_check(12, 12))

    def test_2(self):
        self.assertTrue(checks.checks.is_equal_check("cats", "cats"))

    def test_3(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_equal_check, "na", "blank")

    def test_4(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_equal_check, "na", 45)


class AnyCheckTest(unittest.TestCase):
    def test_1(self):
        self.assertTrue(checks.checks.any_check(4, 2, True))

    def test_2(self):
        self.assertTrue(checks.checks.any_check(0, 0, False, 1))

    def test_3(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.any_check, 0, 0, False, 0)


class IsFunctionCheck(unittest.TestCase):
    def test_1(self):
        self.assertTrue(checks.checks.is_function_check(lambda x: x))

    def test_2(self):
        def foo():
            pass

        self.assertTrue(checks.checks.is_function_check(foo))

    def test_3(self):
        class Bar:
            def __init__(self):
                pass

            def __call__(self):
                pass

        self.assertTrue(checks.checks.is_function_check(Bar()))

    def test_4(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_function_check, "cats")

    def test_5(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_function_check, 123)


class IsJson(unittest.TestCase):
    def test_1(self):
        self.assertTrue(checks.checks.is_json(4, int))

    def test_2(self):
        self.assertTrue(checks.checks.is_json("cats", str))

    def test_3(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, object(), object)

    def test_4(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, dict, dict)

    def test_5(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, {}, str)

    def test_6(self):
        self.assertTrue(checks.checks.is_json(4.4))

    def test_7(self):
        self.assertTrue(checks.checks.is_json("cats"))

    def test_8(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, object())

    def test_9(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, float)

    def test_10(self):
        self.assertTrue(checks.checks.is_json([4, 5, 6], (list, tuple)))

    def test_11(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, {}, (int, float, str))

    def test_12(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, [4, 5, 6, object])

    def test_13(self):
        self.assertTrue(checks.checks.is_json({"cats": 45, "5": [324]}))

    def test_14(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, {"cats": 45, 5: [324]})

    def test_15(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, {"cats": object, "5": [324]})

    def test_16(self):
        self.assertRaises(checks.checks.ChecksError, checks.checks.is_json, {"cats": 45, "5": [object]})
