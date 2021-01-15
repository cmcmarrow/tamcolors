# built in libraries
import unittest.mock
import time
import os

# tamcolors libraries
from tamcolors.tam_io import tam_colors
from tamcolors.tam_io.tam_identifier import NULL
from tamcolors.tam_io import tcp_io
from tamcolors.utils import tcp
from tamcolors.tam import tam_loop_tcp_receiver
from tamcolors.tests.test_multi_task_helper import MultiTaskHelper
from tamcolors.tests.test_utils import slow_test


def _test_tcp_receiver_host():
    io_handler = None
    receiver = None
    try:
        receiver = tam_loop_tcp_receiver.TAMLoopTCPReceiver()
        time.sleep(10)
        io_handler = receiver.get_handler()
        io_handler.run()
        for c in range(16):
            assert io_handler.get_color_16(c) == tam_colors.COLORS[c].mode_rgb
    finally:
        if io_handler is not None:
            io_handler.done()
        if receiver is not None:
            receiver.done()


def _test_null_connection():
    time.sleep(5)
    connection = tcp.TCPConnection()
    tcp_io.run_tcp_connection(connection, NULL)


@unittest.skipIf(os.environ.get("TRAVIS") == "true", "tests cant run in Travis CI.")
class TAMLoopTCPReceiver(MultiTaskHelper, unittest.TestCase):
    @slow_test
    def test_loop_tcp_receiver(self):
        self.multiple_processes_helper([self.task(_test_tcp_receiver_host), self.task(_test_null_connection)])
