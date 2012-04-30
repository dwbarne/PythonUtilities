#!/usr/local/bin python

# Solves a pair of simultaneous equations of the form
#   Ay + Bx = C
#   Dy + Ex = F
#
# The user must input A, B, C, D, E, F
# Output consists of the (x,y) pair that is a solution to both equations

# needed to read in data
import sys

def solution(A,B,C,D,E,F):
    "solve a pair of simultaneous equations"
    denom=A*E-D*B
    print "\n denom = %d \n" % denom

    try:
        x=(A*F-D*C)/(A*E-D*B)
        y=C/A - (B/A)*((A*F-D*C)/(A*E-D*B))   
    except ZeroDivisionError:
        print "\nEquations are indeterminate -- denominator is zero!\n"
        exit()
    except:
        print "\n Unknown exception has been raised! Return (0,0).\n"
        return (0,0)
    else:
        print "\n >>> Good solution!\n"
        return (x,y) 
	
print "Step 1: Enter the coefficients A, B, and C of the first equation"
print "  of the form"
print "   A*x + B*y = C"
print " "
A=float(raw_input(" > Input coefficient A: "))
B=float(raw_input(" >       coefficient B: "))
C=float(raw_input(" >       coefficient C: "))


print " "
print " Step 2: Enter the coefficients D, E, and F of the second equation"
print "  of the form"
print "    D*x + E*y = F"
print " "
D=float(raw_input(" > Input coefficient D: "))
E=float(raw_input(" > Input coefficient E: "))
F=float(raw_input(" > Input coefficient F: "))

# solution(A,B,C,D,E,F)

(x,y)=solution(A,B,C,D,E,F)

print " "
print " Eqn 1: %d*y + %d*x = %d" % (A,B,C)
print " Eqn 2: %d*y + %d*x = %d" % (D,E,F)
print " "
print " \n...Answer: x= %3.3f,  y= %3.3f " % (x,y)
print "\n--End--\n"


