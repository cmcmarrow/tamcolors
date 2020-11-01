from . import tam_colors, tam_buffer
from tamcolors.utils import tcp, object_packer


def get_tcp_io(receiver):
    """
    info: will return TCPObjectConnector connected to an io object
    :param receiver: TCPReceiver
    :return: TCPObjectConnector
    """
    connection = receiver.get_host_connection()
    return tcp.TCPObjectConnector(connection,
                                  object_packer=object_packer.ObjectPackerJson((tam_colors.RGBA,
                                                                                tam_colors.Color,
                                                                                tam_buffer.TAMBuffer)),
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
