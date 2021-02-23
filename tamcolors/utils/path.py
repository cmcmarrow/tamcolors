from os import path
from inspect import stack


def abspath(*file):
    """
    info: gets the abspath for the file in the same directory from the call
    :param file: str
    :return: str
    """
    file_path = path.dirname(stack()[1].filename)

    return path.join(file_path, *file)
