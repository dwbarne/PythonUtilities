#!/usr/bin/env python
#================================================================
# regex: Regular expression demo
#----------------------------------------------------------------

#================================================================
# Imports
#----------------------------------------------------------------

import sys
import re

#================================================================
# Manifest constants
#----------------------------------------------------------------

REGEX = r'[pP]ylot'

#================================================================
# Functions and classes
#----------------------------------------------------------------


# - - -   m a i n

def main():
    """
    """
    test ( "xxxxxxxxx" )
    test ( "xxxxxxxxxpylotyyyyyyyyyy" )
    test ( "Pylot" )

def test ( s ):
    '''Test to see if s matches REGEX
    '''
    print "Search string <%s>" % s
    m = re.search ( REGEX, s )
    if m is None:
        print "No match"
    else:
        print "Prefix <%s>" % s[:m.start()]
        print "Matched part <%s>" % s[m.start():m.end()]
        print "Matched part <%s>" % m.group()
        print "Suffix <%s>" % s[m.end():]



#================================================================
# Epilogue
#----------------------------------------------------------------

if __name__ == "__main__":
    main()
