from tamcolors.examples import tabletennis
from tamcolors import tam
from tamcolors.utils import tcp
from tamcolors.tam_io import tcp_io


def run():
    import cProfile
    import pstats

    profile = cProfile.Profile()
    with tcp.TCPReceiver() as r:
        io = tcp_io.get_tcp_io(r)
        profile.runcall(tam.tam_loop.TAMLoop(tabletennis.TableTennis(), io=io))
        io.close()

    ps = pstats.Stats(profile)
    ps.print_stats()
