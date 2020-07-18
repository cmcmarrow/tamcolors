import distutils.core

_uni_tma_module = distutils.core.Extension("_uni_tma", sources=["_uni_tma.cpp", "uni_tma.cpp"])

distutils.core.setup(name="_uni_tma",
                     version="1.0.0",
                     description="Can work with Unix terminal.",
                     ext_modules=[_uni_tma_module])
