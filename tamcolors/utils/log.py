from os import getcwd
from os.path import join
import logging
from logging import handlers
from io import StringIO


"""
Enable and Disable a log file for tamcolors 
"""


LOG_FILE_NAME = join(getcwd(), "tamcolors.log")
LOGGER = logging.getLogger("tamcolors")
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

LOG_ENABLED = False

LOG_FILE = None
LOG_STREAM = None
LOGGER = logging.getLogger('tamcolors')


def enable_logging(level=DEBUG):
    """
    info: will enable logging at a level
    :param level: log level
    :return:
    """
    global LOG_ENABLED, LOG_FILE, LOG_STREAM
    if LOG_ENABLED:
        disable_logging()
    LOG_ENABLED = True
    logging.Formatter("[%(asctime)s][%(process)d %(processName)s][%(thread)d %(threadName)s][%(levelname)s] %(message)s")
    LOG_FILE = handlers.RotatingFileHandler(LOG_FILE_NAME, mode="w", maxBytes=5000000, encoding="utf-8")
    LOG_STREAM = logging.StreamHandler(StringIO())
    LOGGER.addHandler(LOG_FILE)
    LOGGER.setLevel(level)


def disable_logging():
    """
    info: will disable logging
    :return:
    """
    global LOG_ENABLED
    if LOG_ENABLED:
        LOGGER.removeHandler(LOG_FILE)
        LOGGER.removeHandler(LOG_STREAM)
        LOG_FILE.close()
        LOG_ENABLED = False


def debug(*args, **kwargs):
    """
    info: log at debug level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        LOGGER.debug(*args, **kwargs)


def info(*args, **kwargs):
    """
    info: log at info level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        LOGGER.info(*args, **kwargs)


def warning(*args, **kwargs):
    """
    info: log at warning level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        LOGGER.warning(*args, **kwargs)


def error(*args, **kwargs):
    """
    info: log at debug level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        LOGGER.error(*args, **kwargs)


def critical(*args, **kwargs):
    """
    info: log at debug level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        LOGGER.critical(*args, **kwargs)
