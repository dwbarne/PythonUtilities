"""slotter.py
"""
#import os
import sys

class Slotter(object):	# must use python 2.2 or higher; python 2.0 does not work here
    __slots__  =  ["x", "y", "z"]

    def __init__(self, x, y, z):
        self.x  =  x
        self.y  =  y
        self.z  =  z

#================================================================

s1 = Slotter(4, 5, 6)
s2 = Slotter(0, 0, 7)

print s1.x, s1.y, s1.z
print s2.x, s2.y, s2.z
s1.foo = 55
print s1.foo
