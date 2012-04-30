root = /usr
ver = 2.6

#root=`python -c 'import sys; print sys.prefix'`
#ver=`python -c 'import sys; print sys.version[:3]'`

ext_mandelbrot.so : mandelbrot.o
	g++ -shared -o ext_mandelbrot.so mandelbrot.o
	python -c 'import ext_mandelbrot; print dir(ext_mandelbrot)'

mandelbrot.o : mandelbrot.cpp linear_algebra.cpp NumPyArray.cpp
	g++ -O3 -g -I. -I$(root)/include/python$(ver) -I$(root)/lib/python$(ver)/site-packages/numpy/core/include -c mandelbrot.cpp

test :
	python test_mandelbrot.py > test.log

clean :
	rm -f *.o *.so core *~

realclean : clean
	rm -f ext_mandelbrot.so

	
