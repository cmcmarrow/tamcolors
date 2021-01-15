from tamcolors.tam_io import tam_identifier, tcp_io
from tamcolors.utils import tcp


def run():
    io = tam_identifier.IO
    connection = tcp.TCPConnection()
    tcp_io.run_tcp_connection(connection, io)
