# built in libraries
import unittest.mock
from time import sleep

# tamcolors libraries
from tamcolors.utils.timer import Timer
from tamcolors.tests.test_utils import slow_test


class TimerTests(unittest.TestCase):
    def test_timer(self):
        timer = Timer()
        self.assertIsInstance(timer, Timer)

    def test_lap(self):
        timer = Timer()
        self.assertIsInstance(timer.lap(), float)

    @slow_test
    def test_offset_sleep(self):
        timer = Timer()
        sleep(0.5)
        ran_time, total_time = timer.offset_sleep(1)
        self.assertTrue(0.55 >= ran_time >= 0.45)
        self.assertTrue(1.05 >= total_time >= 0.95)
