# built in libraries
import unittest
import threading
import multiprocessing

# tamcolors libraries
from tamcolors.tests.test_multi_task_helper import MultiTaskHelper


def _test_hand(get_from, pass_to):
    if get_from is not None:
        data = get_from.get()
    else:
        data = "data"

    if pass_to is not None:
        pass_to.put(data)


def _dummy():
    pass


def _error_main_process():
    if multiprocessing.current_process().name != "MainProcess":
        assert False


def _error_not_main_process():
    if multiprocessing.current_process().name != "MainProcess":
        assert False


class MultiTaskHelperTests(MultiTaskHelper, unittest.TestCase):
    def test_assert_thread(self):
        def error():
            if threading.current_thread().name == "MainThread":
                assert False

        self.assertRaises(AssertionError, self.multiple_threads_helper, [self.task(_dummy), self.task(error)])

    def test_assert_no_main_thread(self):
        def error():
            if threading.current_thread().name != "MainThread":
                assert False

        self.assertRaises(AssertionError, self.multiple_threads_helper, [self.task(_dummy), self.task(error)])

    def test_assert_process(self):
        self.assertRaises(AssertionError, self.multiple_processes_helper, [self.task(_dummy),
                                                                           self.task(_error_main_process)])

    def test_assert_no_main_process(self):
        self.assertRaises(AssertionError, self.multiple_processes_helper, [self.task(_dummy),
                                                                           self.task(_error_not_main_process)])

    def test_hand_down(self):
        for helper in (self.multiple_threads_helper,):
            q1 = multiprocessing.Queue()
            q2 = multiprocessing.Queue()

            helper([self.task(_test_hand, None, q1),
                    self.task(_test_hand, q1, q2),
                    self.task(_test_hand, q2, None)])
