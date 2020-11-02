from tamcolors.examples import tabletennis
from tamcolors import tam
from tamcolors.utils import tcp
from tamcolors.tam_io import tcp_io


def run():
    with tcp.TCPReceiver() as r:
        io = tcp_io.get_tcp_io(r)
        tam.tam_loop.TAMLoop(tabletennis.TableTennis(), io=io).run()
        io.close()
