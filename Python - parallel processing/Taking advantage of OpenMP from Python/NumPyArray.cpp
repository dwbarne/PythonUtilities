#include <NumPyArray.h>

int NumPyArray_Float:: checktype () const
{
  if (a->descr->type_num != PyArray_DOUBLE) {
    PyErr_Format(PyExc_ValueError,
		 "a is not of type 'Float'");
    return 0;
  }
  return 1;
}

int NumPyArray_Float:: checkdim (int expected_ndim) const
{
  if (a->nd != expected_ndim) {
    PyErr_Format(PyExc_ValueError,
		 "NumPy array is %d-dimensional; expected %d dimensions", 
		 a->nd, expected_ndim);
    return 0;
  } 
  return 1;
}

int NumPyArray_Float:: checksize (int expected_size0, 
				  int expected_size1, 
				  int expected_size2,
				  int expected_size3,
				  int expected_size4) const
{
  if (a->dimensions[0] != expected_size0) {
    PyErr_Format(PyExc_ValueError,
		 "NumPy array's 1st index runs from 0 to %d (expected %d)", 
		 a->dimensions[0], expected_size0);
    return 0;
  }
  if (expected_size1 > 0) {
    if (a->dimensions[1] != expected_size1) {
	PyErr_Format(PyExc_ValueError,
		     "NumPy array's 2nd index runs from 0 to %d (expected %d)", 
		     a->dimensions[1], expected_size1);
	return 0;
    }
    if (expected_size2 > 0) {
      if (a->dimensions[2] != expected_size2) {
	PyErr_Format(PyExc_ValueError,
		     "NumPy array's 3rd index runs from 0 to %d (expected %d)", 
		     a->dimensions[2], expected_size2);
	return 0;
      }
      if (expected_size3 > 0) {
        if (a->dimensions[3] != expected_size3) {
	  PyErr_Format(PyExc_ValueError,
		     "NumPy array's 4th index runs from 0 to %d (expected %d)", 
		     a->dimensions[3], expected_size3);
	  return 0;
        }
        if (expected_size4 > 0) {
          if (a->dimensions[3] != expected_size4) {
	    PyErr_Format(PyExc_ValueError,
		     "NumPy array's 5th index runs from 0 to %d (expected %d)", 
		     a->dimensions[4], expected_size4);
	    return 0;
          }
        }
      }
    }
  }
  return 1;
}


int NumPyArray_Float:: create (int n) 
{ 
  //printf("Creating array(%d)\n", n);
  int dim1[1]; dim1[0] = n; 
  a = (PyArrayObject*) PyArray_SimpleNew(1, dim1, PyArray_DOUBLE);
  if (a == NULL) { 
    printf("creating NumPyArray in C failed, dim=(%d)\n", n);
    return 0;
  }
  return 1;
}

int NumPyArray_Float:: create (int n0, int n1) 
{ 
  //printf("Creating array(%d,%d)\n", n0, n1);
  int dim2[2]; dim2[0] = n0; dim2[1] = n1;
  a = (PyArrayObject*) PyArray_SimpleNew(2, dim2, PyArray_DOUBLE);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d)\n",n0, n1);
    return 0;
  }
  return 1;
}

int NumPyArray_Float:: create (int n0, int n1, int n2) 
{ 
  int dim3[3]; dim3[0] = n0; dim3[1] = n1; dim3[2] = n2;
  a = (PyArrayObject*) PyArray_SimpleNew(3, dim3, PyArray_DOUBLE);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d)\n",n0, n1, n2);
    return 0;
  }
  return 1;
}

int NumPyArray_Float:: create (int n0, int n1, int n2, int n3) 
{ 
  int dim4[4]; dim4[0] = n0; dim4[1] = n1; dim4[2] = n2; dim4[3] = n3;
  a = (PyArrayObject*) PyArray_SimpleNew(4, dim4, PyArray_DOUBLE);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d,%d)\n",n0, n1, n2, n3);
    return 0;
  }
  return 1;
}

int NumPyArray_Float:: create (int n0, int n1, int n2, int n3, int n4) 
{ 
  int dim5[5]; dim5[0] = n0; dim5[1] = n1; dim5[2] = n2; dim5[3] = n3; dim5[4] = n4;
  a = (PyArrayObject*) PyArray_SimpleNew(5, dim5, PyArray_DOUBLE);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d,%d,%d)\n",n0, n1, n2, n3, n4);
    return 0;
  }
  return 1;
}

void NumPyArray_Float:: deallocate()  // JC march 2008
{
  free(a->data);
}

void dump (std::ostream& o, const NumPyArray_Float& a)
{
  int i,j,k,l,m;
  o << "Dump of NumPyArray object:\n";
  if (a.dim() == 1) {
    for (i = 0; i < a.size0(); i++) {
      o << "(" << i << ")=" << a(i) << " ";
      if (i % 6 == 0) { o << '\n'; }
    }
  }
  if (a.dim() == 2) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	o << "(" << i << "," << j << ")=" << a(i,j) << " ";
	if (i % 5 == 0) { o << '\n'; }
      }
    }
  }
  if (a.dim() == 3) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  o << "(" << i << "," << j << "," << k << ")=" << a(i,j,k) << " ";
	  if (i % 4 == 0) { o << '\n'; }
	}
      }
    }
  }
  if (a.dim() == 4) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  for (l = 0; l < a.size3(); l++) {
	    o << "(" << i << "," << j << "," << k << l << ")=" << a(i,j,k,l) << " ";
	    if (i % 3 == 0) { o << '\n'; }
	  }
	}
      }
    }
  }
  if (a.dim() == 5) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  for (l = 0; l < a.size3(); l++) {
	    for (m = 0; m < a.size4(); m++) {
	     o << "(" << i << "," << j << "," << k << "," << l << "," << m << ")=" << a(i,j,k,l,m) << " ";
	      if (i % 2 == 0) { o << '\n'; }
            }
	  }
	}
      }
    }
  }

}

// JC march 2008

int NumPyArray_Int:: checktype () const
{
  if (a->descr->type_num != PyArray_INT) {
    PyErr_Format(PyExc_ValueError,
		 "a is not of type 'Int'");
    return 0;
  }
  return 1;
}

int NumPyArray_Int:: checkdim (int expected_ndim) const
{
  if (a->nd != expected_ndim) {
    PyErr_Format(PyExc_ValueError,
		 "NumPy array is %d-dimensional; expected %d dimensions", 
		 a->nd, expected_ndim);
    return 0;
  } 
  return 1;
}

int NumPyArray_Int:: checksize (int expected_size0, 
				  int expected_size1, 
				  int expected_size2,
				  int expected_size3,
				  int expected_size4) const
{
  if (a->dimensions[0] != expected_size0) {
    PyErr_Format(PyExc_ValueError,
		 "NumPy array's 1st index runs from 0 to %d (expected %d)", 
		 a->dimensions[0], expected_size0);
    return 0;
  }
  if (expected_size1 > 0) {
    if (a->dimensions[1] != expected_size1) {
	PyErr_Format(PyExc_ValueError,
		     "NumPy array's 2nd index runs from 0 to %d (expected %d)", 
		     a->dimensions[1], expected_size1);
	return 0;
    }
    if (expected_size2 > 0) {
      if (a->dimensions[2] != expected_size2) {
	PyErr_Format(PyExc_ValueError,
		     "NumPy array's 3rd index runs from 0 to %d (expected %d)", 
		     a->dimensions[2], expected_size2);
	return 0;
      }
      if (expected_size3 > 0) {
        if (a->dimensions[3] != expected_size3) {
	  PyErr_Format(PyExc_ValueError,
		     "NumPy array's 4th index runs from 0 to %d (expected %d)", 
		     a->dimensions[3], expected_size3);
	  return 0;
        }
        if (expected_size4 > 0) {
          if (a->dimensions[3] != expected_size4) {
	    PyErr_Format(PyExc_ValueError,
		     "NumPy array's 5th index runs from 0 to %d (expected %d)", 
		     a->dimensions[4], expected_size4);
	    return 0;
          }
        }
      }
    }
  }
  return 1;
}


int NumPyArray_Int:: create (int n) 
{ 
  //printf("Creating array(%d)\n", n);
  int dim1[1]; dim1[0] = n; 
  a = (PyArrayObject*) PyArray_SimpleNew(1, dim1, PyArray_INT);
  if (a == NULL) { 
    printf("creating NumPyArray in C failed, dim=(%d)\n", n);
    return 0;
  }
  return 1;
}

int NumPyArray_Int:: create (int n0, int n1) 
{ 
  //printf("Creating array(%d,%d)\n", n0, n1);
  int dim2[2]; dim2[0] = n0; dim2[1] = n1;
  a = (PyArrayObject*) PyArray_SimpleNew(2, dim2, PyArray_INT);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d)\n",n0, n1);
    return 0;
  }
  return 1;
}

int NumPyArray_Int:: create (int n0, int n1, int n2) 
{ 
  int dim3[3]; dim3[0] = n0; dim3[1] = n1; dim3[2] = n2;
  a = (PyArrayObject*) PyArray_SimpleNew(3, dim3, PyArray_INT);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d)\n",n0, n1, n2);
    return 0;
  }
  return 1;
}

int NumPyArray_Int:: create (int n0, int n1, int n2, int n3) 
{ 
  int dim4[4]; dim4[0] = n0; dim4[1] = n1; dim4[2] = n2; dim4[3] = n3;
  a = (PyArrayObject*) PyArray_SimpleNew(4, dim4, PyArray_INT);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d,%d)\n",n0, n1, n2, n3);
    return 0;
  }
  return 1;
}

int NumPyArray_Int:: create (int n0, int n1, int n2, int n3, int n4) 
{ 
  int dim5[5]; dim5[0] = n0; dim5[1] = n1; dim5[2] = n2; dim5[3] = n3; dim5[4] = n4;
  a = (PyArrayObject*) PyArray_SimpleNew(5, dim5, PyArray_INT);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d,%d,%d)\n",n0, n1, n2, n3, n4);
    return 0;
  }
  return 1;
}

void NumPyArray_Int:: deallocate()  // JC march 2008
{
  free(a->data);
}

void dump (std::ostream& o, const NumPyArray_Int& a)
{
  int i,j,k,l,m;
  o << "Dump of NumPyArray object:\n";
  if (a.dim() == 1) {
    for (i = 0; i < a.size0(); i++) {
      o << "(" << i << ")=" << a(i) << " ";
      if (i % 6 == 0) { o << '\n'; }
    }
  }
  if (a.dim() == 2) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	o << "(" << i << "," << j << ")=" << a(i,j) << " ";
	if (i % 5 == 0) { o << '\n'; }
      }
    }
  }
  if (a.dim() == 3) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  o << "(" << i << "," << j << "," << k << ")=" << a(i,j,k) << " ";
	  if (i % 4 == 0) { o << '\n'; }
	}
      }
    }
  }
  if (a.dim() == 4) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  for (l = 0; l < a.size3(); l++) {
	    o << "(" << i << "," << j << "," << k << l << ")=" << a(i,j,k,l) << " ";
	    if (i % 3 == 0) { o << '\n'; }
	  }
	}
      }
    }
  }
  if (a.dim() == 5) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  for (l = 0; l < a.size3(); l++) {
	    for (m = 0; m < a.size4(); m++) {
	     o << "(" << i << "," << j << "," << k << "," << l << "," << m << ")=" << a(i,j,k,l,m) << " ";
	      if (i % 2 == 0) { o << '\n'; }
            }
	  }
	}
      }
    }
  }

}

// JC july 2009

int NumPyArray_Complex:: checktype () const
{
  if (a->descr->type_num != PyArray_CDOUBLE) {
    PyErr_Format(PyExc_ValueError,
		 "a is not of type 'CDouble'");
    return 0;
  }
  return 1;
}

int NumPyArray_Complex:: checkdim (int expected_ndim) const
{
  if (a->nd != expected_ndim) {
    PyErr_Format(PyExc_ValueError,
		 "NumPy array is %d-dimensional; expected %d dimensions", 
		 a->nd, expected_ndim);
    return 0;
  } 
  return 1;
}

int NumPyArray_Complex:: checksize (int expected_size0, 
				  int expected_size1, 
				  int expected_size2,
				  int expected_size3,
				  int expected_size4) const
{
  if (a->dimensions[0] != expected_size0) {
    PyErr_Format(PyExc_ValueError,
		 "NumPy array's 1st index runs from 0 to %d (expected %d)", 
		 a->dimensions[0], expected_size0);
    return 0;
  }
  if (expected_size1 > 0) {
    if (a->dimensions[1] != expected_size1) {
	PyErr_Format(PyExc_ValueError,
		     "NumPy array's 2nd index runs from 0 to %d (expected %d)", 
		     a->dimensions[1], expected_size1);
	return 0;
    }
    if (expected_size2 > 0) {
      if (a->dimensions[2] != expected_size2) {
	PyErr_Format(PyExc_ValueError,
		     "NumPy array's 3rd index runs from 0 to %d (expected %d)", 
		     a->dimensions[2], expected_size2);
	return 0;
      }
      if (expected_size3 > 0) {
        if (a->dimensions[3] != expected_size3) {
	  PyErr_Format(PyExc_ValueError,
		     "NumPy array's 4th index runs from 0 to %d (expected %d)", 
		     a->dimensions[3], expected_size3);
	  return 0;
        }
        if (expected_size4 > 0) {
          if (a->dimensions[3] != expected_size4) {
	    PyErr_Format(PyExc_ValueError,
		     "NumPy array's 5th index runs from 0 to %d (expected %d)", 
		     a->dimensions[4], expected_size4);
	    return 0;
          }
        }
      }
    }
  }
  return 1;
}


int NumPyArray_Complex:: create (int n) 
{ 
  //printf("Creating array(%d)\n", n);
  int dim1[1]; dim1[0] = n; 
  a = (PyArrayObject*) PyArray_SimpleNew(1, dim1, PyArray_CDOUBLE);
  if (a == NULL) { 
    printf("creating NumPyArray in C failed, dim=(%d)\n", n);
    return 0;
  }
  return 1;
}

int NumPyArray_Complex:: create (int n0, int n1) 
{ 
  //printf("Creating array(%d,%d)\n", n0, n1);
  int dim2[2]; dim2[0] = n0; dim2[1] = n1;
  a = (PyArrayObject*) PyArray_SimpleNew(2, dim2, PyArray_CDOUBLE);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d)\n",n0, n1);
    return 0;
  }
  return 1;
}

int NumPyArray_Complex:: create (int n0, int n1, int n2) 
{ 
  int dim3[3]; dim3[0] = n0; dim3[1] = n1; dim3[2] = n2;
  a = (PyArrayObject*) PyArray_SimpleNew(3, dim3, PyArray_CDOUBLE);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d)\n",n0, n1, n2);
    return 0;
  }
  return 1;
}

int NumPyArray_Complex:: create (int n0, int n1, int n2, int n3) 
{ 
  int dim4[4]; dim4[0] = n0; dim4[1] = n1; dim4[2] = n2; dim4[3] = n3;
  a = (PyArrayObject*) PyArray_SimpleNew(4, dim4, PyArray_CDOUBLE);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d,%d)\n",n0, n1, n2, n3);
    return 0;
  }
  return 1;
}

int NumPyArray_Complex:: create (int n0, int n1, int n2, int n3, int n4) 
{ 
  int dim5[5]; dim5[0] = n0; dim5[1] = n1; dim5[2] = n2; dim5[3] = n3; dim5[4] = n4;
  a = (PyArrayObject*) PyArray_SimpleNew(5, dim5, PyArray_CDOUBLE);
  if (a == NULL) { 
    printf("creating a failed, dims=(%d,%d,%d,%d,%d)\n",n0, n1, n2, n3, n4);
    return 0;
  }
  return 1;
}

void NumPyArray_Complex:: deallocate()  // JC march 2008
{
  free(a->data);
}

void dump (std::ostream& o, const NumPyArray_Complex& a)
{
  int i,j,k,l,m;
  o << "Dump of NumPyArray object:\n";
  if (a.dim() == 1) {
    for (i = 0; i < a.size0(); i++) {
      o << "(" << i << ")=" << a(i).real << "+" << a(i).imag << "j ";
      if (i % 6 == 0) { o << '\n'; }
    }
  }
  if (a.dim() == 2) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	o << "(" << i << "," << j << ")=" << a(i,j).real << "+" << a(i,j).imag << "j ";
	if (i % 5 == 0) { o << '\n'; }
      }
    }
  }
  if (a.dim() == 3) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  o << "(" << i << "," << j << "," << k << ")=" << a(i,j,k).real << "+" << a(i,j,k).imag << "j ";
	  if (i % 4 == 0) { o << '\n'; }
	}
      }
    }
  }
  if (a.dim() == 4) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  for (l = 0; l < a.size3(); l++) {
	    o << "(" << i << "," << j << "," << k << l << ")=" << a(i,j,k,l).real << "+" << a(i,j,k,l).imag << "j ";
	    if (i % 3 == 0) { o << '\n'; }
	  }
	}
      }
    }
  }
  if (a.dim() == 5) {
    for (i = 0; i < a.size0(); i++) {
      for (j = 0; j < a.size1(); j++) {
	for (k = 0; k < a.size2(); k++) {
	  for (l = 0; l < a.size3(); l++) {
	    for (m = 0; m < a.size4(); m++) {
	     o << "(" << i << "," << j << "," << k << "," << l << "," << m << ")=" << a(i,j,k,l,m).real << "+" << a(i,j,k,l,m).imag << "j ";
	      if (i % 2 == 0) { o << '\n'; }
            }
	  }
	}
      }
    }
  }

}


