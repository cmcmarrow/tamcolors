try:
    from . import _win_tam
except ImportError:
    _win_tam = None

try:
    from . import _uni_tam
except ImportError:
    _uni_tam = None


__all__ = ("_win_tam",
           "_uni_tam")
