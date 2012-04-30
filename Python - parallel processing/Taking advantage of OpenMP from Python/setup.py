import os
from distutils.core import setup, Extension
name = 'ext_mandelbrot'
setup(name=name,
      ext_modules=[Extension(name,
                             sources=['mandelbrot.cpp'],
                             include_dirs=[os.curdir])])
