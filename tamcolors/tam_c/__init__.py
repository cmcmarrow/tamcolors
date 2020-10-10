import platform
import os
import shutil

WIN_VS_DLL_PATH = None
# get VS dlls path
if platform.system() == "Windows":
    if platform.architecture()[0] == "32bit":
        WIN_VS_DLL_PATH = os.path.join(__path__[0], "_win_tam_c", "vs_dlls", "x86")
    elif platform.architecture()[0] == "64bit":
        WIN_VS_DLL_PATH = os.path.join(__path__[0], "_win_tam_c", "vs_dlls", "x64")
    else:
        WIN_VS_DLL_PATH = os.path.join(__path__[0], "_win_tam_c", "vs_dlls", "arm")

try:
    try:
        from . import _win_tam
    except ImportError:
        # move over missing dlls and try again
        if WIN_VS_DLL_PATH is not None:
            for _, _, files in os.walk(WIN_VS_DLL_PATH):
                for file in files:
                    from_path = os.path.join(WIN_VS_DLL_PATH, file)
                    to_path = os.path.join(__path__[0], file)
                    if not os.path.exists(to_path):
                        shutil.copy2(from_path, to_path)
        from . import _win_tam
except ImportError:
    _win_tam = None

try:
    from . import _uni_tam
except ImportError:
    _uni_tam = None


__all__ = ("_win_tam",
           "_uni_tam")
