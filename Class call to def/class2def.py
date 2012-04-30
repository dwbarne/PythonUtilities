# test program to see if classes can make calls to defs outside of the calling class

import sys
import os


class Temp1():
    def __init__(self,input1):
        self.input1=input1
        self.callprint()
        printdef(input1)
        
    def callprint(self):
        printdef(self.input1)
        
def printdef(input):
    print "\n Value of input = %s" % input
    
test=Temp1(5)
#test.callprint()
printdef(10)