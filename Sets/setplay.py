#!/usr/bin/env python
#================================================================
# setplay: Demonstrate sets
#----------------------------------------------------------------

#================================================================
# Imports
#----------------------------------------------------------------

import sys
import random

#================================================================
# Manifest constants
#----------------------------------------------------------------

#================================================================
# Functions and classes
#----------------------------------------------------------------


# - - -   m a i n

def main():
    """
    """
    traffic = set ( [ "red", "yellow", "green" ] )
    rainbow = set ( [ "red", "orange", "yellow", "green",
                      "blue", "violet" ] )
    print "traffic", traffic
    print "rainbow", rainbow
    print "list(rainbow)", list(rainbow)
    sortedRainbow = list(rainbow)
    sortedRainbow.sort()
    print "sortedRainbow", sortedRainbow
    rgb = set ( [ "red", "green", "blue" ] )
    print "rgb", rgb
    print "rgb & traffic", rgb & traffic
    print "rgb | traffic", rgb | traffic
    print "rainbow - rgb", rainbow - rgb
    print "traffic ^ rgb", traffic ^ rgb

    someNumbers = [ random.randint ( 1, 20 )
                    for i in range(15) ]
    print "someNumbers", someNumbers
    someSet = set(someNumbers)
    print "someSet", someSet


#================================================================
# Epilogue
#----------------------------------------------------------------

if __name__ == "__main__":
    main()
