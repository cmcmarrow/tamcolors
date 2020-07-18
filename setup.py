from distutils.core import setup, Extension
import platform
import os


ext_modules = []
if platform.system() == "Windows":
    ext_modules.append(Extension("tamcolors.tam._win_tma", sources=[os.path.join("tamcolors", "tam", "_win_tma", "_win_tma.cpp"),
                                                                    os.path.join("tamcolors", "tam", "_win_tma", "win_tma.cpp")]))
elif platform.system() in ("Darwin", "Linux"):
    ext_modules.append(Extension("tamcolors.tam._uni_tma", sources=[os.path.join("tamcolors", "tam", "_uni_tma", "_uni_tma.cpp"),
                                                                    os.path.join("tamcolors", "tam", "_uni_tma", "uni_tma.cpp")]))


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
              "tamcolors.checks",
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
