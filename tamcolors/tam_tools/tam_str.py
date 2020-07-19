# built in libraries
import string

"""
formats strings into strings that tam can use safely  
"""


class TAMStrError(Exception):
    pass


def make_tam_str(text, end_line="\n", bad_char=None):
    """
    info: formats str into a tam str
    :param text: str
    :param end_line: str
    :param bad_char: str
    :return: str
    """
    tam_str = []
    for char in str(text):
        if char == "\n":
            tam_str.append(end_line)
        elif char == "\t":
            for i in range(4):
                tam_str.append(" ")
        elif char in string.whitespace and char != " ":
            if bad_char is None:
                raise TAMStrError("{0} is a bad char".format(repr(char)))
            tam_str.append(bad_char)
        else:
            tam_str.append(char)

    return "".join(tam_str)
