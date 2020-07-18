# built in libraries
import string

# tamcolors libraries
from tamcolors import checks


# Charles McMarrow

"""
formats strings into strings that tma can use safely  
"""


class TMAStrError(Exception):
    pass


def make_tma_str(text, end_line="\n", bad_char=None):
    """
    info: formats str into a tma str
    :param text: str
    :param end_line: str
    :param bad_char: str
    :return: str
    """
    checks.checks.has_method_check(text, "__str__", TMAStrError)
    checks.checks.instance_check(end_line, str, TMAStrError)
    if bad_char is not None:
        checks.checks.instance_check(bad_char, str, TMAStrError)
        for char in bad_char:
            checks.checks.single_block_char_check(char, TypeError)

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
