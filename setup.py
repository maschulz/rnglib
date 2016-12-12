from distutils.core import setup, Extension

from Cython.Build import cythonize

setup(
    name='rnglib',
    version='0.1.0',
    author='Marc-Andre Schulz',
    author_email='marc.schulz@rwth-aachen.de',
    description='Tools for analyzing human-generated random number sequences',
    packages=['rnglib'],
    ext_modules=cythonize(Extension('rnglib.dlscore', ["rnglib/dlscore.pyx"]), ),
    requires=['numpy', 'cython']
)
