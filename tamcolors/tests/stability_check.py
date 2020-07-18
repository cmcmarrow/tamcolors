import unittest

from tamcolors.tests.tam import tests as tam_tests
from tamcolors.tests.tam_tools import tests as tam_tools


def tma_stability_check(ret_bool=True):
    """
    info: run all TMA test but TMALoopTest and TMAFrameTest
    :return: (int, int) or bool: (test_pasted, test_ran) or True if all test pasted
    """

    suite = unittest.TestSuite()
    modules = (tam_tests, tam_tools)
    for module in modules:
        for obj_name in dir(module):
            if hasattr(module, obj_name):
                obj = getattr(module, obj_name)
                if hasattr(obj, "__mro__") and unittest.TestCase in obj.__mro__ and obj not in (tam_tests.TMALoopTest,
                                                                                                tam_tests.TMAFrameTest):
                    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(obj))

    test_results = unittest.TextTestRunner(stream=unittest.mock.Mock()).run(suite)
    tests_out_come = (test_results.testsRun - (len(test_results.errors) + len(test_results.failures)),
                      test_results.testsRun)

    if ret_bool:
        return tests_out_come[0] == tests_out_come[1]

    return tests_out_come
