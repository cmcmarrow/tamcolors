from . import tam_colors, tam_surface, tam_identifier
from tamcolors.utils import tcp, object_packer, log


def get_tcp_io(receiver, wait=True):
    """
    info: will return TCPObjectConnector connected to an io object
    :param receiver: TCPReceiver
    :param wait: bool
    :return: TCPObjectConnector
    """
    connection = receiver.get_host_connection(wait)
    if connection is not None:
        return tcp.TCPObjectConnector(connection,
                                      object_packer=object_packer.ObjectPackerJson((tam_colors.RGBA,
                                                                                    tam_colors.Color,
                                                                                    tam_surface.TAMSurface)),
                                      no_return={"set_mode",
                                                 "draw",
                                                 "start",
                                                 "done",
                                                 "printc",
                                                 "clear",
                                                 "show_console_cursor",
                                                 "set_color_2",
                                                 "set_color_16_pal_256",
                                                 "set_color_16",
                                                 "set_color_256",
                                                 "reset_colors_to_console_defaults",
                                                 "set_tam_color_defaults",
                                                 "enable_console_keys"},
                                      optimizer={"draw",
                                                 "get_dimensions",
                                                 "get_key_dict",
                                                 "get_info_dict"})


def run_tcp_connection(connection, io=None):
    """
    info: will run a tcp connection
    :param connection: TCPConnection
    :param io: IO or None: None will uses default IO
    :return: None
    """
    if io is None:
        io = tam_identifier.IO
    try:
        tcp.TCPObjectWrapper(connection, io, object_packer.ObjectPackerJson((tam_colors.RGBA,
                                                                             tam_colors.Color,
                                                                             tam_surface.TAMSurface)))()
    except tcp.TCPError as error:
        log.warning("run_tcp_connection error: {}".format(error))
    finally:
        io.done()
