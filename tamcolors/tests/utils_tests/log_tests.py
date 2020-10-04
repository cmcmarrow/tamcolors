# built in libraries
import unittest.mock
from os import remove

# tamcolors libraries
from tamcolors.utils import log


class LogTests(unittest.TestCase):
    @staticmethod
    def test_enable_and_disable_logging():
        log.disable_logging()
        log.enable_logging()
        log.enable_logging(log.ERROR)
        log.enable_logging(log.CRITICAL)
        log.disable_logging()
        log.disable_logging()
        log.enable_logging(log.DEBUG)
        log.disable_logging()

    def test_debug(self):
        try:
            log.enable_logging()
            log.debug("test")
            log.debug("dogs")
            log.critical("colors")
            with open(log.LOG_FILE_NAME) as file:
                output = "".join(file.readlines())
                self.assertIn("test", output)
                self.assertIn("dogs", output)
                self.assertIn("colors", output)
        finally:
            log.disable_logging()
            remove(log.LOG_FILE_NAME)

    def test_critical(self):
        try:
            log.enable_logging(log.CRITICAL)
            log.debug("test2")
            log.debug("cats2")
            log.critical("colors2")
            with open(log.LOG_FILE_NAME) as file:
                output = "".join(file.readlines())
                self.assertNotIn("dogs", output)
                self.assertNotIn("test2", output)
                self.assertNotIn("cats2", output)
                self.assertIn("colors2", output)
        finally:
            log.disable_logging()
            remove(log.LOG_FILE_NAME)
