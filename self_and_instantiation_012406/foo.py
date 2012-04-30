#!/usr/local/bin/python

class C:
    def __init__ ( self, color ):
        self.colorName = color

    def set(self, x):
        self.bar  =  x
#==============================
c1 = C("green")			# instantiate c1
print c1.colorName		# note that c1 is passed in as self
c1.set(15)				# now we can call c1.set, passing in the value of 15
print c1.bar			#    and print out c1.bar which has been assigned the value 15

c2=C("puce")			# instantiate c2
print c2.colorName		# we can now print out the color name of 'puce'
print c1.bar			#   and can STILL print out c1.bar as 15; value not changed