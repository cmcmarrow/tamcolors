# built in libraries
import unittest.mock
import time
import os

# tamcolors libraries
from tamcolors.utils import tcp
from tamcolors.tests.test_multi_task_helper import MultiTaskHelper
from tamcolors.tests.test_utils import slow_test


def _test_ping_host():
    with tcp.TCPReceiver() as receiver:
        host = receiver.get_host_connection()
        host.send_data(b"ping receiver")
        assert host.get_data() == b"ping host"
        host.close()
        receiver.close()


def _test_ping_connection():
    # wait for host to start
    time.sleep(5)
    connection = tcp.TCPConnection()
    assert connection.get_data() == b"ping receiver"
    connection.send_data(b"ping host")
    connection.close()


def _test_ping_host_ipv6():
    with tcp.TCPReceiver(host="::1", ipv6=True) as receiver:
        host = receiver.get_host_connection()
        host.send_data(b"ping receiver")
        assert host.get_data() == b"ping host"
        host.close()
        receiver.close()


def _test_ping_connection_ipv6():
    # wait for host to start
    time.sleep(5)
    connection = tcp.TCPConnection(host="::1", ipv6=True)
    assert connection.get_data() == b"ping receiver"
    connection.send_data(b"ping host")
    connection.close()


@unittest.skipIf(os.environ["TRAVIS"] == "true", "tests cant run in Travis CI.")
class TCPTests(MultiTaskHelper, unittest.TestCase):
    @slow_test
    def test_ping(self):
        self.multiple_processes_helper([self.task(_test_ping_host),
                                        self.task(_test_ping_connection)])

    @slow_test
    def test_ping_ipv6(self):
        self.multiple_processes_helper([self.task(_test_ping_host_ipv6),
                                        self.task(_test_ping_connection_ipv6)])
