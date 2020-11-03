from tamcolors.tam_io import tam_identifier, tam_colors, tam_buffer
from tamcolors.utils import tcp
from tamcolors.utils import object_packer


def run():
    io = tam_identifier.IO
    connection = tcp.TCPConnection()
    try:
        tcp.TCPObjectWrapper(connection, io, object_packer.ObjectPackerJson((tam_colors.RGBA,
                                                                                      tam_colors.Color,
                                                                                      tam_buffer.TAMBuffer)))()
    except tcp.TCPError:
        pass
