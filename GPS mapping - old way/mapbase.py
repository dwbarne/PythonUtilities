"""mapbase.py:  TerraServer map tile package.
        $Revision: 1.19 $  $Date: 2005/02/12 00:17:03 $

  Important definitions (See `Specification functions' below):
    mag-code:  Magnification code, meters per pixel: 1, 2, 4, ..., 512
    tile-kind:  1 for orthophoto tiles, 2 for topographic map tiles
    slot-ID:  Identifies a location where one 200x200 tile can
        be displayed; a tuple (mag-code, column, row) where
        the column is the `x=' and the row the `y=' values that
        Terraserver uses to locate tiles at a given magnification.
        The column number increases west->east, and the
        row number increases south->north.
    slot-col-row:  Just the (column,row) part of a slot-ID.
    tile-ID:  Identifies a specific image that goes in a given slot;
        a tuple (mag-code, column, row, tile-kind)
    corner-ID:  Corners are named in the same way: a given
        corner-ID refers to the southwest corner of the tile
        with the same tile-ID.
    corner-col-row:  The (column,row) part of a corner-ID.

        For example, the 4-meter tile in column 372, row 4703 is near
        33N. Lat., 107 W. Lon.  Here are the corner-IDs of its corners:
        
        (4, 372, 4704) NW +---------------+ NE (4, 373, 4704)
                          |               |
                          |               |
                          |    tile-id    |
                          | (4,372,4703)  |
                          |               |
                          |               |
                          |               |
                          |               |
        (4, 372, 4703) SW +---------------+ SE (4, 373, 4703)

    display-coordinate:  The usual coordinate system for displays,
        with (0,0) in the northwest corner, X increasing to the east,
        and Y increasing to the *south* (as opposed to Cartesian
        coordinates where Y increases to the north).

================================================================
  Exports:
----------------------------------------------------------------
    class MapBase:          Represents a mapping base directory
        MapBase(baseDir):
          [ baseDir is a string ->
              return a new MapBase object representing that map base ]
        .baseDir:       [ as passed to constructor, read-only ]
        .getCornerSet(mag):
          [ mag is a magnification as a mag-code ->
              if self knows any corners for that magnification ->
                return a CornerSet object representing all corners
                for that magnification
              else -> raise IOError ]
        .getCornerFileName(mag):
          [ mag is a magnification as a mag-code ->
              return the name of the corners file for that magnification ]
        .getTile(mag, slotCR, kind):
          [ (mag is a magnification as a mag-code) and
            (slotCR specifies a slot as a slot-col-row) and
            (kind is a tile-kind) ->
              if self has a tile for that magnification, slot, and kind ->
                return that tile as a PIL Image object
              else -> raise IOError ]
        .getTileBaseName(mag,slotCR,kind):
          [ (mag is a magnification as a mag-code) and
            (slotCR specifies a slot as a slot-col-row) and
            (kind is a tile-kind) ->
              return the name of the tile file for those attributes,
              minus its extension ]
        .getTileFileName(mag,slotCR,kind):
          [ (mag is a magnification as a mag-code) and
            (slotCR specifies a slot as a slot-col-row) and
            (kind is a tile-kind) ->
              return the name of the tile file for those attributes,
              with the extension (.jpg or .gif) expected for those
              attributes ]

    class MagBox:           Represents one area built up from tiles
        MagBox ( mapBase, magCode, geoBox ):
          [ (mapBase is a MapBase object) and
            (magCode is a magnification as a mag-code) and
            (geoBox is a rectangle of lat-longs as a TerraBox) ->
              if mapBase contains at least one tile slot overlapping
              geoBox ->
                return a new MagBox representing all known corners
                of that magCode that adjoin slots overlapping magBox
              else -> raise ValueError ]
        .mapBase:       [ as passed to constructor, read-only ]
        .magCode:       [ as passed to constructor, read-only ]
        .geoBox:        [ as passed to constructor, read-only ]
        .cornerSet:
          [ a CornerSet containing all known corners of magnification
            self.magCode that adjoin slots overlapping self.magBox ]
        .displayBox:
          [ a 2-sequence (x,y) sizing the image that .getImage()
            will build ]
        .getImage ( kind, bg=None ):
          [ (kind is a tile-kind) and
            (bg is a color name as a string, defaulting to "black") ->
              return a new image, as a PIL Image object, of size
              self.displayBox, containing any tiles with
              tile-kind=kind from self.mapBase, with areas of missing
              tiles set to color bg ]
        .displayToLatLon ( xy ):
          [ xy is a display coordinate on self's image, with (0,0) at
            the northwest corner, as a 2-sequence (x,y) ->
              if xy falls on a known slot in self.mapBase ->
                return the corresponding lat-long as a TerraPosition
              else -> raise ValueError ]
        .latLonToDisplay ( latLon ):
          [ latLon is a TerraPosition ->
              if latLon falls on a known slot in self.mapBase ->
                return the corresponding display coordinate
              else -> raise ValueError ]
        .canToSlotPoint ( canXY ):
          [ canXY is a display coordinate in self as a 2-sequence ->
              return the SlotPoint corresponding to that coordinate ]
        .slotPointToCan ( slotPoint ):
          [ slotPoint is a coordinate as a SlotPoint object defined in self ->
              return the corresponding display coordinate as a 2-sequence ]

    class CornerSet:        Holds the lat-longs for all known tile corners.
        CornerSet():
          [ return a new, empty CornerSet ]
        .cornerBase:
          [ if self contains no corners ->
              None
            else ->
              (minimum corner-col, minimum corner-row) for
              all corners in self ]
        .cornerLimit:
          [ if self contains no corners ->
              None
            else ->
              (maximum corner-col, maximum corner-row) for
              all corners in self ]            
        .__len__(self):     [ return number of corners in self ]
        .addCorner(c):
          [ c is a TileCorner object ->
              if self has no corner with the same corner-ID as c ->
                self  :=  self with c added
              else -> I ]
        .addFile(fileName):
          [ fileName is a string ->
              if fileName names a readable, valid corners file ->
                self  :=  self with new CornerSet objects added
                          representing contents of that file
              else -> raise IOError ]
        .getCorner(slotCR):
          [ slotCR is a slot-col-row ->
              if self has a corner for slotCR ->
                return a TileCorner object representing that corner
              else -> raise KeyError ]
        .getSlot(slotCR):
          [ slotCR is a slot-col-row ->
              if self has all corners of that tile ->
                return a TileSlot object representing those corners
              else -> raise KeyError ]
        .getSlotByLatLon(latLon):
          [ latLon is a TerraPosition ->
              if self contains a TileSlot all corners of which are defined
              and which contains latLon ->
                return that TileSlot
              else -> raise KeyError ]
        .geoCrop(terraBox):
          [ terraBox is a geographic area as a TerraBox ->
              if all four corners of terraBox fall on tiles known to self ->
                return a new CornerSet object containing all the corners in
                self within the rectangle containing terraBox
              else -> raise IOError ]
        .writeFile(fileName):
          [ fileName is a file name as a string ->
              if we can create the file with name fileName new ->
                that file  :=  self as a corners file
              else -> raise IOError ]

    class TileSlot:         Contains coordinates for all 4 corners of a tile.
        TileSlot(slotCR, sw, nw, se, ne):
          [ (slotCR is a slot-col-row) and
            (sw, nw, se, and ne are TileCorner objects defining the
            southwest, northwest, southeast and northeast corners) ->
              return a TileSlot object representing that tile slot ]
        .bbox:
          [ self's bounding box in terrestrial coordinates, as a
            TerraBox object ]
        .containsLatLon(latLon):
          [ latLon is a TerraPosition object ->
              if latLon's position is contained within self -> return 1
              else -> return  0 ]
        .containsUTM(utm):
          [ utm is a UTM object in the same zone as self's zone ->
              if utm is located inside of self's slot -> return 1
              else -> return 0 ]
        .latLonToDisplay(latLon):
          [ latLon is a position as a TerraPosition object ->
              if latLon is contained within self ->
                return its (x,y) display coordinates relative to the
                NORTHWEST corner of self
              else ->
                raise ValueError ]
        .displayToLatLon(p):
          [ p is a 2-sequence of display coordinates relative to
            self's tile's NORTHWEST (not southwest) corner ->
              if p is defined in self ->
                return the position of P as a TerraPosition object, using
                self's corners as a basis
              else -> raise ValueError ]
            **  Note: The argument is a display coordinate, so +Y is south.
            **  Note: This should be used only for points inside self's
                corners.  It will work with reasonable accurace for points
                just outside the tile, but the farther, the less accurate.

    class TileCorner:       Coordinates of one corner of a tile.
        TileCorner ( magCode, slotCR, latLon, utm ):
          [ (magCode is the tile's resolution in meters/pixel) and
            (slotCR is a corner-col-row) and
            (latLon is the corner's location as a TerraPosition object) and
            (utm is the corner's location as a UTM object) ->
              return a new TileCorner object with those values ]
        .magCode:       [ as passed to constructor, read-only ]
        .slotCR:        [ as passed to constructor, read-only ]
        .latLon:        [ as passed to constructor, read-only ]
        .utm:           [ as passed to constructor, read-only ]
        .__cmp__():
          [ compare function that sorts on slotCR's row as the major key
            and slotCR's column as the minor key ]

    class UTM:         A location on the Universal Transverse Mercator Grid
        UTM(zone, easting, northing):
          [ (zone is a UTM zone number) and
            (easting is the easting coordinate in meters) and
            (northing is the northing coordinate in meters) ->
              return a new UTM object representing those coordinates
        .zone:          [ as passed to constructor, read-only ]
        .easting:       [ as passed to constructor, read-only ]
        .northing:      [ as passed to constructor, read-only ]
        **  Note:  Eventually this class needs to be integrated into
            the TerraPosition hierarchy, but at the moment I don't have any
            handy software for converting UTM <-> LatLong, so at this
            point it is basically a struct (in the C sense).

    class SlotPoint:    A location as a tile-ID and a display coordinate.
        SlotPoint ( slotCR, displayXY ):
          [ (slotCR is the slot-ID of a tile slot) and
            (displayXY is a point on that slot as a display coordinate) ->
              return a new SlotPoint object representing that slot
              and coordinate ]
        .slotCR:        [ as passed to constructor, read-only ]
        .displayXY:     [ as passed to constructor, read-only ]
"""


#================================================================
# Imports
#----------------------------------------------------------------

#--
# Standard Python library modules
#--

import os.path              # Pathname functions
import Image as PIL         # Python Imaging Library


#--
# Modules from NumPy, the Numeric Python package
#--

import Numeric              # Numeric Python for arrays
import LinearAlgebra        # For solve_linear_equations()


#--
# Modules specific to this application
#--

from terrapos import *      # Earth position objects: TerraPosition, LatLon


#================================================================
# Manifest constants
#   TILE_WIDE, TILE_HIGH:  The x and y display dimensions of a
#       standard tile.  We hope it's unlikely that TerraServer will
#       suddenly start issuing tiles in other sizes.
#----------------------------------------------------------------

TILE_WIDE  =  200
TILE_HIGH  =  200

PHOTO_KIND  =  1            # Code for orthophoto tiles
TOPO_KIND   =  2            # Code for topographic map tiles

DISPLAY_NW  =  (0,0)        # Display coordinates of tile corners
DISPLAY_NE  =  (200,0)
DISPLAY_SW  =  (0,200)
DISPLAY_SE  =  (200,200)

#--
# File names and extensions.  Most tiles are in .jpg format, but
# we must support .gif because some of the topo tiles are GIFs.
#--

CORNERS_NAME  =  "corners"              # Corners file name
TILES_PREFIX  =  "tiles-"               # E.g., "tiles-4" for mag-4 tiles
TILE_EXT_LIST =  [ ".jpg", ".gif" ]     # Supported tile formats


#--
# Corner file format: foo_F is the index of field foo
#--

PIXEL_SIZE_F    =  0                    # Pixel size
TILE_X_F        =  1 + PIXEL_SIZE_F     # Tile x coordinate...
TILE_Y_F        =  1 + TILE_X_F         # ...and y coord. on the big grid
LAT_DEG_F       =  1 + TILE_Y_F         # Latitude degrees
LON_DEG_F       =  1 + LAT_DEG_F        # Longitude degrees
UTM_ZONE_F      =  1 + LON_DEG_F        # UTM zone number
UTM_EASTING_F   =  1 + UTM_ZONE_F       # UTM easting coordinate
UTM_NORTHING_F  =  1 + UTM_EASTING_F    # UTM northing coordinate
CORNER_FIELDS   =  1 + UTM_NORTHING_F   # Total number of fields


#================================================================
# Specification functions
#----------------------------------------------------------------
# corner-ID ==
#   a 3-sequence (mag, col, row) identifying one slot corner for
#   a given magnification.
#--
#   Corners are named using the same (column,row) numbers as
#   a slot-col-row.  The southwest corner of a tile with tile-ID
#   (4, 372, 4703) is (372, 4703); the northwest corner is
#   (372, 4704); southeast corner is (373, 4703); northeast,
#   (373, 4704).
#----------------------------------------------------------------
# corner-col-row ==
#   a two-sequence (col,row) that names the southwest corner of a
#   tile of a given mag-code
#----------------------------------------------------------------
# mag-code ==
#   an integral power of two in the range [1,512]
#--
#   The magnification of a map tile is expressed in the size of
#   a pixel in meters.  Hence, a mag-code of 1 implies one meter
#   per pixel, so a 200x200-pixel map tile represents 200x200
#   meters.  Similarly, a mag-code of 4 is 4 m/pixel, so a tile
#   with that mag-code shows an 800x800-meter area.
#----------------------------------------------------------------
# normalize-point(min,max,P) ==
#   (P-min)/(max-min)
#--
#   This is the normalization function that standardizes a value
#   P along an interval [min,max].  If P is in the range, its
#   normalized value will fall in [0.0, 1.0].
#----------------------------------------------------------------
# interpolate-point(lo,hi,norm) ==
#   lo+norm*(hi-lo)
#--
#   This function takes a normalized value in [0.0, 1.0] that
#   represents a distance along the line from lo to hi and
#   returns the corresponding value in the range [lo,hi]
#----------------------------------------------------------------
# slot-ID ==
#   a 3-sequence (mag-code, column, row) identifying one tile
#   location for a given magnification.
#----------------------------------------------------------------
# slot-col-row ==
#   a 2-sequence (column, row) identifying a tile location.
#----------------------------------------------------------------
# tile-ID ==
#   a 4-sequence (mag,col,row,kind) where col is the column (x)
#   number and row is the row (y) number in Terraserver's grid
#   for magnification=mag.  See the picture at the top of this file.
#--
#   Tiles of different magnifications have almost the same origin
#   in their (x,y) coordinates.  For a tile at (x,y), the next
#   higher magnification tile showing the southwest quarter of
#   that tile is the one at (2*x-2, 2*y).  So the southwest
#   quarter of mag-8 tile (190,2354) is mag-4 tile (378,4708).
#----------------------------------------------------------------
# tile-kind ==
#   one of:
#       TOPO_KIND for topographic (contour) map tiles
#       PHOTO_KIND for orthophotoquad (aerial photo) tiles
#----------------------------------------------------------------




#================================================================
# Functions and classes
#----------------------------------------------------------------


# - - -   t i l e x f o r m   - - -

#--
# Given:
#  (1)  Four corners of a tile in some (X,Y) coordinate system
#  (2)  Those same four corners in some (U,V) coordinate system
#  (3)  A point P in the (X,Y) coordinate system
# Find the coordinates (Pu,Pv) of point P in the (U,V) system.
#
# Algorithm:
#  (a)  Find the points (W,N,E,S) so that:
#
#         - Point W is on the west side, point E is on the east
#           side, and line WE contains P (and all other points
#           with the same X coordinate).
#
#         - Point N is on the north side, point S is on the south
#           side, and line SN contains P (and all other points
#           with the same Y coordinate).
#
#       First we normalize the coordinates of P to [0.0, 1.0]
#       relative to the sides of the tile in the (X,Y) system,
#       so that (0.0,1.0) is the SE corner, (1.0,0.0) is the
#       NW corner, and so on:
#
#           Wn = (Py-SWy)/(NWy-SWy)
#           En = (Py-SEy)/(NEy-SEy)
#           Sn = (Px-SWx)/(SEx-SWx)
#           Nn = (Px-NWx)/(NEx-NWx)
#
#  (b)  Project these values onto the sides in the (U,V) coordinate system:
#
#           N = (NWu + Nn*(NEu-NWu), NWv + Nn*(NEv-NWv))
#           S = (SWu + Sn*(SEu-SWu), SWv + Sn*(Sev-SWv))
#           W = (SWu + Wn*(NWu-SWu), SWv + Wn*(NWv-SWv))
#           E = (SEu + En*(NEu-SEu), SEv + En*(NEv-SEv))
#
#  (c)  Find the intersection of lines WE and SN using Numeric Python's
#       LinearAlgebra module.
#--

def tilexform(p,sw,nw,se,ne,sw2,nw2,se2,ne2):
    """Generic tile transform function.

      [ (p is an (x,y) 2-sequence in the (X,Y) coordinate system) and
        (sw, nw, se, ne) are 2-sequences of the tile corners in
        the (X,Y) coordinate system) and
        (sw2,nw2,se2,ne2) are 2-sequences of the tile corners in
        the (U,V) coordinate system) and
        (any two adjacent sides of the tile are a basis in either
        coordinate system) ->
          return the tuple (u,v) of point p in the (U,V) system ]
    """

    #-- 1 --
    # [ Wn, En, Sn, Nn  :=  as in step (a) ]
    Wn  =  normalize ( sw[1], nw[1], p[1] )
    En  =  normalize ( se[1], ne[1], p[1] )
    Sn  =  normalize ( sw[0], se[0], p[0] )
    Nn  =  normalize ( nw[0], ne[0], p[0] )

    #-- 2 --
    # [ N, S, E, W  :=  as in step (b) ]
    S  =  (project(sw2[0], se2[0], Sn), project(sw2[1], sw2[1], Nn) )
    N  =  (project(nw2[0], ne2[0], Nn), project(nw2[1], ne2[1], Nn) )
    W  =  (project(sw2[0], nw2[0], Wn), project(sw2[1], nw2[1], Wn) )
    E  =  (project(se2[0], ne2[0], En), project(se2[1], ne2[1], En) )    
    
    #-- 3 --
    # [ (u,v)  :=  solution as in step (c) ]
    uv  =  intersector ( S, N, W, E )
    return uv


# - - -   i n t e r s e c t o r   - - -

#--
# Here is a diagram of the problem:  Find point P, given points
# S,W,N,E.
#                   N
#                  /
#                 /
#                /
#         W-----P------------E
#              /
#             /
#            S
#
# Start with the two-point form for the equation of a line,
# first for line WE:
#  (1)  (y-Wy) / (x-Wx)  = (Ey-Wy) / (Ex-Wx)
#
# Cross-multiplying:
#  (2)  (x-Wx) * (Ey-Wy) = (y-Wy) * (Ex-Wx)
#
# Distribute:
#  (3)  x*(Ey-Wy) - Wx*Ey + Wx*Wy = y*(Ex-Wx) - Wy*Ex + Wx*Wy
#
# Subtract Wx*Wy from both sides:
#  (4)  x*(Ey-Wy) - Wx*Ey         = y*(Ex-Wx) - Wy*Ex
# 
# Rearrange in the form a*x + b*y = c:
#  (5)  x*(Ey-Wy) - y*(Ex-Wx)  =  Wx*Ey - Wy*Ex
#
# Make the coefficient of y positive:
#  (6)  x*(Ey-Wy) + y*(Wx-Ex)  =  Wx*Ey - Wy*Ex
#
# Line SN in the form of equation (5) is then:
#  (6)  x*(Ny-Sy) + y*(Sx-Nx)  =  Sx*Ny - Sy*Nx
#
# At this point we can use Python's linear equation solver
# to find the solution to the system (5) + (6), yielding
# the values of x and y.
#--

def intersector(S,N,W,E):
    """Implements the above algorithm.

      [ (all arguments are (x,y) 2-sequences) and
        (lines SN and EW intersect and are not collinear) ->
          return the (x,y) of SN's intersection with EW ]
    """

    #-- 1 --
    Sx,Sy = S
    Wx,Wy = W
    Ex,Ey = E
    Nx,Ny = N

    #-- 2 --
    # [ a  :=  floating matrix of coefficients for equations (5) and (6)
    #   b  :=  vector of right-hand sides for equations (5) and (6) ]
    a  =  Numeric.array ( ( (Ey-Wy, Wx-Ex), (Ny-Sy, Sx-Nx) ), Numeric.Float64 )
    b  =  Numeric.array ( ( Wx*Ey-Wy*Ex, Sx*Ny - Sy*Nx ) )

    #-- 3 --
    # [ x, y  :=  solutions of the linear system with coefficients a
    #             and right-hand side b ]
    x, y  =  LinearAlgebra.solve_linear_equations ( a, b )

    #-- 4 --
    return (x,y)


# - - -   n o r m a l i z e   - - -

def normalize(lo,hi,x):
    """Normalize a number so 0.0=lo, 1.0=hi.

      [ lo, hi, x are numbers ->
          return (x-lo)/(hi-lo) using float arithmetic ]
    """
    flo  =  float(lo)
    return  (x-flo)/(hi-flo)


# - - -   p r o j e c t   - - -

def project(lo,hi,norm):
    """Project a normalized value based on [0.0,1.0] to a new interval.

      [ lo, hi, and norm are numbers ->
          return lo+norm*(hi-lo) using float arithmetic ]
    """
    flo  =  float(lo)
    return  flo + norm * ( hi - flo )



# - - - - -   c l a s s   M a p B a s e   - - - - -

class MapBase:
    """Object to retrieve tiles.

        Design note:  At this time, you have to download the
        map tiles and create a `corners' file essentially by hand,
        using the procedure described in document py-mapping.xml.
        In the future, we may automate tile downloading by going
        directly through terraserver-usa.com's SOAP interface.
        The baseDir argument will still be necessary, to specify
        where the downloaded tiles and corners will be cached locally.

      State/Invariants:
        self.__cornerSetMap:
          [ a dictionary whose values are all the CornerSet objects
            for corners in self, and whose keys are the mag-codes
            for those CornerSet objects ]
    """


# - - -   M a p B a s e . _ _ i n i t _ _   - - -

    def __init__ ( self, baseDir ):
        "Constructor for MapBase."
        self.baseDir  =  baseDir
        self.__cornerSetMap  =  {}



# - - -   M a p B a s e . g e t C o r n e r S e t   - - -

    def getCornerSet ( self, mag ):
        "Read corners for a given magnification, return as a CornerSet."

        #-- 1 --
        # [ if self.__cornerSetMap has a key mag ->
        #     return self.__cornerSetMap[mag]
        #   else -> I ]
        try:
            return self.__cornerSetMap[mag]
        except KeyError:
            pass

        #-- 2 --
        # [ self.baseDir is a string ->
        #     cornerFileName  :=  a pathname with directory
        #         (self.baseDir + "/" + TILES_PREFIX + "/" +
        #         CORNERS_NAME) ]
        cornerFileName  =  self.getCornerFileName ( mag )

        #-- 3 --
        # [ cornerFileName is a string ->
        #     if cornerFileName names a valid corners file ->
        #       cornerSet  :=  a CornerSet object representing that file
        #     else -> raise IOError ]
        cornerSet  =  CornerSet ( )
        cornerSet.addFile ( cornerFileName )

        #-- 4 --
        self.__cornerSetMap[mag]  =  cornerSet
        return cornerSet


# - - -   M a p B a s e . g e t C o r n e r F i l e N a m e   - - -

    def getCornerFileName ( self, mag ):
        "Return the name of the corners file for a given mag-code."

        #-- 1 -
        # [ self.baseDir is a string ->
        #     cornerFileName  :=  a pathname with directory
        #         (self.baseDir + "/" + TILES_PREFIX + "/" +
        #         CORNERS_NAME) ]
        magDir  =  os.path.join ( self.baseDir,
                                  "%s%d" % (TILES_PREFIX, mag ) )
        cornerFileName  =  os.path.join ( magDir, CORNERS_NAME )

        #-- 2 --
        return cornerFileName


# - - -   M a p B a s e . g e t T i l e   - - -

    def getTile ( self, mag, slotCR, kind ):
        "Return a PIL Image object for a given tile, if we have it."

        #-- 1 --
        # [ fileBase  :=  the path name of file in directory
        #       self.baseDir, subdirectory (TILES_PREFIX+str(mag)),
        #       file name (kind) + "-" + (slotCR[0]) +
        #                 "-" + (slotCR[1]) ]
        fileBase  =  self.getTileBaseName ( mag, slotCR, kind )

        #-- 2 --
        # [ if fileBase plus any of the extensions in TILE_EXT_LIST
        #   names a readable, valid image file ->
        #     return a PIL Image object representing that image
        #   else -> raise IOError ]
        for  ext in TILE_EXT_LIST:
            fileName  =  fileBase+ext
            try:
                result  =  PIL.open ( fileName )
                return result
            except IOError:
                pass

        #-- 3 --
        raise IOError, ( "Couldn't find an image named `%s'." %
            fileBase )


# - - -   M a p B a s e . g e t T i l e B a s e N a m e   - - -

    def getTileBaseName ( self, mag, slotCR, kind ):
        "Get the name of a tile file, without its extension."
        dir  =  os.path.join ( self.baseDir,
                               "%s%d" % (TILES_PREFIX, mag) )
        fileBase  =  os.path.join ( dir,
            "%d-%d-%d" % (kind, slotCR[0], slotCR[1]) )
        return fileBase        


# - - -   M a p B a s e . g e t T i l e F i l e N a m e   - - -        

    def getTileFileName ( self, mag, slotCR, kind ):
        "Get the name of a tile file, complete with extension."

        #-- 1 --
        # [ fileBase  :=  the tile file's name without extension ]
        fileBase  =  self.getTileBaseName ( mag, slotCR, kind )

        #-- 2 --
        # [ extension  :=  the extension expected for TerraServer
        #       tiles of this mag and kind ]
        if  ( ( kind == 2 ) and         # If it's a topo tile...
              ( ( mag == 2 ) or         # ...and has one of...
                ( mag == 8 ) or         # ...these mag-codes
                ( mag == 32 ) ) ):
            extension  =  ".gif"
        else:
            extension  =  ".jpg"

        #-- 3 --
        return fileBase + extension



# - - - - -   c l a s s   M a g B o x   - - - - -

class MagBox:
    "Represents one geographic area built up of image tiles."


# - - -   M a g B o x . _ _ i n i t _ _   - - -

    def __init__ ( self, mapBase, magCode, geoBox ):
        "Constructor for MagBox"

        #-- 1 --
        self.mapBase  =  mapBase
        self.magCode  =  magCode
        self.geoBox   =  geoBox

        #-- 2 --
        # [ if mapFrame has a corner set for magnification magCode ->
        #     fullSet  :=  that set as a CornerSet
        #   else -> raise ValueError ]
        try:
            fullSet  =  mapBase.getCornerSet ( magCode )
        except IOError:
            raise ValueError, ( "Map base has no corners for mag=%d." %
                                magCode )

        #-- 3 --
        # [ self.cornerSet  :=  a CornerSet containing all corners
        #       from fullSet within the rectangle containing geoBox ]
        try:
            self.cornerSet  =  fullSet.geoCrop ( geoBox )
        except IOError:
            text  =  ( "Map base is missing corners of the box [%s]" %
                       geoBox )
            raise ValueError, text

        #-- 4 --
        # [ if self.cornerSet is empty ->
        #     raise ValueError
        #   else ->
        #     self.displayBox  :=  as invariant ]
        if  len ( self.cornerSet ) == 0:
            raise ValueError, ( "Map base has no corners in the "
                "specified area for mag=%d." % magCode )
        else:
            xSize  =  ( TILE_WIDE *
                        ( self.cornerSet.cornerLimit[0] -
                          self.cornerSet.cornerBase[0] ) )
            ySize  =  ( TILE_HIGH *
                        ( self.cornerSet.cornerLimit[1] -
                          self.cornerSet.cornerBase[1] ) )

            self.displayBox  =  (xSize, ySize)


# - - -   M a g B o x . g e t I m a g e   - - -

    def getImage ( self, kind, bg=None ):
        "Build an image up from available tiles."

        #-- 1 --
        # [ mapImage  :=  a new PIL Image of size self.displayBox
        #       with all pixels set to color bg (defaulting to black) ]
        if  bg is None:     color  =  "black"
        else:               color  =  bg
        mapImage  =  PIL.new ( "RGB", self.displayBox, color )

        #-- 2 --
        # [ mapImage  :=  mapImage with all tiles added from self.mapBase
        #       that have tile-kind=kind and whose slots are in
        #       self.cornerSet ]
        for  col in range ( self.cornerSet.cornerBase[0],
                            self.cornerSet.cornerLimit[0] ):
            for  row in range ( self.cornerSet.cornerBase[1],
                                self.cornerSet.cornerLimit[1] ):
                #-- 2 body --
                # [ if self.mapBase has a tile with magnification ==
                #   self.magCode, slot-col-row == (col,row), and
                #   tile-kind=kind ->
                #     mapImage  :=  mapImage with that tile pasted in
                #       at its position relative to self.cornerSet
                #   else -> I ]
                self.__loadTile ( mapImage, (col, row), kind )

        #-- 3 --
        return mapImage


# - - -   M a g B o x . _ _ l o a d T i l e   - - -

    def __loadTile ( self, mapImage, slotCR, kind ):
        """Paste one tile into the image if there is a tile.

          [ (mapImage is a PIL Image object) and
            (slotCR is a slot-col-row) and
            (kind is a tile-kind) ->
              if self.mapBase has a tile with magnification ==
                self.magCode, slot-col-row == (col,row), and
                tile-kind=kind ->
                  mapImage  :=  mapImage with that tile pasted in
                    at its position relative to self.cornerSet
                else -> I ]
        """

        #-- 1 --
        # [ if self.mapBase has a tile with magnification=self.magCode,
        #   slot-col-row=slotCR, and tile-kind=kind ->
        #     tileImage  :=  that tile as a PIL Image object
        #   else -> return ]
        try:
            tileImage  =  self.mapBase.getTile ( self.magCode,
                slotCR, kind )
        except IOError:
            return

        #-- 2 --
        # [ slotOrig  :=  a SlotPoint object representing the (0,0)
        #       pixel of the slot with slot-col-row=slotCR ]
        slotOrig  =  SlotPoint ( slotCR, (0,0) )

        #-- 3 --
        # [ tileOrig  :=  slotOrig as a canvas coordinate ]
        tileOrig  =  self.slotPointToCan ( slotOrig )

        #-- 4 --
        # [ image  :=  image with tileImage replacing the tile-sized
        #       rectangle whose origin is tileOrig ]
        box  =  tileOrig + (tileOrig[0] + TILE_WIDE,
                            tileOrig[1] + TILE_HIGH)
        mapImage.paste ( tileImage, box )


# - - -   M a g B o x . d i s p l a y T o L a t L o n   - - -

    def displayToLatLon ( self, xy ):
        "Find the lat-lon of a display coordinate on the canvas."

        #-- 1 --
        # [ if xy falls on a tile in self.cornerSet ->
        #     slotPoint  :=  a SlotPoint object representing that position
        #   else ->
        #     raise ValueError ]
        slotPoint  =  self.canToSlotPoint ( xy )

        #-- 2 --
        # [ if slotCR is defined in self.cornerSet ->
        #     slot  :=  the slot from slotPoint as a TileSlot object
        #   else -> raise ValueError ]
        try:
            slot  =  self.cornerSet.getSlot ( slotPoint.slotCR )
        except KeyError:
            raise ValueError, ( "Coordinate (%d,%d) out of range." %
                                (slotPoint.slotCR[0], slotPoint.slotCR[1] ) )

        #-- 3 --
        # [ latLon  :=  display coordinates from slotPoint interpreted
        #               relative to the slot ]
        latLon  =  slot.displayToLatLon ( slotPoint.displayXY )

        #-- 4 --
        return latLon


# - - -   M a g B o x . c a n T o S l o t P o i n t   - - -

    def canToSlotPoint ( self, canXY ):
        "Convert a canvas coordinate to the equivalent SlotPoint."

        #-- 1 --
        canX, canY  =  canXY

        #-- 2 --
        # [ colsWest   :=  number of whole tile columns west of canXY
        #   offX       :=  distance from canXY to the next column boundary
        #                  to the west
        #   rowsNorth  :=  number of whole tile rows north of canXY
        #   offY       :=  distance from canXY to the next row boundary
        #                  to the north ]
        colsWest, offX  =  divmod ( canX, TILE_WIDE )
        rowsNorth, offY  =  divmod ( canY, TILE_HIGH )

        #-- 3 --
        # [ tileCR  :=  tile-CR of the tile colsWest to the right and
        #               rowsNorths below the NW corner
        #   offXY   :=  (offX, offY) ]
        colNo   =  self.cornerSet.cornerBase[0] + colsWest
        rowNo   =  self.cornerSet.cornerLimit[1] - 1 - rowsNorth
        tileCR  =  (colNo, rowNo)
        offXY   =  (offX, offY)

        #-- 4 --
        return  SlotPoint ( tileCR, offXY )


# - - -   M a g B o x . l a t L o n T o D i s p l a y   - - -

    def latLonToDisplay ( self, latLon ):
        "Find the display coordinate of a given lat-long."

        #-- 1 --
        # [ if self.cornerSet has a slot containing latLon ->
        #     slot  :=  the slot as a TileSlot
        #   else -> raise ValueError ]
        try:
            slot  =  self.cornerSet.getSlotByLatLon ( latLon )
        except KeyError:
            raise ValueError, ( "Lat-lon %s not on a known slot." % latLon )

        #-- 2 --
        # [ tileXY  :=  display coordinate of latLon within slot ]
        tileXY  =  slot.latLonToDisplay ( latLon )

        #-- 3 --
        # [ slotPoint  :=  a SlotPoint with the slot-CR from slot and
        #                  slot-relative coordinates tileXY ]
        slotPoint  =  SlotPoint ( slot.slotCR, tileXY )

        #-- 4 --
        # [ (slotPoint is a SlotPoint object) and
        #   (slotPoint falls on a known tile slot) ->
        #     return the display coordinate of self's canvas of slotPoint ]
        return self.slotPointToCan ( slotPoint )


# - - -   M a g B o x . s l o t P o i n t T o C a n   - - -

    def slotPointToCan ( self, slotPoint ):
        "Convert a tile ID and a coordinate on that slot to a canvas coord."

        #-- 1 --
        displayX,  displayY  =  slotPoint.displayXY
        slotCol, slotRow     =  slotPoint.slotCR

        #-- 2 --
        # [ colsWest   :=  number of whole tile columns west of slotCol
        #   rowsNorth  :=  number of whole tile rows north of slotRow ]
        colsWest   =  slotCol - self.cornerSet.cornerBase[0]
        rowsNorth  =  self.cornerSet.cornerLimit[1] - 1 - slotRow

        #-- 3 --
        return ( colsWest * TILE_WIDE + displayX,
                 rowsNorth * TILE_HIGH + displayY )



# - - - - -   c l a s s   C o r n e r S e t   - - - - -

class CornerSet:
    """Container for known tile corners (in latLon and UTM coordinates)

      State/Invariants:
        .__crMap:
          [ a dictionary mapping slot-col-row |-> TileCorner objects for
            all corners in self ]
    """


# - - -   C o r n e r S e t . g e t C o r n e r   - - -

    def getCorner ( self, cornerCR ):
        "Retrieve one specific corner by its corner-col-row."
        return self.__crMap [ tuple ( cornerCR ) ]


# - - -   C o r n e r S e t . g e t S l o t   - - -

    def getSlot ( self, slotCR ):
        "Retrieve the TileSlot defining a tile with SW corner slotCR."

        #-- 1 --
        # [ swCR  :=  slotCR as a tuple
        #   nwCR  :=  next corner north of slotCR
        #   seCR  :=  next corner east of slotCR
        #   neCR  :=  next corner northeast of slotCR ]
        swCR  =  tuple ( slotCR )
        nwCR  =  ( swCR[0], swCR[1] + 1 )
        seCR  =  ( swCR[0] + 1, swCR[1] )
        neCR  =  ( swCR[0] + 1, swCR[1] + 1 )

        #-- 2 --
        # [ if self contains corners for all of (swCR,nwCR,seCR,neCR) ->
        #     (swCorner, nwCorner, seCorner, neCorner)  :=  Corner
        #       objects corresponding to those slotCR values
        #   else ->
        #     raise KeyError ]
        swCorner  =  self.getCorner ( swCR )
        nwCorner  =  self.getCorner ( nwCR )
        seCorner  =  self.getCorner ( seCR )
        neCorner  =  self.getCorner ( neCR )

        #-- 3 --
        return TileSlot ( slotCR,
            swCorner, nwCorner, seCorner, neCorner )


# - - -   C o r n e r S e t . g e t S l o t B y L a t L o n   - - -

    def getSlotByLatLon ( self, latLon ):
        "Which slot contains a given lat-lon?"

        #-- 1 --
        # [ if any slot in self contains latLon ->
        #     return a TileSlot representing that slot
        #   else -> I ]
        #--
        # IMPORTANT NOTE:  What if a point falls into the crack
        # between two tiles?  If that ever happens, perhaps
        # the best approach is to make TileSlot.containsLatLon()
        # consider points slightly outside the tile to be inside.
        # A good guess at the size of the error tolerance might
        # be half the size of a pixel.  Determining the size of
        # pixel in lat-long space is nontrivial (it varies with
        # the location), but using a somewhat larger error tolerance
        # would probably still produce reasonable results.  After all,
        # extrapolation of values just outside a tile shouldn't be
        # too bad an idea.
        #--
        # NOTE:  This search algorithm has time complexity O(n).
        # If this is ever a problem, perhaps consider starting in
        # the middle of the rectangle defined by self.cornerBase
        # and self.cornerLimit and, whenever the point is not
        # found, walk in the direction where it is expected.
        #--
        for cornerCR in self.__crMap.keys():
            #-- 1 body --
            # [ if (self has a slot for slot-col-row cornerCR) and
            #   (latLon is within that slot) ->
            #     return that slot as a TileSlot
            #   else -> I ]
            try:
                slot  =  self.getSlot(cornerCR)
                if  slot.containsLatLon ( latLon ):
                    return slot
            except KeyError:
                pass

        #-- 2 --
        raise KeyError


# - - -   C o r n e r S e t . _ _ l e n _ _   - - -

    def __len__ ( self ):
        "Return number of corners in self."
        return len(self.__crMap)


# - - -   C o r n e r S e t . _ _ i n i t _ _   - - -

    def __init__ ( self ):
        "Constructor for CornerSet"
        self.__crMap      =  {}
        self.cornerBase   =  None
        self.cornerLimit  =  None


# - - -   C o r n e r S e t . a d d C o r n e r   - - -

    def addCorner ( self, corner ):
        "Add a new corner to self."

        #-- 1 --
        # [ if corner has the same slot-col-row as a corner in self ->
        #     return
        #   else ->
        #     self.__crMap  +:=  an entry mapping corner's slot-col-row
        #                        |-> corner ]
        if  self.__crMap.has_key ( corner.slotCR ):
            return
        else:
            self.__crMap[corner.slotCR]  =  corner

        #-- 2 --
        # [ if self.cornerBase is None ->
        #     self.cornerBase  :=  corner.slotCR
        #   else if corner is south or west of self.cornerBase ->
        #     self.cornerBase  :=  southwest corner of a box
        #           whose main diagonal is defined by corner and
        #           self.cornerBase
        #   else -> I ]
        if  self.cornerBase is None:
            self.cornerBase  =  corner.slotCR
        else:
            if  ( ( corner.slotCR[0] < self.cornerBase[0] ) or
                  ( corner.slotCR[1] < self.cornerBase[1] ) ):
                self.cornerBase  =  (
                    min ( corner.slotCR[0], self.cornerBase[0] ),
                    min ( corner.slotCR[1], self.cornerBase[1] ) )

        #-- 3 --
        # [ if self.cornerLimit is None ->
        #     self.cornerLimit  :=  corner.slotCR
        #   else if corner is north or east of self.cornerLimit ->
        #     self.cornerLimit  :=  northeast corner of a box
        #           whose main diagonal is defined by corner and
        #           self.cornerLimit
        #   else -> I ]
        if  self.cornerLimit is None:
            self.cornerLimit  =  corner.slotCR
        else:
            if  ( ( corner.slotCR[0] > self.cornerLimit[0] ) or
                  ( corner.slotCR[1] > self.cornerLimit[1] ) ):
                self.cornerLimit  =  (
                    max ( corner.slotCR[0], self.cornerLimit[0] ),
                    max ( corner.slotCR[1], self.cornerLimit[1] ) )


# - - -   C o r n e r S e t . a d d F i l e   - - -

    def addFile ( self, fileName ):

        #-- 1 --
        # [ if fileName can be opened for reading ->
        #     inFile  :=  that file, so opened
        #   else -> raise IOError ]
        inFile  =  open ( fileName )

        #-- 2 --
        # [ if inFile contains only valid corner lines ->
        #     self.__crMap  +:=  entries mapping cr |-> C
        #         where cr are the slot-col-rows from inFile lines and 
        #         each C is a TileCorner object representing that line ]
        for  rawLine in inFile:
            #-- 2 body --
            # [ if rawLine is a valid corner line ->
            #     self.__crMap  +:=  an entry mapping the line's
            #         slot-col-row |-> that line as a TileCorner object
            #   else if rawLine is empty ->
            #     I
            #   else -> raise IOError ]
            self.__scanLine ( rawLine )

        #-- 3 --
        inFile.close()


# - - -   C o r n e r S e t . _ _ s c a n L i n e   - - -

    def __scanLine ( self, rawLine ):
        """Process a line from the corners file.

          [ self.__crMap is a dictionary ->
              if rawLine is a valid corner line ->
                self.__crMap  +:=  an entry mapping the line's
                    slot-col-row |-> that line as a TileCorner object
              else if rawLine is empty ->
                I
              else -> raise IOError ]
        """

        #-- 1 --
        # [ if rawLine contains only whitespace ->
        #     return
        #   else ->
        #     line  :=  rawLine minus all leading and trailing whitespace ]
        line  =  rawLine.strip()
        if  len(line) == 0:
            return

        #-- 2 --
        # [ if (line contains at least CORNER_FIELDS fields) and
        #   (all fields can be converted to the correct type) ->
        #      corner  :=  a TileCorner object representing those fields
        #      slotCR  :=  the slot-col-row from those fields
        #   else -> raise IOError ]
        corner  =  self.__buildCorner ( line.split() )

        #-- 3 --
        # [ if self.__crMap has a key corner.slotCR ->
        #     raise IOError
        #   else ->
        #     self  :=  self with corner added ]
        try:
            old  =  self.__crMap[corner.slotCR]
            raise IOError, ( "Duplicate tile: [%s], old tile was [%s]" %
                ( old, corner ) )
        except KeyError:
            self.addCorner ( corner )



# - - -   C o r n e r S e t . _ _ b u i l d C o r n e r   - - -

    def __buildCorner ( self, lineList ):
        """Convert a list of fields into a Corner object.

          [ lineList is a list of strings ->
              if lineList contains the fields of a valid raw
              corner record in order ->
                return a Corner object representing those fields
              else -> raise IOError ]
        """
        #-- 1 --
        if  len(lineList) < CORNER_FIELDS:
            raise IOError, ( "Not enough fields: [%s]" % line )

        #-- 2 --
        # [ if lineList[PIXEL_SIZE_F] is a valid int as a string ->
        #     pixelSize  :=  that value as an int
        #   else ->
        #     raise IOError ]
        pixelSize   =  self.__intConvert   ( lineList[PIXEL_SIZE_F],
                                             "Pixel size" )
        #-- 3 --
        # [ if lineList[TILE_X_F] and lineList[TILE_Y_F] are
        #   valid ints as strings ->
        #     slotCR  :=  those fields as a 2-tuple
        #   else ->
        #     raise IOError ]
        tileX       =  self.__intConvert   ( lineList[TILE_X_F],
                                             "Tile grid X" )
        tileY       =  self.__intConvert   ( lineList[TILE_Y_F],
                                             "Tile grid Y" )
        slotCR      =  (tileX, tileY)

        #-- 4 --
        # [ if lineList[LAT_DEG_F] and lineList[LON_DEG_F] are a
        #   valid lat-long pair as strings ->
        #     latLon  :=  that lat-long pair as a LatLon object
        #   else ->
        #     raise IOError ]
        latDeg      =  self.__floatConvert ( lineList[LAT_DEG_F],
                                             "Latitude" )
        lonDeg      =  self.__floatConvert ( lineList[LON_DEG_F],
                                             "Longitude" )
        latLon      =  LatLon ( latDeg, lonDeg )

        #-- 5 --
        # [ if (lineList[UTM_ZONE_F] is a valid UTM zone as a string) and
        #   (lineList[UTM_EASTING_F] is a valid UTM easting as a string) and
        #   (lineList[UTM_NORTHING_F] is a valid UTM northing as a string) ->
        #      utm  :=  those coordinates as a UTM object
        #   else ->
        #     raise IOError ]
        utmZone     =  self.__intConvert   ( lineList[UTM_ZONE_F],
                                             "UTM zone" )
        utmEasting  =  self.__intConvert   ( lineList[UTM_EASTING_F],
                                             "UTM easting" )
        utmNorthing =  self.__intConvert   ( lineList[UTM_NORTHING_F],
                                             "UTM northing" )
        utm         =  UTM ( utmZone, utmEasting, utmNorthing )

        #-- 4 --
        # [ return a new TileCorner object with those values ]
        corner  =  TileCorner ( pixelSize, slotCR, latLon, utm )
        return corner


# - - -   C o r n e r S e t . _ _ i n t C o n v e r t   - - -

    def __intConvert ( self, raw, text ):
        """Convert string to integer.

          [ raw and text are strings ->
              if raw can be converted to an int ->
                return that int
              else -> raise IOError identifying the bad field as (text) ]
        """
        try:
            result  =  int ( raw )
            return result
        except ValueError:
            raise IOError, ( "Invalid %s field value, expecting an "
                             "integer: [%s]" % ( text, raw ) )


# - - -   C o r n e r S e t . _ _ f l o a t C o n v e r t   - - -

    def __floatConvert ( self, raw, text ):
        """Convert string to float.

          [ raw and text are strings ->
              if raw can be converted to a float ->
                return that int
              else -> raise IOError identifying the bad field as (text) ]
        """
        try:
            result  =  float ( raw )
            return result
        except ValueError:
            raise IOError, ( "Invalid %s field value, expecting a "
                             "float: [%s]" % ( text, raw ) )


# - - -   C o r n e r S e t . g e o C r o p   - - -

    def geoCrop ( self, terraBox ):
        "Return a new CornerSet for all slots intersecting terraBox."

        #-- 1 --
        # [ newSet  :=  a new, empty CornerSet
        #   swSlot  :=  self's slot for the terraBox.sw corner
        #   nwSlot  :=  self's slot for the terraBox.nw corner
        #   neSlot  :=  self's slot for the terraBox.ne corner
        #   seSlot  :=  self's slot for the terraBox.se corner ]
        newSet    =  CornerSet()
        nwCorner  =  TerraPosition ( terraBox.ne.latRad,
                                     terraBox.sw.lonRad )
        seCorner  =  TerraPosition ( terraBox.sw.latRad,
                                     terraBox.ne.lonRad )
        print terraBox.ne, terraBox.sw
        try:
            swSlot    =  self.getSlotByLatLon ( terraBox.sw )
            nwSlot    =  self.getSlotByLatLon ( nwCorner )
            neSlot    =  self.getSlotByLatLon ( terraBox.ne )
            seSlot    =  self.getSlotByLatLon ( seCorner )
        except KeyError:
            raise IOError, "Can't crop this area due to missing tiles."

        #-- 2 --
        # [ newBase   :=  minimal values of (col,row) from
        #                 (swSlot, nwSlot, neSlot, and seSlot)
        #   newLimit  :=  maximal values of (col,row) from
        #                 (swSlot, nwSlot, neSlot, and seSlot), with
        #                 one added to both for the outer corner row ]
        newBase   =  ( min ( swSlot.slotCR[0],      # Min. col from W side
                             nwSlot.slotCR[0] ),
                       min ( swSlot.slotCR[1],      # Min. row from S side
                             seSlot.slotCR[1] ) )
        newLimit  =  ( max ( neSlot.slotCR[0],      # Max. col from E side
                             seSlot.slotCR[0] ) + 1,
                       max ( nwSlot.slotCR[1],      # Max. row from N side
                             neSlot.slotCR[1] ) + 1 )

        #-- 3 --
        # [ newSet  +:=  corners (cN,rN) from self such that
        #       (newBase[0] <= cN <= newLimit[0]) and
        #       (newBase[1] <= rN <= newLimit[1]) ]
        for  col in range ( newBase[0], newLimit[0] + 1 ):
            for  row in range ( newBase[1], newLimit[1] + 1 ):
                #-- 3 body --
                # [ if self.__crMap has a key (col,row) ->
                #       newSet  +:=  self.__crMap[(col,row)]
                #   else -> I ]
                try:
                    newSet.addCorner ( self.__crMap[(col,row)] )
                except KeyError:
                    pass

        #-- 4 --
        return newSet


# - - -   C o r n e r S e t . w r i t e F i l e   - - -

    def rowMajorCmp(self,cr1,cr2):
        """Compare function to sort (col,row) pairs by row, then col"""
        return cmp((cr1[1],cr1[0]), (cr2[1],cr2[0]))
    
    def writeFile ( self, fileName ):
        "Write self to a new corners file."
        #-- 1 --
        # [ if we can open fileName new ->
        #     outFile  :=  outFile so opened
        #   else ->
        #     raise IOError ]
        outFile  =  open ( fileName, "w" )

        #-- 2 --
        # [ outFile  +:=  lines representing corners in self ]
        colRowList  =  self.__crMap.keys()
        colRowList.sort(self.rowMajorCmp)
        for  colRowKey in colRowList:
            self.__writeLine ( outFile, self.__crMap[colRowKey] )
        outFile.close()


# - - -   C o r n e r S e t . _ _ w r i t e L i n e   - - -

    def __writeLine ( self, outFile, tileCorner ):
        """Write one line to a corners file.

          [ (outFile is a writeable file) and
            (tileCorner is a TileCorner object) ->
              outFile  +:=  a line representing tileCorner ]
          **** NOTE ****
          **** Keep the output format the same as that expected by
          **** the input line parsing logic in self.__scanLine().
        """
        outFile.write ( "%d %d %d "     # Pixel size, tile X, tile Y
            "%.7f %.7f "                # Latitude, longitude
            "%d %d %d\n" %                # UTM zone/easting/northing
            ( tileCorner.magCode,
              tileCorner.slotCR[0], tileCorner.slotCR[1],
              tileCorner.latLon.latDeg, tileCorner.latLon.lonDeg,
              tileCorner.utm.zone, tileCorner.utm.easting,
              tileCorner.utm.northing ) )



# - - - - -   c l a s s   T i l e S l o t   - - - - -

class TileSlot:
    """Represents the place where one tile goes.

      State/Invariants:
        .__swCorner:    [ (self.sw.latLon.lonRad, self.sw.latLon.latRad) ]
        .__nwCorner:    [ (self.nw.latLon.lonRad, self.nw.latLon.latRad) ]
        .__seCorner:    [ (self.se.latLon.lonRad, self.se.latLon.latRad) ]
        .__neCorner:    [ (self.ne.latLon.lonRad, self.ne.latLon.latRad) ]
    """

# - - -   T i l e S l o t . _ _ s t r _ _   - - -

    def __str__ ( self ):
        "Render self as a string."
        return ( "%s: %f %f %f %f" %
                 (self.slotCR,
                  self.sw.latLon.latDeg, self.ne.latLon.latDeg,
                  self.sw.latLon.lonDeg, self.ne.latLon.lonDeg) )


# - - -   T i l e S l o t . _ _ i n i t _ _   - - -

    def __init__ ( self, slotCR, sw, nw, se, ne ):
        "Constructor for TileSlot."

        #-- 1 --
        self.slotCR  =  slotCR
        self.sw      =  sw
        self.nw      =  nw
        self.se      =  se
        self.ne      =  ne
        self.__swCorner  =  (sw.latLon.lonRad, sw.latLon.latRad)
        self.__nwCorner  =  (nw.latLon.lonRad, nw.latLon.latRad)
        self.__seCorner  =  (se.latLon.lonRad, se.latLon.latRad)
        self.__neCorner  =  (ne.latLon.lonRad, ne.latLon.latRad)

        #-- 2 --
        # [ self.bbox  :=  as invariant ]
        minLatRad  =  min ( sw.latLon.latRad, se.latLon.latRad )
        maxLatRad  =  max ( nw.latLon.latRad, ne.latLon.latRad )
        minLonRad  =  min ( nw.latLon.lonRad, sw.latLon.lonRad )
        maxLonRad  =  max ( ne.latLon.lonRad, se.latLon.lonRad )
        self.bbox  =  TerraBox ( TerraPosition(minLatRad,minLonRad),
                                 TerraPosition(maxLatRad,maxLonRad) )


# - - -   T i l e S l o t . c o n t a i n s L a t L o n   - - -

    def containsLatLon ( self, latLon ):
        "Does self contain latLon?"

        #-- 1 --
        # [ if latLon is not within self.bbox ->
        #     return 0
        #   else -> I ]
        if  not self.bbox.contains ( latLon ):
            return 0

        #-- 2 --
        # [ xy  :=  latLon's display coordinates relative to the *NW*
        #           corner of self ]
        xy  =  self.latLonToDisplay(latLon)

        #-- 3 --
        # [ if xy is not within self's display coordinates ->
        #     return 0
        #   else -> return 1 ]
        if  ( ( 0 <= xy[0] < TILE_WIDE ) and
              ( 0 <= xy[1] < TILE_HIGH ) ):
            return 1
        else:
            return 0


# - - -   T i l e S l o t . c o n t a i n s U T M   - - -

    def containsUTM ( self, utm ):
        """Does utm fall within this tile?

            We assume that self and utm are in the same zone.  Someday
            we might be able to handle the case where they aren't, but
            at the moment I don't have a good source of UTM<->lat-lon
            conversion algorithms.
        """

        #-- 1 --
        if  self.sw.utm.zone != utm.zone:
            raise ValueError, ( "Zone mismatch: tile zone %d, point zone "
                                "%d." % ( self.sw.utm.zone, utm.zone ) )

        #-- 2 --
        # [ nLimit  :=  northing of self's northern edge
        #   eLimit  :=  easting of self's eastern edge ]
        eLimit  =  self.sw.easting + self.sw.pixelSize * TILE_WIDE
        nLimit  =  self.sw.northing + self.sw.pixelSize * TILE_HIGH

        #-- 3 --
        if  ( ( self.sw.utm.easting <= utm.easting < eLimit) and
              ( self.sw.utm.northing <= utm.northing < nLimit ) ):
            return 1
        else:
            return 0


# - - -   T i l e S l o t . l a t L o n T o D i s p l a y   - - -

    def latLonToDisplay ( self, latLon ):
        "Find the display coordinates of a given lat-lon."

        #-- 1 --
        # [ p   :=  (lon,lat) tuple of latLon in radians ]
        p  =  (latLon.lonRad, latLon.latRad)

        #-- 2 --
        # [ dx, dy  :=  display coordinates of p transformed from
        #       self's lat-lon space to self's display space ]
        dx, dy  =  tilexform ( p,
            self.__swCorner, self.__nwCorner,
            self.__seCorner, self.__neCorner,
            DISPLAY_SW, DISPLAY_NW, DISPLAY_SE, DISPLAY_NE )

        #-- 3 --
        return (int(dx), int(dy))


# - - -   T i l e S l o t . d i s p l a y T o L a t L o n   - - -

    def displayToLatLon ( self, p ):
        """Convert display coordinates to the corresponding lat-lon.

          [ p is an image coordinate in self as a 2-sequence ->
              return the latLon of that pixel as a TerraPosition ]
        """

        #-- 1 --
        # [ dLon, dLat  :=  display coordinates of p transformed from
        #       self's display space to self's lat-lon space ]
        dLon, dLat  =  tilexform ( p,
            DISPLAY_SW, DISPLAY_NW, DISPLAY_SE, DISPLAY_NE,
            self.__swCorner, self.__nwCorner,
            self.__seCorner, self.__neCorner )

        #-- 3 --
        return TerraPosition ( dLat, dLon )


# - - - - -   c l a s s   T i l e C o r n e r   - - - - -

class TileCorner:
    "Represents the southwest corner of a tile."


# - - -   T i l e C o r n e r . _ _ i n i t _ _   - - -

    def __init__ ( self, magCode, slotCR, latLon, utm ):
        "Constructor for TileCorner."
        self.magCode    =  magCode
        self.slotCR     =  slotCR
        self.latLon     =  latLon
        self.utm        =  utm


# - - -   T i l e C o r n e r . _ _ c m p _ _   - - -

    def __cmp__ ( self, other ):
        "Compare function: (ascending row, ascending column)"
        return cmp ( ( self.slotCR[1], self.slotCR[0] ),
                     ( other.slotCR[1], other.slotCR[0] ) )



# - - - - -   c l a s s   U T M   - - - - -

class UTM:
    "Represents a Universal Transverse Mercator coordinate."
    def __init__ ( self, zone, easting, northing ):
        "Constructor for UTM."
        self.zone      =  zone
        self.easting   =  easting
        self.northing  =  northing



# - - - - -   c l a s s   S l o t P o i n t   - - - - -

class SlotPoint:
    "Represents a combination of slot-col-row and a coordinate on that tile"
    def __init__ ( self, slotCR, displayXY ):
        "Constructor for SlotPoint"
        self.slotCR     =  slotCR
        self.displayXY  =  displayXY
