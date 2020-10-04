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
    info: enable logging
    :level: log level
    :return: None
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
    info: disable logging
    :return: None
    """
    global LOG_ENABLED
    if LOG_ENABLED:
        logging.shutdown()
        LOG_ENABLED = False


def debug(*args, **kwargs):
    """
    info: logs as debug
    :param args: *args
    :param kwargs: **kwargs
    :return: None
    """
    if LOG_ENABLED:
        logging.debug(*args, **kwargs)


def info(*args, **kwargs):
    """
    info: logs as info
    :param args: *args
    :param kwargs: **kwargs
    :return: None
    """
    if LOG_ENABLED:
        logging.info(*args, **kwargs)


def warning(*args, **kwargs):
    """
    info: logs as warning
    :param args: *args
    :param kwargs: **kwargs
    :return: None
    """
    if LOG_ENABLED:
        logging.warning(*args, **kwargs)


def error(*args, **kwargs):
    """
    info: logs as error
    :param args: *args
    :param kwargs: **kwargs
    :return: None
    """
    if LOG_ENABLED:
        logging.error(*args, **kwargs)


def critical(*args, **kwargs):
    """
    info: logs as critical
    :param args: *args
    :param kwargs: **kwargs
    :return: None
    """
    if LOG_ENABLED:
        logging.critical(*args, **kwargs)
