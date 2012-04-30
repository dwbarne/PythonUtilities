#! /usr/bin/python

class Class1():
    x10=10
    x20=20
    print "Before __init__, x10 = %d, x20 = %d\n" % (x10,x20)
    def __init__(self, x100, x200):
        self.x100=x100
        self.x200=x200
        self.x10=10000
        print "After __init__, x10 = %d, x20 = %d\n" % (self.x10,self.x20)

    def print_results(self):
        print "\nx100 = %d, x200 = %d\n" % (self.x100, self.x200)
        print "\nx100 = %d\n" % self.x100
        print "\nx10 = %d\n" % self.x10
        x20=2000
        return
    
test=Class1(100, 200)
#test.print_results()