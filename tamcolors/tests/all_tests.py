# built in libraries
import unittest
import unittest.mock
import types


# tamcolors libraries
from tamcolors import tests as all_tests


def _get_all_tests():
    module_objects = lambda module: [vars(module)[module_key] for module_key in vars(module)]

    def _get_sub_modules(modules, depth=1):
        if isinstance(modules, types.ModuleType):
            modules = (modules,)

        sub_modules = []
        for module in modules:
            for this_object in module_objects(module):
                if isinstance(this_object, types.ModuleType):
                    sub_modules.append(this_object)

        if depth != 0:
            depth -= 1
            return _get_sub_modules(sub_modules, depth)
        return sub_modules

    tests = []
    for test_module in _get_sub_modules(all_tests):
        for test_object in module_objects(test_module):
            if isinstance(test_object, type) and unittest.TestCase in test_object.__mro__:
                tests.append(test_object)

    return tests


ALL_TESTS = _get_all_tests()


def load_tests(loader, other_tests=None, pattern=None):
    suite = unittest.TestSuite()
    for test_class in ALL_TESTS:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


def tests_main(run_slow=False):
    """
    info: the main way tamcolors run tests
    :param run_slow: bool: will run slow tests
    :return:
    """

    all_tests.test_utils.enable_slow_tests(run_slow)

    suite = unittest.TestSuite()

    for test in ALL_TESTS:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test))

    unittest.TextTestRunner(verbosity=2).run(suite)


def stability_check(ret_bool=True, run_slow=False):
    """
    info: run all TAM tests
    :param ret_bool: bool
    :param run_slow: bool
    :return: (int, int) or bool: (test_pasted, test_ran) or True if all test pasted
    """

    all_tests.test_utils.enable_slow_tests(run_slow)

    suite = unittest.TestSuite()

    for test in ALL_TESTS:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test))

    test_results = unittest.TextTestRunner(stream=unittest.mock.Mock(), verbosity=2).run(suite)
    tests_out_come = (test_results.testsRun - (len(test_results.errors) + len(test_results.failures)),
                      test_results.testsRun)

    if ret_bool:
        return tests_out_come[0] == tests_out_come[1]

    return tests_out_come
