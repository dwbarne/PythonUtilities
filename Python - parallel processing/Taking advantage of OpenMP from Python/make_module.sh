#!/bin/sh -x
rm -f *.o *.so
root=`python -c 'import sys; print sys.prefix'`
ver=`python -c 'import sys; print sys.version[:3]'`
g++ -O3 -g -fopenmp -I. -I$root/include/python$ver -I$root/lib/python$ver/site-packages/numpy/core/include -c mandelbrot.cpp
g++ -shared -lgomp -o ext_mandelbrot.so mandelbrot.o

# test the module:
python -c 'import ext_mandelbrot; print dir(ext_mandelbrot)'
           
