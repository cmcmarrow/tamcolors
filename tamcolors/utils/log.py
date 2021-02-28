from os import getcwd
from os.path import join
import logging
from logging import handlers
from datetime import datetime
import threading
import multiprocessing
from functools import wraps


"""
Enable and Disable a log file for tamcolors 
"""


LOG_FILE_NAME = join(getcwd(), "tamcolors.log")
LOGGER = logging.getLogger("tamcolors")
LOG_FORMATTER = logging.Formatter("%(message)s")
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

LOG_ENABLED = False
LOG_FILE = None
LOG = None


class Log:
    def __init__(self, size=5000):
        self._size = size
        self._log = {}
        self._lock = threading.Lock()
        self._last = -1
        self._first = -1

    def __call__(self, msg):
        try:
            self._lock.acquire()
            self._log[self._first + 1] = msg
            self._first += 1
            if len(self._log) > self._size or self._last == -1:
                if self._last in self._log:
                    del self._log[self._last]
                self._last += 1
        finally:
            self._lock.release()

    def log(self, msg):
        self(msg)

    def read(self, log_id):
        return self._log.get(log_id, "")

    def last_msg_id(self):
        return self._last

    def first_msg_id(self):
        return self._first


def format_message(func):
    @wraps(func)
    def _format_message(msg):
        return func("[{}][{} {}][{} {}][{}] {}".format(datetime.now().strftime("%H:%M:%S"),
                                                       threading.currentThread().ident,
                                                       threading.currentThread().name,
                                                       multiprocessing.current_process().ident,
                                                       multiprocessing.current_process().name,
                                                       func.__name__.upper(),
                                                       msg))
    return _format_message


def enable_logging(level=DEBUG):
    """
    info: will enable logging at a level
    :param level: log level
    :return:
    """
    global LOG_ENABLED, LOG_FILE, LOG
    if LOG_ENABLED:
        disable_logging()
    LOG_ENABLED = True
    LOG_FILE = handlers.RotatingFileHandler(LOG_FILE_NAME,  maxBytes=5000000, encoding="utf-8")
    LOG_FILE.setFormatter(LOG_FORMATTER)
    LOG = Log()
    LOGGER.addHandler(LOG_FILE)
    LOGGER.setLevel(level)


def disable_logging():
    """
    info: will disable logging
    :return:
    """
    global LOG_ENABLED, LOG_FILE, LOG
    if LOG_ENABLED:
        LOGGER.removeHandler(LOG_FILE)
        LOG_FILE.close()
        LOG_ENABLED = False
        LOG_FILE = None
        LOG = None


@format_message
def debug(msg):
    """
    info: log at debug level
    :param msg: str
    :return:
    """
    if LOG_ENABLED and LOGGER.level <= DEBUG:
        LOGGER.debug(msg)
        LOG(msg)


@format_message
def info(msg):
    """
    info: log at info level
    :param msg: str
    :return:
    """
    if LOG_ENABLED and LOGGER.level <= INFO:
        LOGGER.info(msg)
        LOG(msg)


@format_message
def warning(msg):
    """
    info: log at warning level
    :param msg: str
    :return:
    """
    if LOG_ENABLED and LOGGER.level <= WARNING:
        LOGGER.warning(msg)
        LOG(msg)


@format_message
def error(msg):
    """
    info: log at debug level
    :param msg: str
    :return:
    """
    if LOG_ENABLED and LOGGER.level <= ERROR:
        LOGGER.error(msg)
        LOG(msg)


@format_message
def critical(msg):
    """
    info: log at critical level
    :param msg: str
    :return:
    """
    if LOG_ENABLED and LOGGER.level <= CRITICAL:
        LOGGER.critical(msg)
        LOG(msg)
