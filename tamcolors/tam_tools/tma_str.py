# built in libraries
import string

"""
formats strings into strings that tam can use safely  
"""


class TMAStrError(Exception):
    pass


def make_tma_str(text, end_line="\n", bad_char=None):
    """
    info: formats str into a tam str
    :param text: str
    :param end_line: str
    :param bad_char: str
    :return: str
    """
    tma_str = []
    for char in str(text):
        if char == "\n":
            tma_str.append(end_line)
        elif char == "\t":
            for i in range(4):
                tma_str.append(" ")
        elif char in string.whitespace and char != " ":
            if bad_char is None:
                raise TMAStrError("{0} is a bad char".format(repr(char)))
            tma_str.append(bad_char)
        else:
            tma_str.append(char)

    return "".join(tma_str)
