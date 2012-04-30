"""
There are several things that don't work as expected.

openMP acceleration is only about 2.2

Now for many points in the complex plane the cpu work is minimal, mostly loops.

It may have something to do with chunk, schedule,...

cset() doesn't work!!! Why??

JC, Santiago, July 21, 2009
"""

import ext_mandelbrot
import numpy
import time

xmin, xmax, ymin, ymax = -2.5, 1.5, -2.0, 2.0
imax = 80
d2 = 2.0

x = xmin + (xmax-xmin)*numpy.arange(600.0)/600
y = ymin + (ymax-ymin)*numpy.arange(600.0)/600

xx,yy = numpy.meshgrid(x,y)
ci = numpy.complex(0.0,1.0)

zz = xx+ci*yy
print zz.real.max(), zz.imag.max()

e0 = time.time()
out = ext_mandelbrot.mandelbrot(zz,imax,d2)
elapsed_time = time.time()-e0

print "\nelapsed time = %7.4f secs." % elapsed_time

print out.min(), out.max()

# The remaining lines of codes generate nice grayscale and color figures.
# The color figure uses HSV colormap. There may be a module for doing this.

from PIL import Image

# grayscale

img = Image.new("L",(600,600),0)

img.fromstring(out.astype('B').tostring())

print img.getextrema()
img.save("mandel.png")

# color

h = 360.0-out.astype('d')/out.max()*360.0
v = numpy.ones(h.shape, 'd')
s = numpy.ones(h.shape, 'd')

hi = numpy.floor(h/60.0)
hi = numpy.mod(hi,6)
f = h/60 - numpy.floor(h/60)
p = v*(1.0-s)
q = v*(1.0-f*s)
t = v*(1.0-(1.0-f)*s)
r = v*numpy.equal(hi,0)+q*numpy.equal(hi,1)+p*numpy.equal(hi,2)+p*numpy.equal(hi,3)+t*numpy.equal(hi,4)+v*numpy.equal(hi,5)
g = t*numpy.equal(hi,0)+v*numpy.equal(hi,1)+v*numpy.equal(hi,2)+q*numpy.equal(hi,3)+p*numpy.equal(hi,4)+p*numpy.equal(hi,5)
b = p*numpy.equal(hi,0)+p*numpy.equal(hi,1)+t*numpy.equal(hi,2)+v*numpy.equal(hi,3)+v*numpy.equal(hi,4)+q*numpy.equal(hi,5)

r *= numpy.not_equal(out,imax)
g *= numpy.not_equal(out,imax)
b *= numpy.not_equal(out,imax)

print r.max(), g.max(), b.max()

img_r = Image.new("L",(600,600),0)
img_g = Image.new("L",(600,600),0)
img_b = Image.new("L",(600,600),0)
img = Image.new("RGB",(600,600))

img_r.fromstring(r.astype('B').tostring())
img_g.fromstring(g.astype('B').tostring())
img_b.fromstring(b.astype('B').tostring())

rgb = numpy.zeros((r.size,3),'d')
rgb[:,0] = numpy.ravel(r)*255
rgb[:,1] = numpy.ravel(g)*255
rgb[:,2] = numpy.ravel(b)*255
img.fromstring(rgb.astype('B').tostring())

img.save("mandel_hsv.png")

