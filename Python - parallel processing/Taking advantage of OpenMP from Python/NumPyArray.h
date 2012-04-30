// DeprecationWarning: PyArray_FromDims: use PyArray_SimpleNew.
// DeprecationWarning: PyArray_FromDimsAndDataAndDescr: use PyArray_NewFromDescr.
//
// july 2009

#ifndef NumPyArray_INCLUDED
#define NumPyArray_INCLUDED

#include <Python.h>              /* Python as seen from C */
#include <numpy/arrayobject.h> /* NumPy  as seen from C */
#include <iostream>

class NumPyArray_Float
{
 private:
  PyArrayObject* a;

 public:
  NumPyArray_Float () { a=NULL; }
  NumPyArray_Float (int n)                                  { create(n); }
  NumPyArray_Float (int n0, int n1)                         { create(n0, n1); }
  NumPyArray_Float (int n0, int n1, int n2)                 { create(n0, n1, n2); }
  NumPyArray_Float (int n0, int n1, int n2, int n3)         { create(n0, n1, n2, n3); }
  NumPyArray_Float (int n0, int n1, int n2, int n3, int n4) { create(n0, n1, n2, n3, n4); }
  NumPyArray_Float (double* data, int n) 
    { wrap(data, n); }
  NumPyArray_Float (double* data, int n0, int n1) 
    { wrap(data, n0, n1); }
  NumPyArray_Float (double* data, int n0, int n1, int n2) 
    { wrap(data, n0, n1, n2); }
  NumPyArray_Float (double* data, int n0, int n1, int n2, int n3) 
    { wrap(data, n0, n1, n2, n3); }
  NumPyArray_Float (double* data, int n0, int n1, int n2, int n3, int n4) 
    { wrap(data, n0, n1, n2, n3, n4); }

  NumPyArray_Float (PyArrayObject* array) { a = array; }
  // NOTE: if we here call wrap(a), a seg.fault appear!
  //NumPyArray_Float (PyArrayObject* array) { wrap(a); }

  // the create functions allocates a new array of doubles
  // with prescribed size
  int create (int n);
  int create (int n0, int n1);
  int create (int n0, int n1, int n2);
  int create (int n0, int n1, int n2, int n3);
  int create (int n0, int n1, int n2, int n3, int n4);

  void deallocate(); // JC march 2008 use A.deallocate() in your code

  // the wrap functions takes an existing array, pointed to by
  // a single double* pointer, and wraps it in a NumPy array

  void wrap (double* data, int n) { 
    int dim1[1]; dim1[0] = n; 
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        1, dim1, PyArray_DOUBLE, (char*) data);
  }

  void wrap (double* data, int n0, int n1) { 
    int dim2[2]; dim2[0] = n0; dim2[1] = n1;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        2, dim2, PyArray_DOUBLE, (char*) data);
  }

  void wrap (double* data, int n0, int n1, int n2) { 
    int dim3[3]; dim3[0] = n0; dim3[1] = n1; dim3[2] = n2;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        3, dim3, PyArray_DOUBLE, (char*) data);
  }

  void wrap (double* data, int n0, int n1, int n2, int n3) { 
    int dim4[4]; dim4[0] = n0; dim4[1] = n1; dim4[2] = n2; dim4[3] = n3;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        4, dim4, PyArray_DOUBLE, (char*) data);
  }

  void wrap (double* data, int n0, int n1, int n2, int n3, int n4) { 
    int dim5[5]; dim5[0] = n0; dim5[1] = n1; dim5[2] = n2; dim5[3] = n3; dim5[4] = n4;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        5, dim5, PyArray_DOUBLE, (char*) data);
  }

  // this wrap function takes a C representation of a NumPy
  // array and wraps in the present C++ class:
  void wrap (PyArrayObject* array) { a = array; }

  int checktype () const;  // are the entries of type double?
  int checkdim  (int expected_ndim) const;
  int checksize (int expected_size0, int expected_size1=0, 
		 int expected_size2=0, int expected_size3=0,
		 int expected_size4=0) const;

  double  operator() (int i) const {
#ifdef INDEX_CHECK
    assert(a->nd == 1 && i >= 0 && i < a->dimensions[0]);
#endif
    return *((double*) (a->data + i*a->strides[0]));
  }
  double& operator() (int i) {
    return *((double*) (a->data + i*a->strides[0]));
  }

  double  operator() (int i, int j) const {
    return *((double*) (a->data + i*a->strides[0] + j*a->strides[1]));
  }
  double& operator() (int i, int j) {
    return *((double*) (a->data + i*a->strides[0] + j*a->strides[1]));
  }

  double  operator() (int i, int j, int k) const {
    return *((double*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2]));
  }
  double& operator() (int i, int j, int k) {
    return *((double*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2]));
  }

  double  operator() (int i, int j, int k, int l) const {
    return *((double*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3]));
  }
  double& operator() (int i, int j, int k, int l) {
    return *((double*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3]));
  }

  double  operator() (int i, int j, int k, int l, int m) const {
    return *((double*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3] + m*a->strides[4]));
  }
  double& operator() (int i, int j, int k, int l, int m) {
    return *((double*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3] + m*a->strides[4]));
  }

  int dim() const { return a->nd; }  // no of dimensions
  int size0() const { return a->dimensions[0]; }
  int size1() const { return a->dimensions[1]; }
  int size2() const { return a->dimensions[2]; }
  int size3() const { return a->dimensions[3]; }
  int size4() const { return a->dimensions[4]; }
  double* getData () { return (double*) a->data; }  // most useful in 1D
  PyArrayObject* getPtr () { return a; }
};

void dump (std::ostream& o, const NumPyArray_Float& a);

// A new class of integer arrays
// Capital letters indicate types as seen in C.
// Python int = 32 bits = 4 bytes
// JC march 2008

class NumPyArray_Int
{
 private:
  PyArrayObject* a;

 public:
  NumPyArray_Int () { a=NULL; }
  NumPyArray_Int (int n)                                  { create(n); }
  NumPyArray_Int (int n0, int n1)                         { create(n0, n1); }
  NumPyArray_Int (int n0, int n1, int n2)                 { create(n0, n1, n2); }
  NumPyArray_Int (int n0, int n1, int n2, int n3)         { create(n0, n1, n2, n3); }
  NumPyArray_Int (int n0, int n1, int n2, int n3, int n4) { create(n0, n1, n2, n3, n4); }
  NumPyArray_Int (int* data, int n) 
    { wrap(data, n); }
  NumPyArray_Int (int* data, int n0, int n1) 
    { wrap(data, n0, n1); }
  NumPyArray_Int (int* data, int n0, int n1, int n2) 
    { wrap(data, n0, n1, n2); }
  NumPyArray_Int (int* data, int n0, int n1, int n2, int n3) 
    { wrap(data, n0, n1, n2, n3); }
  NumPyArray_Int (int* data, int n0, int n1, int n2, int n3, int n4) 
    { wrap(data, n0, n1, n2, n3, n4); }

  NumPyArray_Int (PyArrayObject* array) { a = array; }
  // NOTE: if we here call wrap(a), a seg.fault appear!
  //NumPyArray_Int (PyArrayObject* array) { wrap(a); }

  // the create functions allocates a new array of integers
  // with prescribed size
  int create (int n);
  int create (int n0, int n1);
  int create (int n0, int n1, int n2);
  int create (int n0, int n1, int n2, int n3);
  int create (int n0, int n1, int n2, int n3, int n4);

  void deallocate(); // JC march 2008 use A.deallocate() in your code

  // the wrap functions takes an existing array, pointed to by
  // a single int* pointer, and wraps it in a NumPy array

  void wrap (int* data, int n) { 
    int dim1[1]; dim1[0] = n; 
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        1, dim1, PyArray_INT, (char*) data);
  }

  void wrap (int* data, int n0, int n1) { 
    int dim2[2]; dim2[0] = n0; dim2[1] = n1;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        2, dim2, PyArray_INT, (char*) data);
  }

  void wrap (int* data, int n0, int n1, int n2) { 
    int dim3[3]; dim3[0] = n0; dim3[1] = n1; dim3[2] = n2;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        3, dim3, PyArray_INT, (char*) data);
  }

  void wrap (int* data, int n0, int n1, int n2, int n3) { 
    int dim4[4]; dim4[0] = n0; dim4[1] = n1; dim4[2] = n2; dim4[3] = n3;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        4, dim4, PyArray_INT, (char*) data);
  }

  void wrap (int* data, int n0, int n1, int n2, int n3, int n4) { 
    int dim5[5]; dim5[0] = n0; dim5[1] = n1; dim5[2] = n2; dim5[3] = n3; dim5[4] = n4;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        5, dim5, PyArray_INT, (char*) data);
  }

  // this wrap function takes a C representation of a NumPy
  // array and wraps in the present C++ class:
  void wrap (PyArrayObject* array) { a = array; }

  int checktype () const;  // are the entries of type int?
  int checkdim  (int expected_ndim) const;
  int checksize (int expected_size0, int expected_size1=0, 
		 int expected_size2=0, int expected_size3=0,
		 int expected_size4=0) const;

  int  operator() (int i) const {
#ifdef INDEX_CHECK
    assert(a->nd == 1 && i >= 0 && i < a->dimensions[0]);
#endif
    return *((int*) (a->data + i*a->strides[0]));
  }
  int& operator() (int i) {
    return *((int*) (a->data + i*a->strides[0]));
  }

  int  operator() (int i, int j) const {
    return *((int*) (a->data + i*a->strides[0] + j*a->strides[1]));
  }
  int& operator() (int i, int j) {
    return *((int*) (a->data + i*a->strides[0] + j*a->strides[1]));
  }

  int  operator() (int i, int j, int k) const {
    return *((int*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2]));
  }
  int& operator() (int i, int j, int k) {
    return *((int*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2]));
  }

  int  operator() (int i, int j, int k, int l) const {
    return *((int*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3]));
  }
  int& operator() (int i, int j, int k, int l) {
    return *((int*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3]));
  }

  int  operator() (int i, int j, int k, int l, int m) const {
    return *((int*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3] + m*a->strides[4]));
  }
  int& operator() (int i, int j, int k, int l, int m) {
    return *((int*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3] + m*a->strides[4]));
  }

  int dim() const { return a->nd; }  // no of dimensions
  int size0() const { return a->dimensions[0]; }
  int size1() const { return a->dimensions[1]; }
  int size2() const { return a->dimensions[2]; }
  int size3() const { return a->dimensions[3]; }
  int size4() const { return a->dimensions[4]; }
  int* getData () { return (int*) a->data; }  // most useful in 1D
  PyArrayObject* getPtr () { return a; }
};

void dump (std::ostream& o, const NumPyArray_Int& a);

/*
   A new class of complex arrays
   Capital letters indicate types as seen in C
   Python complex = 16 bytes
   C complex = 16 bytes (2 doubles, 8 bytes each)
   See old_defines.h

   NumPyArray_Float -> NumPyArray_Complex
   PyArray_DOUBLE -> PyArray_CDOUBLE
   double -> npy_cdouble

   npy_cdouble is rather primitive, doesn't have methods
   or overloaded operators. It doesn't make sense to create
   a new class for complex numbers because at the end A(0,0)
   is going to be a plain npy_cdouble.

   JC july 2009
*/

class NumPyArray_Complex
{
 private:
  PyArrayObject* a;

 public:
  NumPyArray_Complex () { a=NULL; }
  NumPyArray_Complex (int n)                                  { create(n); }
  NumPyArray_Complex (int n0, int n1)                         { create(n0, n1); }
  NumPyArray_Complex (int n0, int n1, int n2)                 { create(n0, n1, n2); }
  NumPyArray_Complex (int n0, int n1, int n2, int n3)         { create(n0, n1, n2, n3); }
  NumPyArray_Complex (int n0, int n1, int n2, int n3, int n4) { create(n0, n1, n2, n3, n4); }
  NumPyArray_Complex (npy_cdouble* data, int n) 
    { wrap(data, n); }
  NumPyArray_Complex (npy_cdouble* data, int n0, int n1) 
    { wrap(data, n0, n1); }
  NumPyArray_Complex (npy_cdouble* data, int n0, int n1, int n2) 
    { wrap(data, n0, n1, n2); }
  NumPyArray_Complex (npy_cdouble* data, int n0, int n1, int n2, int n3) 
    { wrap(data, n0, n1, n2, n3); }
  NumPyArray_Complex (npy_cdouble* data, int n0, int n1, int n2, int n3, int n4) 
    { wrap(data, n0, n1, n2, n3, n4); }

  NumPyArray_Complex (PyArrayObject* array) { a = array; }
  // NOTE: if we here call wrap(a), a seg.fault appear!
  //NumPyArray_Complex (PyArrayObject* array) { wrap(a); }

  // the create functions allocates a new array of integers
  // with prescribed size
  int create (int n);
  int create (int n0, int n1);
  int create (int n0, int n1, int n2);
  int create (int n0, int n1, int n2, int n3);
  int create (int n0, int n1, int n2, int n3, int n4);

  void deallocate(); // JC march 2008 use A.deallocate() in your code

  // the wrap functions takes an existing array, pointed to by
  // a single npy_cdouble* pointer, and wraps it in a NumPy array

  void wrap (npy_cdouble* data, int n) { 
    int dim1[1]; dim1[0] = n; 
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        1, dim1, PyArray_CDOUBLE, (char*) data);
  }

  void wrap (npy_cdouble* data, int n0, int n1) { 
    int dim2[2]; dim2[0] = n0; dim2[1] = n1;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        2, dim2, PyArray_CDOUBLE, (char*) data);
  }

  void wrap (npy_cdouble* data, int n0, int n1, int n2) { 
    int dim3[3]; dim3[0] = n0; dim3[1] = n1; dim3[2] = n2;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        3, dim3, PyArray_CDOUBLE, (char*) data);
  }

  void wrap (npy_cdouble* data, int n0, int n1, int n2, int n3) { 
    int dim4[4]; dim4[0] = n0; dim4[1] = n1; dim4[2] = n2; dim4[3] = n3;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        4, dim4, PyArray_CDOUBLE, (char*) data);
  }

  void wrap (npy_cdouble* data, int n0, int n1, int n2, int n3, int n4) { 
    int dim5[5]; dim5[0] = n0; dim5[1] = n1; dim5[2] = n2; dim5[3] = n3; dim5[4] = n4;
    a = (PyArrayObject*) PyArray_FromDimsAndData(
        5, dim5, PyArray_CDOUBLE, (char*) data);
  }

  // this wrap function takes a C representation of a NumPy
  // array and wraps in the present C++ class:
  void wrap (PyArrayObject* array) { a = array; }

  int checktype () const;  // are the entries of type npy_cdouble?
  int checkdim  (int expected_ndim) const;
  int checksize (int expected_size0, int expected_size1=0, 
		 int expected_size2=0, int expected_size3=0,
		 int expected_size4=0) const;

  npy_cdouble  operator() (int i) const {
#ifdef INDEX_CHECK
    assert(a->nd == 1 && i >= 0 && i < a->dimensions[0]);
#endif
    return *((npy_cdouble*) (a->data + i*a->strides[0]));
  }
  npy_cdouble& operator() (int i) {
    return *((npy_cdouble*) (a->data + i*a->strides[0]));
  }

  npy_cdouble  operator() (int i, int j) const {
    return *((npy_cdouble*) (a->data + i*a->strides[0] + j*a->strides[1]));
  }
  npy_cdouble& operator() (int i, int j) {
    return *((npy_cdouble*) (a->data + i*a->strides[0] + j*a->strides[1]));
  }

  npy_cdouble  operator() (int i, int j, int k) const {
    return *((npy_cdouble*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2]));
  }
  npy_cdouble& operator() (int i, int j, int k) {
    return *((npy_cdouble*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2]));
  }

  npy_cdouble  operator() (int i, int j, int k, int l) const {
    return *((npy_cdouble*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3]));
  }
  npy_cdouble& operator() (int i, int j, int k, int l) {
    return *((npy_cdouble*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3]));
  }

  npy_cdouble  operator() (int i, int j, int k, int l, int m) const {
    return *((npy_cdouble*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3] + m*a->strides[4]));
  }
  npy_cdouble& operator() (int i, int j, int k, int l, int m) {
    return *((npy_cdouble*) (a->data + i*a->strides[0] + j*a->strides[1] +
			k*a->strides[2] + l*a->strides[3] + m*a->strides[4]));
  }

  int dim() const { return a->nd; }  // no of dimensions
  int size0() const { return a->dimensions[0]; }
  int size1() const { return a->dimensions[1]; }
  int size2() const { return a->dimensions[2]; }
  int size3() const { return a->dimensions[3]; }
  int size4() const { return a->dimensions[4]; }
  npy_cdouble* getData () { return (npy_cdouble*) a->data; }  // most useful in 1D
  PyArrayObject* getPtr () { return a; }
};

void dump (std::ostream& o, const NumPyArray_Complex& a);

#endif
