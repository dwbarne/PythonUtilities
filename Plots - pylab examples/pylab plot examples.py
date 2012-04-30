#!/usr/bin/env python
# load_camp_revised.py
#  shows example of pylab plots
#-----------------------------------------------------------------------

# import stuff
import pylab
import time, sys
####import numpy

# print version number
####print " "
####print " numpy version ",numpy.__version__

# create an array of floating point 

start = 0.0
stop  = 128.0
step  = 1.0
x = pylab.arange(start, stop, step, 'float')
# square it
y = x*x
lenx = len(x)
print len(x),len(y)
print x[lenx-1], y[lenx-1]

# create an empty "ndarray"
xy = pylab.empty( (lenx,2), typecode='f')
# fill the array with x and y
xy[:,0] = x
xy[:,1] = y

# clear the figure
pylab.clf()
#create first of 2 sub plots
pylab.subplot(211)
pylab.xlabel('X')
pylab.ylabel('X * X')
pylab.plot(xy[:,0],xy[:,1])

# create second of 2 sub plots
pylab.subplot(212)
pylab.cla()
pylab.xlabel('index')
pylab.ylabel('X')
pylab.plot(xy[:,0])

# force the display
pylab.show()

