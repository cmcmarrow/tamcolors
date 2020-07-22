import setuptools
from distutils.core import setup, Extension
import platform
import os


def get_c_file_path(directory, name):
    return os.path.join("tamcolors", "tam_c", directory, name)


ext_modules = []
if platform.system() == "Windows":
    ext_modules.append(Extension("tamcolors.tam_c._win_tam", sources=[get_c_file_path("_win_tam_c", "_win_tam.cpp"),
                                                                      get_c_file_path("_win_tam_c", "win_tam.cpp")]))
elif platform.system() in ("Darwin", "Linux"):
    ext_modules.append(Extension("tamcolors.tam_c._uni_tam", sources=[get_c_file_path("_uni_tam_c", "_uni_tam.cpp"),
                                                                      get_c_file_path("_uni_tam_c", "uni_tam.cpp")]))

with open(os.path.join("tamcolors", "README.rst")) as readme:
    long_description = readme.read()

setup(
    name="tamcolors",
    version="1.0.2",
    author="Charles McMarrow",
    author_email="Charles.M.McMarrow@gmail.com",
    url="https://github.com/cmcmarrow/tamcolors",
    license="Apache Software License 2.0",
    description="This library standardizes console color output across multiple platforms.",
    description_content_type="text/plain",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["tamcolors",
              "tamcolors.tam",
              "tamcolors.tam_tools",
              "tamcolors.tam_basic",
              "tamcolors.examples",
              "tamcolors.tam_io",
              "tamcolors.tests",
              "tamcolors.tests.tam",
              "tamcolors.tests.tam_tools",
              "tamcolors.tests.tam_io",
              "tamcolors.tam_c",
              "tamcolors.tam_c._win_tam_c",
              "tamcolors.tam_c._uni_tam_c"],

    package_data={"tamcolors": ["LICENSE", "README.rst"],
                  "tamcolors.tam_c._win_tam_c": ["*.cpp", "*.h"],
                  "tamcolors.tam_c._uni_tam_c": ["*.cpp", "*.h"]},

    ext_modules=ext_modules,

    classifiers=["Development Status :: 3 - Alpha",
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
                 "Topic :: Terminals",
                 "Topic :: Utilities"]
)
