from . import tam_loop_receiver
from tamcolors.utils import tcp
from tamcolors.tam_io import tcp_io


class TAMLoopTCPReceiver(tam_loop_receiver.TAMLoopReceiver):
    def __init__(self,
                 host="127.0.0.1",
                 port=4444,
                 ipv6=False,
                 listen_count=10,
                 connection_password="",
                 address_white_list=None,
                 address_black_list=None,
                 encryption=None,
                 object_packer=None,
                 our_information=None):

        self._receiver = tcp.TCPReceiver(host=host,
                                         port=port,
                                         ipv6=ipv6,
                                         listen_count=listen_count,
                                         connection_password=connection_password,
                                         address_white_list=address_white_list,
                                         address_black_list=address_black_list,
                                         encryption=encryption,
                                         object_packer=object_packer,
                                         our_information=our_information)
        super().__init__("{}@{}".format(host, port))

    def get_handler(self):
        """
        info: Will get an io if available
        :return: TAMLoopIOHandler or None
        """
        return tcp_io.get_tcp_io(self._receiver, False)    # TODO write

    def done(self):
        """
        info: Will stop the receiver
        :return: None
        """
        super().done()
        self._receiver.close()
