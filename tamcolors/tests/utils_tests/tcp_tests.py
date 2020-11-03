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


def _test_ping_connection_ipv6():
    # wait for host to start
    time.sleep(5)
    connection = tcp.TCPConnection(host="::1", ipv6=True)
    assert connection.get_data() == b"ping receiver"
    connection.send_data(b"ping host")
    connection.close()


@unittest.skipIf(os.environ.get("TRAVIS") == "true", "tests cant run in Travis CI.")
class TCPTests(MultiTaskHelper, unittest.TestCase):
    @slow_test
    def test_ping(self):
        self.multiple_processes_helper([self.task(_test_ping_host),
                                        self.task(_test_ping_connection)])

    @slow_test
    def test_ping_ipv6(self):
        self.multiple_processes_helper([self.task(_test_ping_host_ipv6),
                                        self.task(_test_ping_connection_ipv6)])


def _test_object_host():
    with tcp.TCPReceiver() as r:
        host = r.get_host_connection()
        obj_con = tcp.TCPObjectConnector(host, no_return={"echo"}, optimizer={"ping"})
        assert obj_con.add(3, 5) == 8
        assert obj_con.add(3, -5) == -2

        for i in range(1, 10):
            assert obj_con.step() == i

        assert obj_con.ping("cats", "dogs", sum=44) == "ping ('cats', 'dogs') {'sum': 44}"
        assert obj_con.ping("cats", "dogs", sum=44) == "ping ('cats', 'dogs') {'sum': 44}"
        assert obj_con.ping("cats", "dogs", sum=-234) == "ping ('cats', 'dogs') {'sum': -234}"

        assert obj_con.ran_echo() is False
        assert obj_con.echo() is None
        assert obj_con.ran_echo() is True
        host.close()


def _test_object_connection():
    class Dummy:
        def __init__(self):
            self._i = 0
            self._echo = False

        @staticmethod
        def ping(*args, **kwargs):
            return "ping {} {}".format(args, kwargs)

        @staticmethod
        def add(a, b):
            return a + b

        def step(self):
            self._i += 1
            return self._i

        def echo(self):
            self._echo = True
            return "echo"

        def ran_echo(self):
            return self._echo

    time.sleep(5)
    try:
        connection = tcp.TCPConnection()
        tcp.TCPObjectWrapper(connection, Dummy())()
    except tcp.TCPError:
        pass


@unittest.skipIf(os.environ.get("TRAVIS") == "true", "tests cant run in Travis CI.")
class TCPObjectWrapper(MultiTaskHelper, unittest.TestCase):
    @slow_test
    def test_object_wrapper(self):
        self.multiple_processes_helper([self.task(_test_object_host),
                                        self.task(_test_object_connection)])
