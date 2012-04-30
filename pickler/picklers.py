#!/usr/bin/env python
#================================================================
# picklers.py:  Objects for pickle testing: can an object
#   reconstitute itself in its constructor?
# Answer: no, but it can be done with static methods.
#----------------------------------------------------------------

import pickle

class A:
    def __init__ ( self, x ):
        self.x  =  x
        self.__privy  =  'privy'
        self.__tab    =  {0: 'red', 1: 'green'}

    def show ( self ):
        print "A.show(): .x=", self.x
        print "A.show(): .__privy=", self.__privy
        print "A.show(): .__tab=", self.__tab

class B:
    def __init__ ( self ):
        self.__L  =  [A(i) for i in range(5)]

    def show ( self ):
        for item in self.__L:
            item.show()

    def save ( x, fileName ):
        """Pickle an instance and write to the given named file.
        """
        outFile  =  open ( fileName, 'w' )
        pickle.dump ( x, outFile )
        outFile.close()

    save = staticmethod ( save )

    def restore ( fileName ):
        """Using a pickled instance in the given file, return the instance.
        """
        inFile  =  open ( fileName )
        newB  =  pickle.load ( inFile )
        inFile.close()
        return newB

    restore  =  staticmethod ( restore )


#================================================================

if  __name__  ==  '__main__':
    b  =  B()
    print "Original object:"
    b.show()
    B.save ( b, 'saveme' )

    print "\nReconstitute:"
    newB  =  B.restore('saveme')
    newB.show()
