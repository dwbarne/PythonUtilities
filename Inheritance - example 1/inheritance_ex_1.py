# Can a class talk to another class?
#
# DWB 052808

def func1(value):
    print " From func1, value is ", value

class Class1():
    class1Data=5
    print " This is Class1(), class1Data = ", class1Data 
    
    def testPrint1(self):
        print " 888888  This is def testPrint1"
#    call_2_from_1=Class2()
    
class Class2(Class1):
    def __init__(self,print_value):
        self.print_value=print_value
        self.class2Data=15
        self.class3Data=100
        if self.print_value == 1:
            print "   print_value = %d " % self.print_value
#        if self.print_value == 2:
#            print "        print_value = %d, class2Data = " % (self.print_value, class2Data)
    
    class2Data=10
    
    func1(3)
#    def testPrint(self):
#        print " *** Inside testPrint, class2Data = ", self.class2Data
#        print ' *** Inside testPrint, class3Data = ', self.class3Data
#    if self.print_value == 2:
#        print "        print_value = %d, class2Data = " % (self.print_value, class2Data)

    print "   This is Class2(), class2Data =", class2Data
#    call_1_from_2=Class1()
#    call_1_from_2.testPrint1()

# class1Data is not defined within the scope of Class2
#    print " class1Data before instantiate Class2 = ",class1Data

# Proof you can instantiate Class1 from within Class2 even tho Class2 also inherits from Class1
#    testclass=Class1()
#    testclass.testPrint1()

#    print " class1Data after instantiate Class2 = ",class1Data
    print "         This is the third print statement"
  
#print " *** class2Data = ", class2Data  
class2=Class2(1)
class22=Class2(2)
#class22.testPrint()
class2.testPrint1()
class22.testPrint1()