from distutils.core import setup, Extension

from Cython.Build import cythonize

setup(
    ext_modules=cythonize(Extension('rnglib.dlscore', ["rnglib/dlscore.pyx"]), )
)
