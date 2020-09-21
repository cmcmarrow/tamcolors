# built in libraries
from functools import wraps

# tamcolors libraries
from tamcolors import tam_io


"""
tam placing finds the x, y coordinates 
"""


def _get_center(spot, length):
    """
    info: gets the center
    :param spot: int
    :param length: int: 0 - inf
    :return: int
    """
    return spot - length//2


def _get_other_side(spot, length):
    """
    info: gets the other side
    :param spot: int
    :param length: int: 0 - inf
    :return: int
    """
    return spot - max(0, length - 1)


def _get_dimensions(func):
    """
    info: is a wrapper
    :param func: function(x, y , width, height)
    :return: function
    """
    @wraps(func)
    def _get_dimensions_wrapper(x, y, width=None, height=None, buffer=None):
        """
        info: will put dimensions as width, height
        :param x: int
        :param y: int
        :param width: int or None
        :param height: int or None
        :param buffer: TAMBuffer
        :return: x, y
        """
        if isinstance(buffer, tam_io.tam_buffer.TAMBuffer):
            width, height = buffer.get_dimensions()

        return func(x, y, width, height)

    return _get_dimensions_wrapper


@_get_dimensions
def top_left(x, y, width, height):
    """
    info: gets the top left x, y
    :param x: int
    :param y: int
    :param width: int: 0 - inf
    :param height: int: 0 - inf
    :return: (int, int)
    """
    return x, y


@_get_dimensions
def top_right(x, y, width, height):
    """
    info: gets the top right x, y
    :param x: int
    :param y: int
    :param width: int: 0 - inf
    :param height: int: 0 - inf
    :return: (int, int)
    """
    return _get_other_side(x, width), y


@_get_dimensions
def bottom_left(x, y, width, height):
    """
    info: gets the bottom left x, y
    :param x: int
    :param y: int
    :param width: int: 0 - inf
    :param height: int: 0 - inf
    :return: (int, int)
    """
    return x, _get_other_side(y, height)


@_get_dimensions
def bottom_right(x, y, width, height):
    """
    info: gets the bottom right x, y
    :param x: int
    :param y: int
    :param width: int: 0 - inf
    :param height: int: 0 - inf
    :return: (int, int)
    """
    return _get_other_side(x, width), _get_other_side(y, height)


@_get_dimensions
def center(x, y, width, height):
    """
    info: gets the center x, y
    :param x: int
    :param y: int
    :param width: int: 0 - inf
    :param height: int: 0 - inf
    :return: (int, int)
    """
    return _get_center(x, width), _get_center(y, height)
