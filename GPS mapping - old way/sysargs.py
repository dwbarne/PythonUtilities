"""sysargs.py:  Object to check command line arguments
        $Revision: 1.6 $  $Date: 2004/01/06 22:16:20 $

Exports:
  class SysArgs:  Represents digested command line arguments.
    SysArgs(switchSpecs, posSpecs):
      [ if (switchSpecs is a list of SwitchArg objects
        representing switches accepted by this program,
        and is-switch-valid(switchSpecs)) and
        ( posSpecs is a list of PosArg objects representing
        positional arguments accepted by this program,
        and is-pos-list-valid(posSpecs)) ->
          if (sys.argv contains only switches in switchSpecs) and
          (sys.argv's positional arguments conform to posSpecs) ->
            return a new SysArgs object representing those digested
            arguments
          else ->
            sys.stderr  +:=  (usage message) + (error message)
            stop execution ]
    .switchSpecs:    [ as passed to constructor, read-only ]
    .posSpecs:       [ as passed to constructor, read-only ]
    .switchMap:
      [ a dictionary mapping L |-> s, for L the set of all
        SwitchArg.letter values, and s is:
                takesValue      Supplied      Not supplied
                ----------      --------      ------------
                    0               1               0
                    1               string          None ]
    .posMap:
      [ the positional arguments from sys.argv, in a 1-1 correspondence
        with the elements of self.posSpecs, as a dictionary mapping
        k |-> v, where k is the PosArg.key value, and v is None
        for a missing optional unrepeated argument, the value as
        a string for a present unrepeated argument, and a list of strings
        for a repeated argument ]
          | Example:
          |     args = SysArgs (
          |         [ SwitchArg ( "v", [ "verbose output" ] ),
          |           SwitchArg ( "f",
          |             [ "Use this argument to specify the name of a file",
          |               "that you wanted mangled." ], takesValue=1 ),
          |           SwitchArg ( "o", [ "output file (optional)" ],
          |             takesValue=1 ) ],
          |         [ PosArg ( "infiles",
          |             [ "Names of input files to be mangled." ],
          |             repeated=1 ),
          |           PosArg ( "logfile",
          |             [ "Output log file." ] ) ] )
          |     print "f argument value is:", args.switchMap["f"]
          |     print "3rd input file is:", args.posMap["infiles"][2]
  def usage(switchSpecs, posSpecs, *textList):
    [ if (switchSpecs and posSpecs are as passed to SysArgs)
      and (textList is a list of strings) ->
        sys.stderr  +:=  (usage message) + (concatenation of textList)
        stop execution ]
  class SwitchArg:  Represents one possible switch argument
    SwitchArg(letter, description, takesValue=0):
      [ if (letter is the switch letter as a one-character string)
        and (takesValue is true if the switch must have a value)
        and (description is a textual description of the meaning
        of the switch as a list of strings not exceeding 60
        characters per string) ->
          return a new SwitchArg object representing those values ]
    .letter:        [ as passed to constructor ]
    .description:   [ as passed to constructor ]
    .takesValue:    [ as passed to constructor ]
  class PosArg:  Represents one (possibly repeated) positional argument
    PosArg ( key, description, optional=0, repeated=0 ):
      [ if (key is the name of this argument in the usage message)
        and (description is as in SwitchArg())
        and (optional is true iff the positional argument is optional)
        and (repeated is true iff the argument may be repeated) ->
          return a new PosArg representing those values ]
    .key:           [ as passed to constructor ]
    .description:   [ as passed to constructor ]
    .optional:      [ as passed to constructor ]
    .repeated:      [ as passed to constructor ]
"""

#================================================================
# Contents
#----------------------------------------------------------------
# 1. Exports (above).
# 2. Imports.
# 3. Verification functions.
# 4. Classes and functions.
#----------------------------------------------------------------


#================================================================
# Imports
#----------------------------------------------------------------

import sys          # For sys.argv, raw command line arguments
import getopt       # Python's rough digester for arguments


#================================================================
# Verification functions
#----------------------------------------------------------------
# is-pos-list-valid(posSpecs) ==
#   if posSpecs contains more than one repeating element ->
#     0
#   else if posSpecs contains one repeating element and one
#   or more optional elements ->
#     0
#   else if any non-optional element of posSpecs occurs after
#   any optional element ->
#     0
#   else -> 1
#--
# Explanation:
#   - There can be only repeating element in an argument list.
#   - If a set of positional arguments contains a repeating element,
#     it cannot have an optional element.  For example, if repeating
#     argument R is followed by optional argument Q, is a list of
#     three arguments [R,R,Q] or [R,R,R]?
#   - Optional elements must all be bunched up at the end.
#----------------------------------------------------------------
# is-switch-list-valid(switchSpecs) ==
#   if there any duplicates in the .letter members of switchSpecs ->
#     0
#   else -> 1
#--
#   We don't allow more than one of a switch.  If we did, one or
#   more of the values would be discarded, since we are storing the
#   values in a dictionary with the switch letters as keys.
#----------------------------------------------------------------


# - - - - -   c l a s s   S y s A r g s   - - - - -

class SysArgs:
    """Represents validated command line arguments.

      State/Invariants:
        .__optx:
          [ if self.posSpecs contains any optional arguments ->
              the index in self.posSpecs of the first one
            else -> None ]
        .__repx:
          [ if self.posSpecs contains a repeating argument ->
              its index in self.posSpecs
            else -> None ]
    """


# - - -   S y s A r g s . _ _ i n i t _ _   - - -

    def __init__ ( self, switchSpecs, posSpecs ):
        "Constructor for SysArgs"

        #-- 1 --
        self.switchSpecs  =  switchSpecs
        self.posSpecs     =  posSpecs
        self.switchMap   =  {}
        self.posMap      =  {}

        #-- 2 --
        # [ if sys.argv passes getopt.getopt ->
        #     optList  :=  options returned by getopt.getopt()
        #     posList  :=  args returned by getopt.getopt()
        #   else ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution ]
        optList, posList  =  self.__roughSort ( )

        #-- 3 --
        # [ if optList is consistent with self.switchSpecs and
        #   its letters are unique ->
        #     self.switchMap  +:=  entries mapping letters from
        #         optList |-> the option values as in the invariant
        #   else ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution ]
        self.__optCheck ( optList )

        #-- 4 --
        # [ if posList is consistent with self.posSpecs ->
        #     self.posMap  +:=  entries mapping k |-> v where
        #         k is the set of .key values in self.posSpecs
        #         and the values v are as in the invariant
        #     self.__optx  :=  as invariant
        #     self.__repx  :=  as invariant
        #     return self
        #   else ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution ]
        self.__posCheck ( posList )


# - - -   S y s A r g s . _ _ r o u g h S o r t   - - -

    def __roughSort ( self ):
        """Rough syntax checking of the arguments.

          [ if sys.argv passes getopt.getopt ->
              return (options returned by getopt.getopt(),
                      args returned by getopt.getopt())
            else ->
              sys.stderr  +:=  (usage message) + (error message)
              stop execution ]
        """

        #-- 1 --
        # [ optionString  :=  string for the 2nd argument of
        #                     getopt.getopt, based on self.switchSpecs ]
        optionString  =  self.__buildOptionString ( )
        
        #-- 2 --
        # [ if sys.argv is valid according to getopt.getopt ->
        #     return (optList, argList) as getopt.getopt does
        #   else ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution ]
        try:
            result  =  getopt.getopt ( sys.argv[1:], 
                                                 optionString )
            return result
        except getopt.GetoptError, detail:
            usage ( self.switchSpecs, self.posSpecs, str(detail) )


# - - -   S y s A r g s . _ _ b u i l d O p t i o n S t r i n g   - - -

    def __buildOptionString ( self ):
        """Set up the string that tells getopt.getopt what switches we allow

          [ if self.switchSpecs is as invariant ->
              optionString  :=  string for the 2nd argument of
                                getopt.getopt, based on self.switchSpecs ]
        """

        #-- 1 --
        result  =  []

        #-- 2 --
        # [ result  +:=  strings defining each element of self.switchSpecs
        #                as getopt.getopt requires it ]
        for  sw in self.switchSpecs:
            #-- 2 body --
            # [ if sw is a SwitchArg ->
            #     result  +:=  a string defining sw as getopt.getopt
            #                  requires it ]
            if  sw.takesValue:
                result.append ( "%s:" % sw.letter )
            else:
                result.append ( sw.letter )

        #-- 3 --
        # [ return the strings in result, concatenated ]
        return "".join ( result )


# - - -   S y s A r g s . _ _ o p t C h e c k   - - -

    def __optCheck ( self, optList ):
        """Check option switches
          [ if (optList is the list of switches as returned by
            getopt.getopt()) ->
              if optList is consistent with self.switchSpecs and
              its letters are unique ->
                self.switchMap  +:=  entries mapping letters from
                    optList |-> the option values as in the invariant
              else ->
                sys.stderr  +:=  (usage message) + (error message)
                stop execution ]
        """

        #-- 1 --
        # [ self.switchMap  +:=  entries mapping L |-> 0 for
        #       L ranging over all .letter members of self.switchSpecs ]
        for  switch in self.switchSpecs:
            if  switch.takesValue:
                self.switchMap[switch.letter]  =  None
            else:
                self.switchMap[switch.letter]  =  0

        #-- 2 --
        # [ if any element of optlist corresponds to a letter not a
        #   key in self.switchMap ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution ]
        #   else ->
        #     self.switchMap  :=  self.switchMap with values added
        #         from entries in optList whose letters correspond
        #         to the keys in self.switchMap ]
        for switch, value in optList:
            #-- 1 body --
            # [ if switch[1] is a letter in self.switchSpecs but not
            #   a key in self.switchMap ->
            #     if value is "" ->
            #       self.switchMap[switch[1]]  :=  1
            #     else ->
            #       self.switchMap[switch[1]]  :=  value
            #   else ->
            #     sys.stderr  +:=  (usage message) + (error message)
            #     stop execution ]
            self.__checkSwitch ( switch[1], value )


# - - -   S y s A r g s . _ _ c h e c k S w i t c h   - - -

    def __checkSwitch ( self, letter, value ):
        """Validate and store one command line option.

          [ if (letter is a switch letter) and (value is a string)
            and (self.switchMap contains entries whose keys are
            all the letters from self.switchSpecs ->
              if letter is a letter in self.switchSpecs but not
              a key in self.switchMap ->
                if value is "" ->
                  self.switchMap[letter]  :=  1
                else ->
                  self.switchMap[letter]  :=  value
              else ->
                sys.stderr  +:=  (usage message) + (error message)
                stop execution ]
        """

        #-- 1 --
        # [ if letter is a key in self.switchMap -> I
        #   else ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution ]
        if  not self.switchMap.has_key ( letter ):
            usage ( self.switchSpecs, self.posSpecs,
                    "No such switch: -%s" % letter )

        #-- 2 --
        if  len(value) == 0:
            self.switchMap[letter]  =  1
        else:
            self.switchMap[letter]  =  value


# - - -   S y s A r g s . _ _ p o s C h e c k   - - -

    def __posCheck ( self, posList ):
        """Check the positional arguments from posList against self.posSpecs

          [ if posList is a list of strings representing positional
            command line arguments ->
              if posList is consistent with self.posSpecs ->
                self.posMap  +:=  entries mapping k |-> v where
                    k is the set of .key values in self.posSpecs
                    and the values v are as in the invariant
                self.__optx    :=  as invariant
                self.__repx    :=  as invariant
                self.__minPos  :=  as invariant
                self.__maxPos  :=  as invariant
              else ->
                sys.stderr  +:=  (usage message) + (error message)
                stop execution ]
        """

        #-- 1 --
        # [ if is-pos-list-valid(self.posSpecs) ->
        #     self.__optx    :=  as invariant
        #     self.__repx    :=  as invariant
        #     self.__minPos  :=  as invariant
        #     self.__maxPos  :=  as invariant
        #   else ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution ]
        self.__validatePosList ( )

        #-- 2 --
        # [ if posList is a valid sequence of positionals as
        #   specified by self.posSpec ->
        #     self.posMap  :=  as invariant from posList
        #   else ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution ]
        self.__storePositionals ( posList )


# - - -   S y s A r g s . _ _ v a l i d a t e P o s L i s t   - - -

    def __validatePosList ( self ):
        """Insure is-pos-list-valid(self.posSpecs)

          [ if is-pos-list-valid(self.posSpecs) ->
              self.__optx    :=  as invariant
              self.__repx    :=  as invariant
            else ->
              sys.stderr  +:=  (usage message) + (error message)
              stop execution ]
        """

        #-- 1 --
        self.__optx    =  None
        self.__repx    =  None

        #-- 2 --
        # [ if (self.posSpecs contains multiple repeated elements)
        #   or (self.posSpecs contains one repeated element and any
        #   optional element)
        #   or (self.posSpecs contains any non-optional element after
        #   any optional element) ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution
        #   else ->
        #     self.__optx    :=   as invariant
        #     self.__repx    :=   as invariant
        for  posx in range ( len ( self.posSpecs ) ):
            #-- 2 body --
            # [ if (self.posSpecs[posx] is repeated but there is already
            #   a repeated element)
            #   or (self.posSpecs[posx] is repeated or non-optional
            #   but there are already optional elements) ->
            #     sys.stderr  +:=  (usage message) + (error message)
            #     stop execution
            #   else if self.posSpecs[posx] is repeated ->
            #     self.__repx  :=  posx
            #   else if (self.posSpecs[posx] is optional)
            #   and (self.__optx is None) ->
            #     self.__optx  :=  posx
            #   else -> I ]
            self.__validatePosSpec ( posx )


# - - -   S y s A r g s . _ _ v a l i d a t e P o s S p e c   - - -

    def __validatePosSpec ( self, posx ):
        """Check one positional specifier for validity.

          [ if posx is an index in self.posSpecs ->
              if (self.posSpecs[posx] is repeated but there is already
              a repeated element)
              or (self.posSpecs[posx] is repeated or non-optional
              but there are already optional elements)
              or (self.posSpecs[posx] is both repeated and optional) ->
                sys.stderr  +:=  (usage message) + (error message)
                stop execution
              else if self.posSpecs[posx] is repeated ->
                self.__repx  :=  posx
              else if (self.posSpecs[posx] is optional)
              and self.__optx is None) ->
                self.__optx  :=  posx ]
              else -> I ]
        """

        #-- 1 --
        posArg  =  self.posSpecs[posx]

        #-- 2 --
        if  posArg.repeated:
            if  self.__repx is not None:
                usage ( self.switchSpecs, self.posSpecs,
                    "Programming error: multiple repeated positionals." )
            if  self.__optx is not None:
                usage ( self.switchSpecs, self.posSpecs,
                    "Programming error: you can't mix repeated and ",
                    "optional arguments." )
            if  posArg.repeated and posArg.optional:
                usage ( self.switchSpecs, self.posSpecs,
                        "Programming error: an argument can't be both ",
                        "repeated and optional." )
            self.__repx    =   posx
        elif  posArg.optional:
            if  self.__repx is not None:
                usage ( self.switchSpecs, self.posSpecs,
                    "Programming error: you can't mix repeated and ",
                    "optional arguments." )
            if  self.__optx is None:
                self.__optx  =  posx
        else:   # Required, non-repeating
            if  self.__optx is not None:
                usage ( self.switchSpecs, self.posSpecs,
                    "Programming error: all optional arguments ",
                    "must be last." )


# - - -   S y s A r g s . _ _ s t o r e P o s i t i o n a l s   - - -

    def __storePositionals ( self, posList ):
        """Allocate positional arguments to their self.posSpecs members

          [ if posList is a list of positional arguments as strings ->
              if posList is a valid sequence of positionals as
              specified by self.posSpec ->
                self.posMap  :=  as invariant from posList
              else ->
                sys.stderr  +:=  (usage message) + (error message)
                stop execution ]
        """

        #-- 1 --
        if  self.__repx is not None:
            #-- 1.1 --
            # [ if posList matches self.posSpecs ->
            #     self.posMap  +:=  entries mapping keys from
            #         self.posSpecs |-> corresponding values from
            #         posList, with any repeated arguments packed into
            #         a list under key self.posSpecs[self.__repx].key
            #   else ->
            #     sys.stderr  +:=  (usage message) + (error message)
            #     stop execution ]
            self.__scatterRepeated ( posList )
        elif self.__optx is not None:
            #-- 1.2 --
            # [ if posList matches self.posSpecs ->
            #     self.posMap  +:=  entries mapping keys from
            #         self.posSpecs |-> corresponding values from
            #         posList, or None for missing optional arguments
            #   else ->
            #     sys.stderr  +:=  (usage message) + (error message)
            #     stop execution ]
            self.__scatterOptionals ( posList )
        else:
            #-- 1.3 --
            # [ if posList matches self.posSpecs ->
            #     self.posMap  +:=  entries mapping keys from
            #         self.posSpecs |-> corresponding values from posList
            #   else ->
            #     sys.stderr  +:=  (usage message) + (error message)
            #     stop execution ]
            self.__scatterRequireds ( posList )


# - - -   S y s A r g s . _ _ s c a t t e r R e p e a t e d   - - -

    def __scatterRepeated ( self, posList ):
        """Allocate positionals when one is repeated.

          [ if (posList is the list of positional arguments as strings)
            and (self.__repx is not None) ->
              if posList matches self.posSpecs ->
                self.posMap  +:=  entries mapping keys from
                    self.posSpecs |-> corresponding values from
                    posList, with any repeated arguments packed into
                    a list under self.posSpecs[self.__repx].key
              else ->
                sys.stderr  +:=  (usage message) + (error message)
                stop execution ]

            Here's how arguments from posList map onto self.posSpecs.
            The most general case is where there are required arguments
            both before and after the repeated argument R2:

                |<------------ len(poslist) ------------>|
                |<-- self.__repx -->|<-numReps->|
                +===================+===========+========+
        posList | initial, required | repeated  | final, |     ACTUAL
                |                   |           | req'd  |    POSITIONALS
                +===================+===========+========+
                |                   |          /        /
                |                   |         /        /
                |                   |        /        /
                v                   v       /        /
                |<-- self.__repx -->|<-1->|v        v
                +===================+=====+========+
  self.posSpecs | initial, required | rep.| final, |    POSITIONAL ARG.
                |                   |     | req'd  |       SPECIFIERS
                +===================+=====+========+
                |<------ len(self.posSpecs) ------>|
        """

        #-- 1 --
        # [ numNonReps  :=  len(self.posSpecs) - 1
        #   numReps     :=  len(posList) - (len(self.posSpecs) - 1) ]
        # NB: numNonReps is the total number of non-repeating required
        # arguments, and numReps is the number of positionals from posList
        # that correspond to the repeated argument.
        numNonReps  =  len(self.posSpecs) - 1
        numReps     =  len(posList) - numNonReps

        #-- 2 --
        # [ if numReps < 0 ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution
        #   else -> I ]
        if numReps < 0:
            usage ( self.switchSpecs, self.posSpecs,
                    "Only %d positional arguments were supplied, "
                    "need at least %d." %
                    ( len(posList), len(self.posSpecs) - 1 ) )

        #-- 3 --
        # [ self.posMap  +:=  entries mapping keys of
        #       self.posSpecs[0:self.__repx] |-> poslist[0:self.__repx] ]
        for  posx in range ( self.__repx ):
            self.posMap[self.posSpecs[posx].key]  =  posList[posx]

        #-- 4 --
        # [ self.posMap  +:=  an entry mapping the key of
        #       self.posSpecs[self.__repx].key |-> the list
        #       posList[self.__repx:self__repx+numReps] ]
        self.posMap[self.posSpecs[self.__repx].key]  =  (
            posList[self.__repx:self.__repx+numReps] )

        #-- 5 --
        # [ self.posMap  +:=  entries mapping keys of
        #       self.posSpecs[self.__repx+1:] |->
        #       posList[self.__repx+numReps:] ]
        for  spex in range ( self.__repx+1, len(self.posSpecs)):
            sourcex  =  spex - 1 + numReps
            self.posMap[self.posSpecs[spex].key]  =  posList[sourcex]


# - - -   S y s A r g s . _ _ s c a t t e r O p t i o n a l s   - - -

    def __scatterOptionals ( self, posList ):
        """Allocate positional arguments when some are optional.

          [ if (posList is the list of positional arguments as strings)
            and (self.__optx is not None) ->
              if posList matches self.posSpecs ->
                self.posMap  +:=  entries mapping keys from
                    self.posSpecs |-> corresponding values from
                    posList, or None for missing optional arguments
              else ->
                sys.stderr  +:=  (usage message) + (error message)
                stop execution ]
        """
        #-- 1 --
        # [ if len(posList) < self.__optx ->
        #     sys.stderr  +:=  (usage message) + (error message)
        #     stop execution
        #   else -> I ]
        if  len(posList) < self.__optx:
            usage ( self.switchSpecs, self.posSpecs,
                    "At least %d positional required, %d supplied." %
                    ( self.__optx, len(posList) ) )

        #-- 2 --
        # [ self.posMap  +:=  entries mapping the keys from the first
        #       self.__optx elements of self.posSpecs |-> the 
        #       corresponding elements of self.posList ]
        for  i in range(self.__optx):
            self.posMap[self.posSpecs[i].key]  =  posList[i]

        #-- 3 --
        # [ self.posMap  +:=  entries mapping the keys from
        #       self.posSpecs[self._optx:-1] |-> corresponding
        #       elements of posList, substituting None where
        #       there is no corresponding element ]
        for  i in range(self.__optx, len(self.posSpecs)):
            key  =  self.posSpecs[i].key
            if  i >= len(posList):
                self.posMap[key]  =  None
            else:
                self.posMap[key]  =  posList[i]


# - - -   S y s A r g s . _ _ s c a t t e r R e q u i r e d s   - - -

    def __scatterRequireds ( self, posList ):
        """Allocate positional arguments when all are required.

          [ if (posList is a list of positional arguments as strings)
            and (self.__reqx is None) and (self.__optx is None) ->
              if posList matches self.posSpecs ->
                self.posMap  +:=  entries mapping keys from
                    self.posSpecs |-> corresponding values from posList
              else ->
                sys.stderr  +:=  (usage message) + (error message)
                stop execution ]
        """

        #-- 1 --
        if  len(posList) != len(self.posSpecs):
            usage ( self.switchSpecs, self.posSpecs,
                    "%d positional arguments required, %d supplied." %
                    ( len(self.posSpecs), len(posList) ) )

        #-- 2 --
        # [ self.posMap  +:=  entries mapping keys from
        #       self.posSpecs |-> corresponding values from posList
        for  i in range(len(posList)):
            self.posMap[self.posSpecs[i].key]  =  posList[i]


# - - -   u s a g e   - - -

MESSAGE_PREFIX  =  "***"        # Prefixed to all error lines
DESC_MARGIN     =  12           # Indentation of description parts
WHERE_INDENT    =  2            # Indentation of switches/keys

def usage ( switchSpecs, posSpecs, *textList ):
    "Write a usage message and terminate."

    #-- 1 --
    # [ text  :=  concatenation of elements of textList ]
    text  =  "".join ( textList )

    #-- 2 --
    # [ sys.stderr  +:=  (usage message) ]
    sys.stderr.write ( "%s Usage:\n" % MESSAGE_PREFIX )

    #-- 3 --
    # [ sys.stderr  +:=  command line based on our name in sys.argv[0],
    #                    switchSpecs, and posSpecs ]
    commandModel  =  buildCommandModel ( switchSpecs, posSpecs )
    sys.stderr.write ( "%s    %s %s\n" %
                       ( MESSAGE_PREFIX, sys.argv[0], commandModel ) )

    #-- 4 --
    sys.stderr.write ( "%s where:\n" % MESSAGE_PREFIX )

    #-- 5 --
    # [ sys.stderr  +:=  lines describing the switches in switchSpecs ]
    for  switch in switchSpecs:
        usageSwitch ( switch )

    #-- 6 --
    # [ sys.stderr  +:=  lines describing positionals in posSpecs ]
    for  pos in posSpecs:
        usagePos ( pos )

    #-- 7 --
    sys.stderr.write ( "%s Error: %s\n" % ( MESSAGE_PREFIX, text ) )

    #-- 8 --
    # [ stop execution ]
    sys.exit(1)


# - - -   b u i l d C o m m a n d M o d e l   - - -

def buildCommandModel ( switchSpecs, posSpecs ):
    """Build a model command line for the usage message.

      [ if (switchSpecs is a list of SwitchArg objects)
        and (posSpecs is a list of PosArg objects) ->
          return a string showing the switches and positionals they describe ]
    """

    #-- 1 --
    result  =  []

    #-- 2 --
    # [ result  +:=  strings representing the options in switchSpecs ]
    for  switch in switchSpecs:
        result.append ( "-%s" % switch.letter )

    #-- 3 --
    # [ result  +:=  strings representing the keys in posSpecs ]
    for  pos in posSpecs:
        if  pos.optional:
            result.append ( "[%s]" % pos.key )
        else:
            result.append ( pos.key )
            if  pos.repeated:
                result.append ( "..." )

    #-- 4 --
    # [ return the concatenation of the strings in result with single
    #   spaces between them ]
    return " ".join ( result )


# - - -   u s a g e S w i t c h   - - -

def usageSwitch ( switch ):
    """Display a SwitchArg

      [ if switch is a SwitchArg object ->
          sys.stderr  +:=  lines describing switch ]
    """

    #-- 1 --
    # [ prefix  :=  switch.letter left-justified in a field of size
    #               DESC_MARGIN ]
    prefix  =  ( "%s%-*s" %
                 ( " "*WHERE_INDENT, DESC_MARGIN, "-%s" % switch.letter ) )

    #-- 2 --
    # [ sys.stderr  +:=  (prefix + switch.description[0] + "\n") +
    #       (lines from switch.description[1:], each prefixed
    #       with DESC_MARGIN spaces) ]
    for line in switch.description:
        sys.stderr.write ( "%s %s %s\n" % ( MESSAGE_PREFIX, prefix, line ) )
        prefix  =  ( "%s" % ( " "*(WHERE_INDENT + DESC_MARGIN) ) )


# - - -   u s a g e P o s   - - -

def usagePos ( pos ):
    """Display a PosArg

      [ if pos is a PosArg object ->
          sys.stderr  +:=  lines describing pos ]
    """

    #-- 1 --
    # [ prefix       :=  pos.key left-justified in a field of size DESC_MARGIN
    #   linesLeft    :=  copy of pos.description list
    #   blankMargin  :=  string of DESC_MARGIN blanks ]
    prefix       =  "%s%-*s" % ( " "*WHERE_INDENT, DESC_MARGIN, pos.key )
    linesLeft    =  pos.description[:]
    blankMargin  =  " " * DESC_MARGIN

    #-- 2 --
    # [ if len(pos.key) >= (DESC_MARGIN-1) ->
    #     sys.stderr  +:=  (prefix + "\n") +
    #         (lines of linesLeft each followed by "\n")
    #   else ->
    #     sys.stderr  +:=  (prefix + pos.description[0] + "\n") +
    #         (lines of linesLeft[1:], each preceded by blankMargin
    #         and followed by "\n") ]
    if  len(pos.key) >= (DESC_MARGIN - 1):
        print "%s %s" % ( MESSAGE_PREFIX, prefix )
    else:
        print "%s %s %s" % ( MESSAGE_PREFIX, prefix, linesLeft[0] )
        del linesLeft[0]

    for line in linesLeft:
        print ( "%s %s%s %s" %
                ( MESSAGE_PREFIX, " "*WHERE_INDENT, blankMargin, line ) )


# - - - - -   c l a s s   S w i t c h A r g   - - - - -

class SwitchArg:
    "Represents the specification for a valid switch argument."
    def __init__ ( self, letter, description, takesValue=0 ):
        "Constructor for SwitchArg"
        self.letter       =  letter
        self.description  =  description
        self.takesValue   =  takesValue



# - - - - -   c l a s s   P o s A r g   - - - - -

class PosArg:
    "Represents the specification for a valid positional argument."
    def __init__ ( self, key, description, optional=0, repeated=0 ):
        "Constructor for PosArg"
        self.key          =  key
        self.description  =  description
        self.optional     =  optional
        self.repeated     =  repeated
