from distutils.core import setup
from Cython.Build import cythonize

setup(name='Pizza Math',
      ext_modules=cythonize("pizzaMath.pyx"))
