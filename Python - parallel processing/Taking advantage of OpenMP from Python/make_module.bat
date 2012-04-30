python setup.py build --compiler=mingw32
copy build\lib.win32-2.4\ext_mandelbrot.pyd
python -c "import ext_mandelbrot; print dir(ext_mandelbrot)"

