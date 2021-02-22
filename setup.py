import setuptools
from distutils.core import setup, Extension
import platform
import os


def get_c_file_path(directory, name):
    return os.path.join("tamcolors", "tam_c", directory, name)


ext_modules = []
if platform.system() == "Windows":
    ext_modules.append(Extension("tamcolors.tam_c._win_tam",
                                 sources=[get_c_file_path("_win_tam_c", "_win_tam.cpp"),
                                          get_c_file_path("_win_tam_c", "win_tam.cpp")]))
elif platform.system() in ("Darwin", "Linux"):
    libraries = []
    if platform.system() == "Linux":
        libraries.append("X11")
    ext_modules.append(Extension("tamcolors.tam_c._uni_tam",
                                 sources=[get_c_file_path("_uni_tam_c", "_uni_tam.cpp"),
                                          get_c_file_path("_uni_tam_c", "uni_tam.cpp")],
                                 libraries=libraries))

with open(os.path.join("README.rst")) as readme:
    long_description = readme.read()

setup(
    name="tamcolors",
    version="2.0.0",
    author="Charles McMarrow",
    author_email="Charles.M.McMarrow@gmail.com",
    url="https://github.com/cmcmarrow/tamcolors",
    license="Apache Software License 2.0",
    description="tamcolors is a terminal game library which supports multiplayer and audio.",
    description_content_type="text/plain",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["tamcolors",
              "tamcolors.tam",
              "tamcolors.tam_tools",
              "tamcolors.tam_basic",
              "tamcolors.examples",
              "tamcolors.tam_io",
              "tamcolors.utils",
              "tamcolors.tests",
              "tamcolors.tests.tam_tests",
              "tamcolors.tests.tam_tools_tests",
              "tamcolors.tests.tam_io_tests",
              "tamcolors.tests.tam_basic_tests",
              "tamcolors.tests.utils_tests",
              "tamcolors.tests.tests_tests",
              "tamcolors.tam_c",
              "tamcolors.tam_c._win_tam_c",
              "tamcolors.tam_c._win_tam_c.vs140_dlls",
              "tamcolors.tam_c._win_tam_c.vs140_dlls.arm",
              "tamcolors.tam_c._win_tam_c.vs140_dlls.x64",
              "tamcolors.tam_c._win_tam_c.vs140_dlls.x86",
              "tamcolors.tam_c._uni_tam_c"],

    package_data={"tamcolors.tam_c._win_tam_c": ["*.cpp", "*.h"],
                  "tamcolors.tam_c._uni_tam_c": ["*.cpp", "*.h"],
                  "tamcolors.tam_c._win_tam_c.vs140_dlls.arm": ["*.dll"],
                  "tamcolors.tam_c._win_tam_c.vs140_dlls.x64": ["*.dll"],
                  "tamcolors.tam_c._win_tam_c.vs140_dlls.x86": ["*.dll"]},

    extras_require={"dev": ["wheel", "check-manifest", "twine", "sphinx", "sphinx-rtd-theme", "cryptography"],
                    "encryption": ["cryptography"]},

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
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Topic :: Terminals",
                 "Topic :: Utilities"]
)
