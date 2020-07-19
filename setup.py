from distutils.core import setup, Extension
import platform
import os


def get_c_file_path(directory, name):
    return os.path.join("tamcolors", "tam_c", directory, name)


ext_modules = []
if platform.system() == "Windows":
    ext_modules.append(Extension("tamcolors.tam_io._win_tam", sources=[get_c_file_path("_win_tam", "_win_tam.cpp"),
                                                                       get_c_file_path("_win_tam", "win_tam.cpp")]))
elif platform.system() in ("Darwin", "Linux"):
    ext_modules.append(Extension("tamcolors.tam_io._uni_tam", sources=[get_c_file_path("_uni_tam", "_uni_tam.cpp"),
                                                                       get_c_file_path("_uni_tam", "uni_tam.cpp")]))


setup(
    name="tamcolors",
    version="1.0.0",
    author="Charles McMarrow",
    author_email="Charles.M.McMarrow@gmail.com",
    license="Apache Software License 2.0",

    packages=["tamcolors",
              "tamcolors.tam",
              "tamcolors.tam_tools",
              "tamcolors.tam_basic",
              "tamcolors.examples",
              "tamcolors.tests",
              "tamcolors.tests.tam",
              "tamcolors.tests.tam_tools"],

    ext_modules=ext_modules,

    classifiers=["Development Status :: 5 - Production/Stable",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Natural Language :: English",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: POSIX :: Linux",
                 "Operating System :: MacOS :: MacOS X",
                 "Programming Language :: C",
                 "Programming Language :: C++",
                 "Programming Language :: Python :: Implementation :: CPython",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Topic :: Terminals",
                 "Topic :: Utilities"]
)
