"""mapframe.py:  Tkinter widget to display maps.
        $Revision: 1.20 $  $Date: 2005/07/07 23:15:54 $

================================================================
  Exports:
----------------------------------------------------------------
    class MapFrame(Frame):      Widget to display a map.
        MapFrame(master, latLonBox, mapBase, magCode, tileKind,
                 canvasSize=None):
          [ (master is a Frame) and
            (latLonBox defines the terrestrial area to be displayed
            as a TerraBox object) and
            (mapBase is a map base as a MapBase object) and
            (magCode is a magnification as a mag-code) and
            (kind is a tile-kind) and
            (canvasSize is a (width,height) tuple for the actual screen
            dimensions of the canvas, defaulting to (CANVAS_WIDE,
            CANVAS_HIGH) ->
              master  :=  master with a new MapFrame added ungridded
                that displays any tiles from that map base that
                are at least partially inside latLonBox
              return that MapFrame object
            else -> raise ValueError ]
        .latLonBox:     [ as passed to constructor, read-only ]
        .mapBase:       [ as passed to constructor, read-only ]
        .magCode:       [ as passed to constructor, read-only ]
        .tileKind:      [ as passed to constructor, read-only ]
        .canvasSize:
            [ as passed to constructor, with defaulting, read-only ]
        .magBox:
          [ a MagBox object representing the map image built
            up from self.mapBase cropped using self.latLonBox ]
        .scrollCan:
            [ a ScrolledCanvas widget displaying self's map ]
        .can:
            [ the canvas from self.canScroll ]
        .displayToLatLon(xy):
          [ xy is an image location as a 2-sequence (x,y) ->
              if xy lies inside one of self's tiles ->
                return a TerraPosition object representing the corresponding
                terrestrial location
              else -> raise ValueError ]
        .latLonToDisplay(latLon):
          [ latLon is a TerraPosition object ->
              if latLon lies inside one of self's tiles ->
                return the corresponding image coordinate as an (x,y) tuple
              else -> raise ValueError ]
"""


#================================================================
# Imports
#----------------------------------------------------------------

#--
# Standard Python library modules
#--

from Tkinter import *       # Tkinter graphical user interface
import Image as PIL         # Python Imaging Library
import ImageTk              # PIL <-> Tkinter adapter

#--
# Modules from Shipman's Python library
#--

import canscroll            # ScrolledCanvas widget

#--
# Modules specific to this application
#--

import terrapos             # Earth position objects: TerraPosition, LatLon
from mapbase import *       # Map tile storage and retrieval


#================================================================
# Manifest constants
#----------------------------------------------------------------

CANVAS_WIDE  =  900         # Size of canvas by default: width...
CANVAS_HIGH  =  550         # ...and height


# - - - - -   c l a s s   M a p F r a m e   - - - - -

class MapFrame(Frame):
    """Earth mapping widget.

      State/Invariants:
        .photoImage:
          [ an ImageTk.PhotoImage object containing the actual
            map image ]
              ** NOTE: **  Reference counts are not correctly
              incremented for PhotoImage objects.  Hence, we
              absolutely must keep some variable bound to this
              object or it will be garbage-collected and the
              image will mysteriously disappear.  Yes, this is
              a KLUGE.
    """

# - - -   M a p F r a m e . d i s p l a y T o L a t L o n   - - -

    def displayToLatLon ( self, xy ):
        "Convert an image location to the corresponding lat-lon."
        return self.magBox.displayToLatLon ( xy )


# - - -   M a p F r a m e . l a t L o n T o D i s p l a y   - - -

    def latLonToDisplay ( self, latLon ):
        "Find the image coordinate closest to a given lat-lon."
        return self.magBox.latLonToDisplay ( latLon )


# - - -   M a p F r a m e . _ _ i n i t _ _   - - -

    def __init__ ( self, master, latLonBox, mapBase, magCode,
                   tileKind, canvasSize=None ):
        "Constructor for MapFrame."

        #-- 1 --
        # [ self.latLonBox   :=  as invariant
        #   self.mapBase     :=  as invariant
        #   self.magCode     :=  as invariant
        #   self.tileKind    :=  as invariant
        #   self.canvasSize  :=  as invariant ]
        self.latLonBox  =  latLonBox
        self.mapBase    =  mapBase
        self.magCode    =  magCode
        self.tileKind   =  tileKind
        if  canvasSize is None:
            self.canvasSize  =  (CANVAS_WIDE, CANVAS_HIGH)
        else:
            self.canvasSize  =  canvasSize

        #-- 2 --
        # [ master  :=  master with a new Frame added
        #   self    :=  that Frame ]
        Frame.__init__ ( self, master )

        #-- 3 --
        # [ if (self.mapBase names a map base that has at least one
        #   defined slot overlapping self.latLonbox) ->
        #     self  :=  self with a ScrolledCanvas added, displaying
        #               any tiles from self.MapBase that overlap
        #               self.latLonBox
        #  else -> raise ValueError ]
        self.__createWidgets ( )


# - - -   M a p F r a m e . _ _ c r e a t e W i d g e t s   - - -

    def __createWidgets ( self ):
        """Create all self's contained widgets.

          [ (self is a Frame) and
            (self.latLonBox is as invariant) and
            (self.mapBase is as invariant) and
            (self.magCode is as invariant) and
            (self.tileKind is as invariant) and
            (self.canvasSize is a (width,height) 2-sequence) ->
              if (self.mapBase names a map base that has at least one
              defined slot overlapping self.latLonbox) ->
                self  :=  self with a ScrolledCanvas added, displaying
                          any tiles from self.MapBase that overlap
                          self.latLonBox
             else -> raise ValueError ]
        """

        #-- 1 --
        # [ self  :=  self with row 0 and column 0 made stretchable ]
        self.columnconfigure ( 0, weight=1 )
        self.rowconfigure    ( 0, weight=1 )

        #-- 2 --
        # [ (self.latLonBox is as invariant) and
        #   (self.mapBase is as invariant) and
        #   (self.magCode is as invariant) ->
        #     if self.mapBase contains at least one tile slot
        #     overlapping self.latLonBox ->
        #       self.magBox  :=  a new MagBox object representing   
        #           all known corners from self.mapBase that adjoin
        #           slots overlapping self.latLonBox
        #       else -> raise ValueERror ]
        self.magBox  =  MagBox ( self.mapBase, self.magCode,
                                 self.latLonBox )

        #-- 3 --
        # [ self.scrollCan  :=  a ScrolledCanvas object in self,
        #       gridded, with virtual size self.magBox.displayBox
        #       and physical self.canvasSize
        #   self.can   :=  the canvas from that ScrolledCanvas ]
        self.scrollCan  =  canscroll.ScrolledCanvas ( self,
            self.magBox.displayBox[0],
            self.magBox.displayBox[1],
            width=self.canvasSize[0],
            height=self.canvasSize[1] )
        self.scrollCan.grid(sticky=N+S+E+W)
        self.can  =  self.scrollCan.can

        #-- 4 --
        # [ (self.magBox as invariant) and
        #   (self.tileKind as invariant) ->
        #     self.photoImage  :=  an image, as a PIL Image object,
        #       containing any tiles from self.magBox of kind
        #       tileKind, with missing areas gray ]
        image  =  self.magBox.getImage ( self.tileKind, "#cccccc" )
        self.photoImage  =  ImageTk.PhotoImage ( image )

        #-- 5 --
        # [ self.can  :=  self.can with self.photoImage loaded ]
        self.can.create_image ( 0, 0, anchor=NW,
            image=self.photoImage )
