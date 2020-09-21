# built in libraries
import zlib


def compress(data):
    """
    info: will compress data
    :param data: bytes
    :return: bytes
    """
    return zlib.compress(data)


def decompress(data):
    """
    info: will defcompress data
    :param data: bytes
    :return: bytes
    """
    return zlib.decompress(data)
