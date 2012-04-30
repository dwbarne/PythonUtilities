#
# Module manyxvalues
#  Ref: Learning Python, p. 338

X=11

class c:
	X=22
	def m(self):
		X=33
		self.X=44
	
def f():
	X=55

def g():
	print X
	
	
"""
To implement, run python in this directory and type following:


obj=c()
print c.X
print obj.X

obj.m()
print obj.X
print c.X
print X

# print c.m.X 	#Fails: onlyh visible in method
# print f.X		# FAILS: only visible in function
