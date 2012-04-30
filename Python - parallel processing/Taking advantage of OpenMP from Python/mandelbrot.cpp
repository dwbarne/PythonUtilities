/*
Linux:
$ ./make_module.sh
$ python test_mandelbrot.py

Windows:
$ make_module.bat
$ python test_mandelbrot.py

JC, Santiago, June 2009
*/

#include <math.h>
#include <stdio.h>               /* for debug output */

#include "omp.h"

// Note: keep the parts of the extension module that needs
// the Python or NumPy C API in a single file!
// Therefore we include the class .h and .cpp files here:
#include <NumPyArray.h>
#include <NumPyArray.cpp>

/*
import ext_mandelbrot
import numpy
a = numpy.arange(100)
a.dtype
print ip.sum_of_int(a), sum(a)
*/

int min(int a, int b)
{
if (a<b) return a; else return b;
}

// See numcomplex.h for more functions

inline int cset(npy_cdouble a, npy_cdouble b)
{
a.real = b.real;
a.imag = b.imag;
return 0; 
}

inline npy_cdouble czero(void)
{
npy_cdouble c;
c.real = 0.0;
c.imag = 0.0;
return c; 
}

inline npy_cdouble ci(void)
{
npy_cdouble c;
c.real = 0.0;
c.imag = 1.0;
return c; 
}

inline npy_cdouble cconj(npy_cdouble a)
{
npy_cdouble c;
c.real = c.real;
c.imag = -c.imag;
return c; 
}

inline npy_cdouble cadd(npy_cdouble a, npy_cdouble b)
{
npy_cdouble c;
c.real = a.real+b.real;
c.imag = a.imag+b.imag;
return c; 
}

inline npy_cdouble cadd(double a, npy_cdouble b)
{
npy_cdouble c;
c.real = a+b.real;
c.imag = b.imag;
return c; 
}

inline npy_cdouble csub(npy_cdouble a, npy_cdouble b)
{
npy_cdouble c;
c.real = a.real-b.real;
c.imag = a.imag-b.imag;
return c; 
}

inline npy_cdouble cmul(npy_cdouble a, npy_cdouble b)
{
npy_cdouble c;
c.real = a.real*b.real-a.imag*b.imag;
c.imag = a.real*b.imag+a.imag*b.real;
return c; 
}

inline npy_cdouble cmul(double a, npy_cdouble b)
{
npy_cdouble c;
c.real = a*b.real;
c.imag = a*b.imag;
return c; 
}

inline double cmulconj(npy_cdouble a)
{
return a.real*a.real-a.imag*a.imag;
}

inline npy_cdouble cdiv(npy_cdouble a, npy_cdouble b)
{
npy_cdouble c;
double d = b.real*b.real+b.imag*b.imag;
c.real = (a.real*b.real+a.imag*b.imag)/d;
c.imag = (-a.real*b.imag+a.imag*b.real)/d;
return c; 
}

inline npy_cdouble cdiv(double a, npy_cdouble b)
{
npy_cdouble c;
double d = b.real*b.real+b.imag*b.imag;
c.real = (a*b.real)/d;
c.imag = (-a*b.imag)/d;
return c; 
}

inline npy_cdouble cdiv(npy_cdouble a, double b)
{
npy_cdouble c;
c.real = a.real/b;
c.imag = a.imag/b;
return c; 
}

extern "C" {  // extern "C" is important since this is compiled under C++

static char mandelbrot_doc[] = \
	"Generates Mandelbrot map in the complex plane.\n\
	m = mandelbrot(z)";

static PyObject* mandelbrot(PyObject* self, PyObject* args)
{
	PyArrayObject *z_;
	PyFloatObject *d2_;
	PyIntObject *imax_;
	/* arguments: z */
	if (!PyArg_ParseTuple(args, "O!O!O!:mandelbrot",
		&PyArray_Type, &z_,
		&PyInt_Type, &imax_,
		&PyFloat_Type, &d2_)) {
		return NULL; /* PyArg_ParseTuple has raised an exception */
	}
	NumPyArray_Complex z (z_); 
	if (!z.checktype()) { return NULL; } 
	if (!z.checkdim(2)) { return NULL; }
	int M = z.size0();
	int N = z.size1();

	double d2;
	d2 = PyFloat_AS_DOUBLE(d2_);
	long imax;
	imax = PyInt_AS_LONG(imax_);

	NumPyArray_Int out(M,N);

	npy_cdouble zo,zn,c;

	int i,m,n;

	#pragma omp parallel for shared(z,out,M,N,d2,imax) private(i,m,n,zo,zn,c)
	for(m=0; m<M; m++) {
		for(n=0; n<N;n++){

			//if ((n==0)&&(m==0)) printf("%f+%fj, ",z(m,n).real,z(m,n).imag);
			//cset(c,z(m,n));
			//c = z(m,n);
			c.real = z(m,n).real; c.imag = z(m,n).imag; 
			//if ((n==0)&&(m==0)) printf("%f+%fj, ",c.real,c.imag);

			zo = czero();
			zn = czero();
			i = 0;
			while ((cmulconj(zn)<d2) && (i<imax)) {
				zn = cadd(c,cmul(zo,zo));
				//cset(zn,cadd(c,cmul(zo,zo)));
				//cset(zo,zn); // zo = zn;
				zo.real = zn.real; zo.imag = zn.imag;
				i++;
			}
			out(m,n) = i;
		}
	}

	return PyArray_Return(out.getPtr());
}

/* doc string of the module: */
static char module_doc[] = \
	"m = mandelbrot(z)";

/* 
   The method table must always be present - it lists the 
   functions that should be callable from Python: 
*/
static PyMethodDef ext_mandelbrot_methods[] = {
	{"mandelbrot",    /* name of func when called from Python */
	mandelbrot,      /* corresponding C function */
	METH_VARARGS,   /* ordinary (not keyword) arguments */
	mandelbrot_doc}, /* doc string for function */
	{NULL, NULL}     /* required ending of the method table */
};

PyMODINIT_FUNC initext_mandelbrot()
{
	/* Assign the name of the module and the name of the
	method table and (optionally) a module doc string:
	*/
	Py_InitModule3("ext_mandelbrot", ext_mandelbrot_methods, module_doc);
	/* without module doc string: 
	Py_InitModule ("ext_mandelbrot", ext_mandelbrot_methods); */

	import_array();   /* required NumPy initialization */
}

} // end extern "C"
