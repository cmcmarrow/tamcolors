import platform
import sys
import os

WIN_VS_DLL_PATH = None
# get VS dlls path
if sys.platform == "win32":
    if platform.architecture()[0] == "32bit":
        WIN_VS_DLL_PATH = os.path.join(__path__[0], "vs_dlls", "x86")
    elif platform.architecture()[0] == "64bit":
        WIN_VS_DLL_PATH = os.path.join(__path__[0], "vs_dlls", "x64")
    else:
        WIN_VS_DLL_PATH = os.path.join(__path__[0], "vs_dlls", "arm")

try:
    # add VS dlls to python path
    if isinstance(WIN_VS_DLL_PATH, str):
        sys.path.append(WIN_VS_DLL_PATH)
    from . import _win_tam
except ImportError:
    _win_tam = None
finally:
    # remove VS dlls from path
    if isinstance(WIN_VS_DLL_PATH, str):
        try:
            sys.path.remove(WIN_VS_DLL_PATH)
        except ValueError:
            pass

try:
    from . import _uni_tam
except ImportError:
    _uni_tam = None


__all__ = ("_win_tam",
           "_uni_tam")
