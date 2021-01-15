from random import randint
from tamcolors.utils.tcp import TCPConnection
from tamcolors.tam_io.tcp_io import run_tcp_connection


def run():
    run_tcp_connection(TCPConnection(user_name=str(randint(0, 1000000000000000000))))
