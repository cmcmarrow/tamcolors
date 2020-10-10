# built in libraries
from functools import wraps


SLOW_TESTS = True


def enable_slow_tests(enable=True):
    """
    info: will enable slow tests
    :param enable: bool
    :return:
    """
    global SLOW_TESTS
    SLOW_TESTS = enable


def is_slow_tests_enabled():
    """
    info: will check iif slow tests are enabled
    :return: bool
    """
    global SLOW_TESTS
    return SLOW_TESTS


def slow_test(function):
    """
    info: slow_test decorators
    :param function: function
    :return: function
    """
    @wraps(function)
    def slow_test_wrapper(self, *args, **kwargs):
        """
        info: will skip slow test if not enable
        :param self
        :param args: tuple
        :param kwargs: dict
        :return: object
        """
        if not is_slow_tests_enabled():
            self.skipTest("Slow tests are disabled")
        return function(self, *args, **kwargs)
    return slow_test_wrapper
