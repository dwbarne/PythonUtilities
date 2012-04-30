#!/usr/bin/env python

# run as follows, in a standard command line window
#    python testset.py < testdata.txt
#================================================================
# testset: Read a file and print unique lines, sorted
#----------------------------------------------------------------

#================================================================
# Imports
#----------------------------------------------------------------

import sys

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
    answer = set()
    for line in [ s.rstrip() for s in sys.stdin ]:
        answer.add ( line )
    answerList = list (answer)
    answerList.sort()
    for line in answerList:
        print line,
    print

#================================================================
# Epilogue
#----------------------------------------------------------------

if __name__ == "__main__":
    main()
