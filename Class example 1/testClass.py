
class testClass(object):
    print "Creating New Class \n==================="
#    number=5
    num=10
    num2=20
    def __init__(self, string):
        self.string=string
        self.number=5
    def printClass(self):
        print "Number = %d" % self.number
        print "String = %s" % self.string
        
if __name__ == '__main__':
    tc=testClass("Five")
    tc.printClass()
    tc.number=10
    tc.string="Ten"
    tc.printClass()

