# built in libraries
import unittest
from threading import Thread

# tamcolors libraries
from tamcolors.utils import tcp
from tamcolors.tests.test_utils import slow_test


class TCPTest(unittest.TestCase):
    @slow_test
    def test_echo(self):
        def _connection():
            con = tcp.TCPConnection("127.0.0.1", 4444)
            con.send_data(con.get_data())

        self._run_other_box(_connection)

        receiver = tcp.TCPReceiver()
        receiver.start("127.0.0.1", 4444)
        c = receiver.get_connection("127.0.0.1", 4444, wait=True)
        host = tcp.TCPHost(*c)
        echo = b"echo"
        host.send_data(echo)
        self.assertEqual(host.get_data(), echo)

    @staticmethod
    def _run_other_box(func, *args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
