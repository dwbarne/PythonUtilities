#
# area calculations
#   from website: http://www.freenetpages.co.uk/hp/alan.gauld/tutclass.htm
#   modified by D. Barnette, 051608
#

class Square:
	def __init__(self,side):
		self.side=side
	def calculateArea(self):
		return "square",self.side**2
		
class Circle:
	def __init__(self,radius):
		self.radius=radius
	def calculateArea(self):
		import math
		return "circle",math.pi*(self.radius**2)
		
class Area:
	def __init__(self,length):
		self.length=length
	def Square(self):
		return 'square',self.length**2
	def Circle(self):
		import math
		return 'circle',math.pi*(self.length**2)

if __name__ == '__main__':
#	list=[("square",Square(4)), ("square",Square(16)), ("circle",Circle(2)), ("circle",Circle(8))]
	list1=[Square(4), Square(16), Circle(2), Circle(8)]
	print
	print '** For list1:'
	for calc in list1:
		print "The area for shape %s is %6.2f" % (calc.calculateArea() )
		
	print
	print '** For list2:'
	
	list2=[Area(4).Square(), Area(16).Square(), Area(2).Circle(), Area(8).Circle()]
	
	for calc in list2:
		print "The area for shape %s is %6.2f" % (calc)
		
	print
	print '** For list3:'
	
	list3=[2,4,6,8]
	
	for num in list3:
		print "**For length %s:" % num
		print " The area for shape %s is %6.2f" % Area(num).Square()
		print "   The area for shape %s is %6.2f" % Area(num).Circle()
	
	print "\n -- Program Finished --\n\n"
