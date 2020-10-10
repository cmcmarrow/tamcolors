from os import getcwd
from os.path import join
import logging


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


def enable_logging(level=DEBUG):
    """
    info: will enable logging at a level
    :param level: log level
    :return:
    """
    global LOG_ENABLED
    if LOG_ENABLED:
        disable_logging()
    LOG_ENABLED = True
    logging.basicConfig(filename=LOG_FILE_NAME,
                        filemode="w",
                        format="[%(asctime)s][%(process)d %(processName)s][%(thread)d %(threadName)s][%(levelname)s] %(message)s")
    logging.getLogger().setLevel(level)


def disable_logging():
    """
    info: will disable logging
    :return:
    """
    global LOG_ENABLED
    if LOG_ENABLED:
        logging.shutdown()
        LOG_ENABLED = False


def debug(*args, **kwargs):
    """
    info: log at debug level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        logging.debug(*args, **kwargs)


def info(*args, **kwargs):
    """
    info: log at info level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        logging.info(*args, **kwargs)


def warning(*args, **kwargs):
    """
    info: log at warning level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        logging.warning(*args, **kwargs)


def error(*args, **kwargs):
    """
    info: log at debug level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        logging.error(*args, **kwargs)


def critical(*args, **kwargs):
    """
    info: log at debug level
    :param args: tuple
    :param kwargs: dict
    :return:
    """
    if LOG_ENABLED:
        logging.critical(*args, **kwargs)
