import distutils.core

_win_tma_module = distutils.core.Extension("_win_tma", sources=["_win_tma.cpp", "win_tma.cpp"])

distutils.core.setup(name="_win_tma",
                     version="1.0.0",
                     description="Can work with Windows terminal.",
                     ext_modules=[_win_tma_module])
