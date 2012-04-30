"""latlonentry.py:  A Tkinter widget for entering lat/lon coordinates.
"""

LAT_LON_ENTRY_REVISION  =  "$Revision: 1.9 $"
LAT_LON_ENTRY_DATE      =  "$Date: 2004/02/18 18:59:33 $"
LAT_LON_ENTRY_VERSION   =  "0.0"

#================================================================
# Exports
#----------------------------------------------------------------
# class LatLonEntry(Frame):  An entry widget for lat-lon coordinates.
#   LatLonEntry ( master=None ):
#     [ master is a Frame, defaulting to a new root window ->
#         master  :=  master with a new LatLonEntry widget added but
#                     not gridded
#         return that widget ]
#   .get():
#     [ if the fields contain a valid coordinate set ->
#         return a LatLon object representing those fields
#       else ->
#         <screen>  :=  <screen> with a pop-up describing the problem
#         raise ValueError ]
#   .setDeg(terraPos):
#     [ terraPos is a TerraPosition object ->
#         self  :=  self displaying terraPos as decimal degrees ]
#   .setDegMin(terraPos):
#     [ terraPos is a TerraPosition object ->
#         self  :=  self displaying terraPos as whole degrees
#                   and decimal minutes ]
#   .setDMS(terraPos):
#     [ terraPos is a TerraPosition object ->
#         self  :=  self displaying terraPos as whole degrees and minutes
#                   and decimal seconds ]
#   .set(latLon):
#     [ latLon is a LatLon object (NOTE: *Not* a TerraPosition!) ->
#         self  :=  self displaying latLon in its original units ]
#   .clear():
#     [ self  :=  self with all fields cleared ]
#----------------------------------------------------------------


#================================================================
# Imports
#----------------------------------------------------------------

#--
# From standard Python libraries
#--

from Tkinter import *       # Tkinter widgets
from Dialog import *        # Popup Tk dialogs
import tkFont               # Tkinter fonts


#--
# Modules from the python/mapping directory
#--

import terrapos             # TerraPosition and LatLon objects


#--
# Modules from Shipman's Tkinter library
#--

import dropdown             # DropDown object


#================================================================
# Manifest constants
#----------------------------------------------------------------

#--
# Choice lists for N/S and E/W drop-down menus (first is the default):
#   N_S_CHOICES:  Latitude north or south.
#   E_W_CHOICES:  Longitude east or west.
#   DATUM_CHOICES:  Map datum values we support.
#--

N_S_CHOICES     =  ["N", "S"]
N_CHOICE  =  0                  # Index of "N"...
S_CHOICE  =  1                  # ...and "S" in N_S_CHOICES
E_W_CHOICES     =  ["W", "E"]
W_CHOICE  =  0                  # Index of "W"...
E_CHOICE  =  1                  # ...and "E" in E_W_CHOICES
DATUM_CHOICES   =  ["WGS-84", "NAD-27"]


#--
# Tkinter appearance features.  DEGREE_FONT is for a degree symbol as a
# tiny letter "o".
#--

LABEL_FONT   =  {"family": "Helvetica", "size": 12}
LABEL_COLOR  =  "DodgerBlue"        # A medium blue
DEGREE_FONT  =  {"family": "Helvetica", "size": 8}
ENTRY_FONT   =  {"family": "lucidatypewriter", "size": 12, "weight":  "bold"}
ENTRY_COLOR  =  "#008800"           # A medium green
ENTRY_BG     =  "#dddddd"           # A light gray



# - - -   e r r o r P a n e l   - - -

def errorPanel ( * L ):
    """Pop up an error panel, wait for a mouse click, then return.

      [ (we can pop up new windows) and
        (L is a list of strings) ->
          <screen>  :=  <screen> with a new popup displaying the
                concatenation of the elements of L, with a `dismiss'
                button ]
    """

    #-- 1 --
    # [ message  :=  concatenation of elements of L ]
    message  =  "".join(L)

    #-- 2 --
    # [ we can pop up new windows ->
    #     <screen>  :=  <screen> with a new popup displaying message,
    #                   with a `dismiss' button ]
    d  =  Dialog ( title="Message", bitmap="info",
                   text=message,
                   default=0,   # First button is the default
                   strings = ("OK",) )    # Only one button: OK



# - - - - -   c l a s s   L a t L o n E n t r y   - - - - -

class LatLonEntry(Frame):
    """Lat-long coordinate entry widget

      Widget grid plan:

         0               1             2
        +---------------+-------------+--------------+
      0 | .__latLabel   | .__latGroup | .__nsMenu    |
        +---------------+-------------+--------------+
      1 | .__lonLabel   | .__lonGroup | .__ewMenu    |
        +---------------+-------------+--------------+
      2 | .__datumLabel | .__datumMenu               |
        +---------------+-------------+--------------+

      Key:
        .__latLabel     Label "Lat:"
        .__latGroup     AngleEntry widget for deg/min/sec latitude
        .__nsMenu       DropDown menu for north/south latitude
        .__lonLabel     Label "Lon:"        
        .__lonGroup     AngleEntry widget for deg/min/sec longitude
        .__ewMenu       DropDown menu for east/west longitude
        .__datumLabel   Label "Map datum"
        .__datumMenu    DropDown menu for map datum

      State/Invariants:
        .__nsVar:  StringVar for .__nsMenu
        .__ewVar:  StringVar for .__ewMenu
        .__datumVar:  StringVar for .__datumMenu        
        .__labelFont:  Font for all labels
    """


# - - -   L a t L o n E n t r y . _ _ i n i t _ _   - - -

    def __init__ ( self, master=None ):
        "Constructor for LatLonEntry"

        #-- 1 --
        # [ master  :=  master with a new Frame object added un gridded
        #   self    :=  that Frame ]
        Frame.__init__ ( self, master )

        #-- 2 --
        # [ self  :=  self with all internal widgets created ]
        self.__createWidgets ( )


# - - -   L a t L o n E n t r y . _ _ c r e a t e W i d g e t s   - - -

    def __createWidgets ( self ):
        "Create all internal widgets in self"

        #-- 1 --
        # [ self.__labelFont  :=  as invariant
        #   self.__entryFont  :=  as invariant
        #   self.__degreeFont  :=  as invariant ]
        self.__labelFont  =  tkFont.Font ( ** LABEL_FONT )
        self.__entryFont  =  tkFont.Font ( ** ENTRY_FONT )
        self.__degreeFont  =  tkFont.Font ( ** DEGREE_FONT )

        #-- 2 --
        # [ self  :=  self with all latitude-related widgets added ]
        self.__createLatRow ( 0 )

        #-- 3 --
        # [ self  :=  self with all longitude-related widgets added ]
        self.__createLonRow ( 1 )

        #-- 4 --
        # [ self  :=  self with all map datum widgets added ]
        self.__createDatumRow ( 2 )


# - - -   L a t L o n E n t r y . _ _ c r e a t e L a t R o w   - - -

    def __createLatRow ( self, rowx ):
        """Create the row for entry of latitude.

          [ (self has all fonts defined) and (rowx >= 0) ->
              self  :=  self with .__latLabel, .__latGroup, and
                        .__nsMenu added and gridded in row=rowx ]
        """

        #-- 1 --
        # [ self.__latLabel  :=  as invariant ]
        self.__latLabel  =  Label ( self,
            anchor=NW, font=self.__labelFont, fg=LABEL_COLOR,
            text="Lat:" )
        colx  =  0
        self.__latLabel.grid ( row=rowx, column=colx, ipadx=2,
            sticky=W )

        #-- 2 --
        # [ self.__latGroup  :=  as invariant ]
        self.__latGroup  =  AngleEntry ( self )
        colx  =  colx + 1
        self.__latGroup.grid ( row=rowx, column=colx, sticky=E )

        #-- 3 --
        # [ self.__nsVar   :=  as invariant
        #   self.__nsMenu  :=  as invariant ]
        self.__nsVar   =  StringVar()
        self.__nsMenu  =  dropdown.DropDown ( self,
            self.__nsVar, N_S_CHOICES )
        colx  =  colx + 1
        self.__nsMenu.grid ( row=rowx, column=colx, sticky=W )


# - - -   L a t L o n E n t r y . _ _ c r e a t e L o n R o w   - - -

    def __createLonRow ( self, rowx ):
        """Create the for entry of longitude.

          [ (self has all fonts defined) and (rowx >= 0) ->
              self  :=  self with .__lonLabel, .__lonGroup, and
                        .__ewMenu added and gridded in row=rowx ]
        """

        #-- 1 --
        # [ self.__lonLabel  :=  as invariant ]
        self.__lonLabel  =  Label ( self,
            anchor=NW, font=self.__labelFont, fg=LABEL_COLOR,
            text="Lon:" )
        colx  =  0
        self.__lonLabel.grid ( row=rowx, column=colx, ipadx=2,
            sticky=W )

        #-- 2 --
        # [ self.__lonGroup  :=  as invariant ]
        self.__lonGroup  =  AngleEntry ( self )
        colx  =  colx + 1
        self.__lonGroup.grid ( row=rowx, column=colx, sticky=E )

        #-- 3 --
        # [ self.__ewVar   :=  as invariant
        #   self.__ewMenu  :=  as invariant ]
        self.__ewVar   =  StringVar()
        self.__ewMenu  =  dropdown.DropDown ( self,
            self.__ewVar, E_W_CHOICES )
        colx  =  colx + 1
        self.__ewMenu.grid ( row=rowx, column=colx, sticky=W )


# - - -   L a t L o n E n t r y . _ _ c r e a t e D a t u m R o w   - - -

    def __createDatumRow ( self, rowx ):
        """Create the widgets for setting the map datum code.

          [ self has all fonts set up ->
              self  :=  self with .__datumLabel and .__datumMenu gridded
                        and .__datumVar slaved to .__datumMenu ]
        """

        #-- 1 --
        # [ self.__datumLabel  :=  as invariant ]
        self.__datumLabel  =  Label ( self,
            anchor=E, font=self.__labelFont, fg=LABEL_COLOR,
            text="Datum:" )
        colx  =  0
        self.__datumLabel.grid ( row=rowx, column=colx, sticky=E )

        #-- 2 --
        # [ self.__datumMenu  :=  as invariant ]
        self.__datumVar   =  StringVar()
        self.__datumMenu  =  dropdown.DropDown ( self,
            self.__datumVar, DATUM_CHOICES )
        colx  =  colx + 1
        self.__datumMenu.grid ( row=rowx, column=colx,
            columnspan=2, sticky=W )


# - - -   L a t L o n E n t r y . g e t   - - -

    def get ( self ):
        "Retrieve self's value as a terrapos.LatLon object."

        #-- 1 --
        # [ latNS     :=  self.__nsMenu's string
        #   lonEW     :=  self.__ewMenu's string
        #   mapDatum  :=  self.__datumMenu's string ]
        latNS       =  N_S_CHOICES [ self.__nsMenu.get() ]
        lonEW       =  E_W_CHOICES [ self.__ewMenu.get() ]
        mapDatum    =  DATUM_CHOICES [ self.__datumMenu.get() ]

        #-- 2 --
        # [ if self.__latGroup is a valid angle ->
        #     latAngle  :=  that angle as a DegVariant.value, with sign
        #                   determined by latNS
        #   else ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError ]
        latAngle  =  self.__latGroup.get().value
        if  latNS == "S":
            latAngle  =  [ -x for x in latAngle ]

        #-- 3 --
        # [ if self.__lonGroup is a valid angle ->
        #     lonAngle  :=  that angle as a DegVariant.value, with sign
        #                   determined by lonEW
        #   else ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError ]
        lonAngle  =  self.__lonGroup.get().value
        if  lonEW == "W":
            lonAngle  =  [ -x for x in lonAngle ]

        #-- 4 --
        return terrapos.LatLon ( latAngle, lonAngle, datumName=mapDatum )


# - - -   L a t L o n E n t r y . s e t D e g   - - -

    def setDeg ( self, terraPos ):
        "Set self in degrees with decimal."

        #-- 1 --
        # [ self.__nsMenu  :=  self.__nsMenu showing "N" or "S"
        #       depending on the sign of terraPos.latDeg
        #   self.__ewMenu  :=  self.__ewMenu showing "E" or "W"
        #       depending on the sign of terraPos.lonDeg ]
        self.__setSigns ( terraPos )

        #-- 2 --
        # [ self.__latGroup  :=  self.__latGroup showing
        #       abs(terraPos.degLat) as degrees
        #   self.__lonGroup  :=  self.__lonGroup showing
        #       abs(terraPos.degLon) as degrees ]
        self.__latGroup.set ( terrapos.DegVariant (
            abs ( terraPos.latDeg ) ) )
        self.__lonGroup.set ( terrapos.DegVariant (
            abs ( terraPos.lonDeg ) ) )


# - - -   L a t L o n E n t r y . _ _ s e t S i g n s   - - -

    def __setSigns ( self, terraPos ):
        """Set latitude N/S and longitude E/W indicators from terraPos

          [ terraPos is a TerraPosition object ->
              self.__nsMenu  :=  self.__nsMenu showing "N" or "S"
                  depending on the sign of terraPos.latDeg
              self.__ewMenu  :=  self.__ewMenu showing "E" or "W"
                  depending on the sign of terraPos.lonDeg ]
        """

        #-- 1 --
        # [ if terraPos.latDeg < 0 ->
        #     self.__nsMenu  :=  self.__nsMenu showing "S"
        #   else ->
        #     self.__nsMenu  :=  self.__nsMenu showing "N" ]
        if  terraPos.latDeg < 0:
            self.__nsMenu.set ( S_CHOICE )
        else:
            self.__nsMenu.set ( N_CHOICE )

        #-- 2 --
        # [ if terraPos.lonDeg < 0 ->
        #     self.__ewMenu  :=  self.__ewMenu showing "W"
        #   else ->
        #     self.__ewMenu  :=  self.__ewMenu showing "E" ]
        if  terraPos.lonDeg < 0:
            self.__ewMenu.set ( W_CHOICE )
        else:
            self.__ewMenu.set ( E_CHOICE )


# - - -   L a t L o n E n t r y . s e t D e g M i n  - - -

    def setDegMin ( self, terraPos ):
        "Set self in whole degrees, and minutes with decimal."

        #-- 1 --
        # [ self.__nsMenu  :=  self.__nsMenu showing "N" or "S"
        #       depending on the sign of terraPos.latDeg
        #   self.__ewMenu  :=  self.__ewMenu showing "E" or "W"
        #       depending on the sign of terraPos.lonDeg ]
        self.__setSigns ( terraPos )

        #-- 2 --
        # [ self.__latGroup  :=  self.__latGroup showing
        #       abs(terraPos.degLat) as degrees and minutes
        #   self.__lonGroup  :=  self.__lonGroup showing
        #       abs(terraPos.degLon) as degrees and minutes ]
        latD, latM  =  divmod ( terraPos.latDeg, 60.0 )
        self.__latGroup.set ( terrapos.DegVariant ( ( int(latD), latM ) ) )
        lonD, lonM  =  divmod ( terraPos.lonDeg, 60.0 )
        self.__lonGroup.set ( terrapos.DegVariant ( ( int(lonD), lonM ) ) )


# - - -   L a t L o n E n t r y . s e t D M S   - - -

    def setDMS ( self, terraPos ):
        "Set self in degrees/minutes/seconds."

        #-- 1 --
        # [ self.__nsMenu  :=  self.__nsMenu showing "N" or "S"
        #       depending on the sign of terraPos.latDeg
        #   self.__ewMenu  :=  self.__ewMenu showing "E" or "W"
        #       depending on the sign of terraPos.lonDeg ]
        self.__setSigns ( terraPos )

        #-- 2 --
        # [ self.__latGroup  :=  self.__latGroup showing
        #       abs(terraPos.degLat) as degrees/minutes/seconds
        #   self.__lonGroup  :=  self.__lonGroup showing
        #       abs(terraPos.degLon) as degrees and minutes ]
        self.__latGroup.set ( terrapos.DegVariant (
            terrapos.degDMSfuzz ( abs ( terraPos.latDeg ), terrapos.F_SEC ) ) )
        self.__lonGroup.set ( terrapos.DegVariant (
            terrapos.degDMSfuzz ( abs ( terraPos.lonDeg ), terrapos.F_SEC ) ) )


# - - -   L a t L o n E n t r y . s e t   - - -

    def set ( self, latLon ):
        "Display the given value."

        #-- 1 --
        # [ self.__nsMenu  :=  self.__nsMenu showing "N" or "S"
        #       depending on the sign of terraPos.latDeg
        #   self.__ewMenu  :=  self.__ewMenu showing "E" or "W"
        #       depending on the sign of terraPos.lonDeg ]
        self.__setSigns ( latLon )

        #-- 2 --
        # [ self.__latGroup  :=  self.__latGroup showing latLon.lat
        #   self.__lonGroup  :=  self.__lonGroup showing latLon.lon ]
        self.__latGroup.set ( latLon.latVar )
        self.__lonGroup.set ( latLon.lonVar )


# - - -   L a t L o n E n t r y . c l e a r   - - -

    def clear ( self ):
        "Clear all self's text entries."
        self.__latGroup.clear()
        self.__lonGroup.clear()



# - - - - -   c l a s s   A n g l e E n t r y   - - - - -

class AngleEntry(Frame):
    """A Tkinter widget allowing entry of an angle in deg/min/sec

      Exports:
        AngleEntry ( master=None ):
          [ master is a Frame ->
              master  :=  master with a new AngleEntry widget added
                  but not gridded ]
        .get():
          [ if the fields contain a valid coordinate set ->
             return a DegVariant representing those fields
           else ->
             <screen>  :=  <screen> with a pop-up describing the error
             raise ValueError ]
        .set(degVariant):
          [ degVariant is a DegVariant object ->
              self  :=  self with degVariant displayed ]
        .clear():
          [ self  :=  self with all text entries cleared ]

      Widget grid plan:
         0    1    2    3    4    5
        +----+----+----+----+----+----+
        | DE | DL | ME | ML | SE | SL |
        +----+----+----+----+----+----+

      Key:
        DE  .__degEntry:  Entry widget for degrees
        DL  .__degLabel:  Label for degrees
        ME  .__minEntry:  Entry widget for minutes
        ML  .__minLabel:  Label for minutes
        SE  .__secEntry:  Entry widget for seconds
        SL  .__secLabel:  Label for seconds

      State/Invariants:
        .__degVar:      [ a StringVar for .__degEntry ]
        .__minVar:      [ a StringVar for .__minEntry ]
        .__secVar:      [ a StringVar for .__secEntry ]
        .__labelFont:   [ LABEL_FONT as a Font ]
        .__entryFont:   [ ENTRY_FONT as a Font ]
        .__degreeFont:  [ DEGREE_FONT as a Font ]
    """
    

# - - -   A n g l e E n t r y . _ _ i n i t _ _   - - -

    def __init__ ( self, master=None ):
        "Constructor for AngleEntry"

        #-- 1 --
        # [ master  :=  master with a new Frame object added ungridded
        #   self    :=  that Frame ]
        Frame.__init__ ( self, master )
        
        #-- 2 --
        # [ self.__labelFont   :=  as invariant
        #   self.__degreeFont  :=  as invariant
        #   self.__degVar      :=  a new StringVar
        #   self.__minVar      :=  a new StringVar
        #   self.__secVar      :=  a new StringVar ]
        self.__labelFont   =  tkFont.Font ( ** LABEL_FONT )
        self.__entryFont   =  tkFont.Font ( ** ENTRY_FONT )
        self.__degreeFont  =  tkFont.Font ( ** DEGREE_FONT )
        self.__degVar      =  StringVar()
        self.__minVar      =  StringVar()
        self.__secVar      =  StringVar()

        #-- 3 --
        # [ self  :=  self with a new Entry widget for self.__degVar ]
        # [ self.__degEntry  :=  that widget ]
        self.__degEntry  =  Entry ( self,
            font=self.__entryFont, fg=ENTRY_COLOR, bg=ENTRY_BG,
            width=terrapos.L_DEG,
            textvariable=self.__degVar )
        rowx  =  0
        colx  =  0
        self.__degEntry.grid ( row=rowx, column=colx, sticky=E )

        #-- 3 --
        # [ self  :=  self + (a Label for degrees)
        #   self.__degLabel  :=  that Label ]
        self.__degLabel  =  Label ( self,
            anchor=NW, font=self.__degreeFont, fg=LABEL_COLOR,
            text="o" )
        colx  =  colx + 1
        self.__degLabel.grid ( row=rowx, column=colx, sticky=NW )

        #-- 4 --
        # [ self  :=  self with a new Entry widget for self.__minVar
        #   self.__minEntry  :=  that Entry ]
        self.__minEntry  =  Entry ( self,
            font=self.__entryFont, fg=ENTRY_COLOR, bg=ENTRY_BG,
            width=terrapos.L_MIN,
            textvariable=self.__minVar )
        colx  =  colx + 1
        self.__minEntry.grid ( row=rowx, column=colx, sticky=E )

        #-- 5 --
        # [ self  :=  self + (a Label for minutes)
        #   self.__minLabel  :=  that Label ]
        self.__minLabel  =  Label ( self,
            anchor=NW, font=self.__labelFont, fg=LABEL_COLOR,
            text="'" )
        colx  =  colx + 1
        self.__minLabel.grid ( row=rowx, column=colx, sticky=NW )

        #-- 6 --
        # [ self  :=  self with a new Entry widget for self.__secVar
        #   self.__secEntry  :=  that Entry ]
        self.__secEntry  =  Entry ( self,
            font=self.__entryFont, fg=ENTRY_COLOR, bg=ENTRY_BG,
            width=terrapos.L_SEC,
            textvariable=self.__secVar )
        colx  =  colx + 1
        self.__secEntry.grid ( row=rowx, column=colx, sticky=E )

        #-- 7 --
        # [ self  :=  self + (a Label for seconds)
        #   self.__secLabel  :=  that Label ]
        self.__secLabel  =  Label ( self,
            anchor=NW, font=self.__labelFont, fg=LABEL_COLOR,
            text='"' )
        colx  =  colx + 1
        self.__secLabel.grid ( row=rowx, column=colx, sticky=NW )


# - - -   A n g l e E n t r y . g e t   - - -

    def get ( self ):
        "Return a DegVariant if valid, otherwise popup and raise ValueError"

        #-- 1 --
        # [ if self.__degEntry is a valid integer degrees ->
        #     degValue  :=  int(self.__degEntry)
        #   else if self.__degEntry is a valid float degrees ->
        #     degValue  :=  float(self.__degEntry)
        #   else ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError ]
        degValue  =  self.__checkDeg()

        #-- 2 --
        # [ if (self.__minEntry is a valid integer minutes) and
        #   (degValue is an int) ->
        #     minValue  :=  int(self.__minEntry)
        #   else if (self.__minEntry is a valid float) and
        #   (degValue is an int) ->
        #     minValue  :=  float(self.__minEntry)
        #   else if (self.__minEntry is empty) ->
        #     minValue  :=  None
        #   else ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError ]
        minValue  =  self.__checkMin(degValue)

        #-- 3 --
        # [ if (self.__secEntry is empty) ->
        #     secValue  :=  None
        #   else if (self.__secEntry is a valid integer seconds) and
        #   (minValue is not None) ->
        #     secValue  :=  int(self.__secEntry)
        #   else if (self.__secEntry is a valid float seconds) and
        #   (minValue is not None) ->
        #     secValue  :=  float(self.__secEntry)
        #   else ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError ]
        secValue  =  self.__checkSec(minValue)

        #-- 4 --
        # [ return a DegVariant made from degValue, minValue, and secValue ]
        if  minValue is None:
            return terrapos.DegVariant(degValue)
        elif  secValue is None:
            return terrapos.DegVariant((degValue, minValue))
        else:
            return terrapos.DegVariant((degValue, minValue, secValue))


# - - -   A n g l e E n t r y . _ _ c h e c k D e g   - - -

    def __checkDeg ( self ):
        """Validate the degrees field

          [ if self.__degEntry is a valid integer degrees ->
              return int(self.__degEntry)
            else if self.__degEntry is a valid float degrees ->
              return float(self.__degEntry)
            else ->
              <screen>  :=  <screen> with a pop-up describing the error
              raise ValueError ]          
        """

        #-- 1 --
        # [ raw  :=  self.__degEntry's contents ]
        raw  =  self.__degVar.get().strip()

        #-- 2 --
        # [ if raw is a valid int ->
        #     result  :=  raw as an int
        #   else if raw is a valid float ->
        #     result  :=  raw as a float
        #   else ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError ]          
        try:
            result  =  int ( raw )
        except ValueError:
            try:
                result  =  float ( raw )
            except ValueError:
                message  =  "Degrees value is not a valid number: `%s'" % raw
                errorPanel ( message )
                raise ValueError, message

        #-- 3 --
        # [ if ( ( result < 0 ) or ( result > 360 ) ) ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError
        #   else ->
        #     return result ]
        if  not ( 0.0 <= result < 360.0 ):
            message  =  ( "Degrees value must be positive and less "
                          "than 360: `%s'" % result )
            errorPanel ( message )
            raise ValueError, message
        else:
            return result


# - - -   A n g l e E n t r y . _ _ c h e c k M i n   - - -

    def __checkMin ( self, degValue ):
        """Validate the minutes field.

          [ if (self.__minEntry is a valid integer minutes) and
            (degValue is an int) ->
              return int(self.__minEntry)
            else if (self.__minEntry is a valid float) and
            (degValue is an int) ->
              return float(self.__minEntry)
            else if (self.__minEntry is empty) ->
              return None
            else ->
              <screen>  :=  <screen> with a pop-up describing the error
              raise ValueError ]
        """

        #-- 1 --
        # [ raw  :=  self.__minEntry's contents, deblanked ]
        raw  =  self.__minVar.get().strip()

        #-- 2 --
        # [ if raw is empty ->
        #     return None
        #   else -> I ]
        if  len(raw) == 0:
            return None

        #-- 3 --
        # [ if type(degValue) is float ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError
        #   else -> I ]
        if  type(degValue) is float:
            message  =  ( "Degrees must be an integer when using the "
                          "minutes field." )
            errorPanel ( message )
            raise ValueError, message

        #-- 4 --
        # [ if raw is a valid int ->
        #     result  :=  int(raw)
        #   else if raw is a valid float ->
        #     result  :=  float(raw)
        #   else ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError ]          
        try:
            result  =  int(raw)
        except ValueError:
            try:
                result  =  float(raw)
            except ValueError:
                message  =  ( "Minutes value is not a valid number: "
                              "`%s'" % raw )
                errorPanel ( message )
                raise ValueError, message

        #-- 4 --
        # [ if ( ( result < 0 ) or ( result >= 60 ) ) ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError
        #   else ->
        #     return result ]
        if  not ( 0.0 <= result < 60.0 ):
            message  =  ( "Minutes value must be nonnegative and less "
                          "than 60: `%s'" % result )
            errorPanel ( message )
            raise ValueError, message
        else:
            return result


# - - -   A n g l e E n t r y . _ _ c h e c k S e c   - - -

    def __checkSec ( self, minValue ):
        """Validate the seconds field.

          [ if (self.__secEntry is a valid integer seconds) and
            (minValue is an int) ->
              return int(self.__secEntry)
            else if (self.__secEntry is a valid float) and
            (minValue is an int) ->
              return float(self.__secEntry)
            else if (self.__secEntry is empty) ->
              return None
            else ->
              <screen>  :=  <screen> with a pop-up describing the error
              raise ValueError ]
        """

        #-- 1 --
        # [ raw  :=  self.__secEntry's contents, deblanked ]
        raw  =  self.__secVar.get().strip()

        #-- 2 --
        # [ if raw is empty ->
        #     return None
        #   else -> I ]
        if  len(raw) == 0:
            return None

        #-- 3 --
        # [ if type(minValue) is float ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError
        #   else -> I ]
        if  type(minValue) is float:
            message  =  ( "Minutes must be an integer when using the "
                          "seconds field." )
            errorPanel ( message )
            raise ValueError, message

        #-- 4 --
        # [ if raw is a valid int ->
        #     result  :=  int(raw)
        #   else if raw is a valid float ->
        #     result  :=  float(raw)
        #   else ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError ]          
        try:
            result  =  int(raw)
        except ValueError:
            try:
                result  =  float(raw)
            except ValueError:
                message  =  ( "Seconds value is not a valid number: "
                              "`%s'" % raw )
                errorPanel ( message )
                raise ValueError, message

        #-- 4 --
        # [ if ( ( result < 0 ) or ( result >= 60 ) ) ->
        #     <screen>  :=  <screen> with a pop-up describing the error
        #     raise ValueError
        #   else ->
        #     return result ]
        if  not ( 0.0 <= result < 60.0 ):
            message  =  ( "Seconds value must be nonnegative and less "
                          "than 60: `%s'" % result )
            errorPanel ( message )
            raise ValueError, message
        else:
            return result


# - - -   A n g l e E n t r y . s e t   - - -

    def set ( self, degVariant ):
        "Display degVariant in self."

        #-- 1 --
        # [ if degVariant.min is None ->
        #     self  :=  self as decimal degrees with length L_DEG
        #               and precision F_DEG
        #     return
        #   else -> I ]
        if  degVariant.min is None:
            degValue  =  "%*.*f" % (terrapos.L_DEG, terrapos.F_DEG,
                                    degVariant.deg)
            self.__degVar.set ( degValue )
            self.__minVar.set ( "" )
            self.__secVar.set ( "" )
            return

        #-- 2 --
        # [ if degVariant.sec is None ->
        #     self  :=  self as integer degrees, and minutes with
        #               length L_MIN and precision F_MIN
        #     return
        #   else -> I ]
        if  degVariant.sec is None:
            degValue  =  "%d" % degVariant.deg
            minValue  =  "%0*.*f" % (terrapos.L_MIN, terrapos.F_MIN,
                                     degVariant.min)
            self.__degVar.set ( degValue )
            self.__minVar.set ( minValue )
            self.__secVar.set ( "" )
            return

        #-- 3 --
        # [ self  :=  self as integer degrees, integer minutes, and
        #             seconds with length L_SEC and precision F_SEC ]
        degValue  =  "%d" % degVariant.deg
        minValue  =  "%02d" % degVariant.min
        secValue  =  "%*.*f" % (terrapos.L_SEC, terrapos.F_SEC,
                                degVariant.sec)
        self.__degVar.set ( degValue )
        self.__minVar.set ( minValue )
        self.__secVar.set ( secValue )


# - - -   A n g l e E n t r y . c l e a r   - - -

    def clear ( self ):
        "Clear all self's text entries."
        self.__degVar.set ( "" )
        self.__minVar.set ( "" )
        self.__secVar.set ( "" )
