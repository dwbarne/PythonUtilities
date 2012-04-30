"""terrapos.py:  Terrestrial position objects
        $Revision: 1.28 $  $Date: 2005/02/12 00:30:08 $

    An important design goal of this package is to avoid pathological
    back conversion errors, such as (107d 54' 0") -> (107d 53' 60").
    The base class, TerraPosition, is a generic representation optimized
    for spherical geometry calculations; the derived class LatLon carries
    both the original mixed-units form and the TerraPosition form so that
    no back-conversion is necessary.

  Exports:
    def degRad(deg):            Convert degrees to radians
      [ deg is an angle in degrees as a float ->
          return that angle in radians as a float ]
    def radDeg(rad):            Convert radians to degrees
      [ rad is an angle in radians as a float ->
          return that angle in degrees as a float ]
    def feetToAngle(feet):      Convert feet to distance angle
      [ feet is a distance in feet ->
          return the angle in radians subtended by that distance from the
          center of the earth ]
    def angleToFeet(angle):     Convert distance angle to feet
      [ angle is an angle in radians ->
          return the distance in feet on the surface subtended by
          that angle from the center of the earth ]
    def degDMS(deg):
      [ deg is an angle in degrees ->
          return deg as a (degrees,minutes,seconds) tuple ]
    def dmsDeg(dms):
      [ dms is a 2- or 3-tuple as (degrees,minutes,seconds) ->
          return dms as degrees with fraction ]
    def degDMSfuzz(deg, secDigits):
      [ (deg is an angle in degrees) and
        (digits is a nonnegative integer) ->
          return deg as a (degrees,minutes,seconds) tuple so that
          when the seconds part is formatted with secDigits digits
          of precision, that part will never display as >= 60 ]
        #--
        # This avoids the pathological conversion error where
        # (107d 54' 0") might display as (107d 53' 60").  For
        # example, if you are using "%.1f" to display seconds,
        # use degDMSfuzz(deg, 1) and the seconds will never be "60.0".
        #--

    class TerraPosition:    Represents a position on Terra's surface
        TerraPosition(latRad, lonRad, altFeet=None, datumName=None):
          [ ( ( latRad is a signed north latitude in radians ) and
              ( lonRad is a signed east latitude in radians ) and
              ( altFeet is an altitude in feet, None for unknown ) and
              ( datumName is the name of the map datum, defaulting to
                DEFAULT_DATUM ) ) ->
              return a new TerraPosition representing those values ]
        .latRad:        [ as passed to constructor, read-only ]
        .lonRad:        [ as passed to constructor, read-only ]
        .latDeg:        [ self.latRad in degrees, read-only ]
        .lonDeg:        [ self.lonRad in degrees, read-only ]
        .altFeet:       [ as passed to constructor, read-only ]
        .datumName:
          [ as passed to constructor, defaulting to DEFAULT_DATUM ]
        .__str__(self):
          [ return self represented as a string ]
        .__cmp__(self, other):
          [ other is a TerraPosition ->
              return the usual compare function sorting values by
              (ascending latitude, ascending longitude) ]
        .crowFeet(other):
          [ other is a TerraPosition ->
              return the distance from self to other "as the crow flies",
              that is, at a constant bearing and a constant altitude
              sufficient to clear the terrain ]
        .bearing(other):
          [ other is a TerraPosition ->
              return the bearing from self to other in radians ]
        .offset(bearing,distangle):
          [ (bearing is the bearing to a point P in radians) and
            (distangle is the angle from self to P in radians subtended
            by the center of the earth) ->
              return P as a TerraPosition ]
        .offsetFeet(bearing, feet):
          [ (bearing is the bearing to a point P in radians) and
            (feet is the distance in feet to point P) ->
              return P as a TerraPosition ]

    class LatLon(TerraPosition):    Represents a lat-long position
        LatLon(lat, lon, altFeet=None, datumName=None):
          [ (lat is a latitude as a degree-value) and
            (lon is a longitude as a degree-value) and
            (altFeet and datumName are as in the parent class) ->
              return a new LatLon object with those values ]
        .lat:           [ as passed to constructor, read-only ]
        .lon:           [ as passed to constructor, read-only ]
        .latVar:
          [ a DegVariant object representing the absolute value
            of self's latitude ]
        .latNS:
          [ if self is at or north of the equator -> "N"
            else -> "S" ]
        .lonVar:
          [ a DegVariant object representing the absolute value
            of self's longitude ]
        .lonEW:
          [ if self is at or east of longitude 0 -> "E"
            else -> "W" ]

    class DegVariant:               Represents an angle in external form
        DegVariant(value):
          [ value is a degree-value ->
              return a DegVariant representing value in its external
              and internal forms ]
        .value:
          [ if value passed to constructor was a scalar ->
              its absolute value as a 1-element sequence
            else ->
              absolute value of argument passed to constructor ]
        .sign:          [ -1 if value was negative, 1 if positive ]
        .__str__(self):
          [ return self as a string with the precision as created ]
        .deg:
          [ if value was a scalar or 1-tuple ->
              absolute value of degrees, with the same type
            else ->
              abs(value[0]) ]
        .min:
          [ if value was a scalar or 1-tuple -> None
            else -> abs(value[1]) ]
        .sec:
          [ if value was not a 3-tuple -> None
            else -> abs(value[2]) ]
        .degFloat:
          [ self's angle as signed, float decimal degrees ]
        .neg():
          [ return a new DegVariant with the opposite sign of self ]

    def scanAngle ( raw ):
      [ raw is a string ->
          if raw is a generic-angle ->
            return a degree-value representing that angle
          else -> raise ValueError ]

    def scanLat ( raw ):
      [ raw is a string ->
          if raw is a generic-lat ->
            return a degree-value representing that angle
          else -> raise ValueError ]

    def scanLon ( raw ):
      [ raw is a string ->
          if raw is a generic-lon ->
            return a degree-value representing that angle
          else -> raise ValueError ]

    def scanLatLon ( raw ):
      [ raw is a string ->
          if raw is a (generic-lat + generic-lon) ->
            return a LatLon representing that location
          else -> raise ValueError ]

    class TerraBox:    Represents a rectangle in lat-lon space
        TerraBox ( p1, p2 ):
          [ p1 and p2 are two endpoints of a main diagonal of a
            rectangle in lat-lon space as TerraPosition objects ->
              return a new TerraBox object that represents that
              rectangle ]
        .sw:   [ self's southwest corner as a TerraPosition ]
        .ne:   [ self's northeast corner as a TerraPosition ]
        .__str__(self): [ return self as a string ]
        .contains(p):
          [ p is a TerraPosition ->
              if self contains p ->
                return 1
              else -> return 0 ]
        .overlaps(b2):
          [ b2 is a TerraBox object ->
              if self and b2 share no points ->
                return 0
              else -> return 1 ]
        .union(b2):
          [ b2 is a TerraBox object ->
              return a new TerraBox object representing the
              smallest rectangle containing self and b2 ]
        .intersect(b2):
          [ b2 is a TerraBox object ->
              if self and b2 do not overlap ->
                return None
              else ->
                return a new TerraBox object representing the
                intersection of self and b2 ]
            
================================================================
Formulas from the Aviation Formulary V1.40 at:

    http://williams.best.vwm.net/avform.htm

The formulary treats West Longitude as positive, while the
TerraPosition treats West Longitude as negative.  Formulae have
been modified appropriately using the identities:

    sin(-x) = -sin(x)         cos(-x) = cos(x)
================================================================
"""

#================================================================
# Specification functions
#----------------------------------------------------------------
# degree-value ==
#   an angle specified as any of:
#     (a)   Degrees as a scalar int or float
#     (b)   Degrees as a 1-tuple with int or float degrees
#     (c)   A 2-tuple (D,M) where D is int and M is int or float
#     (d)   A 3-tuple (D,M,S) where D and M are int and S is
#           int or float
#   For negative angles, all values must have the same sign.
#--
#   A degree-value is represented internally as an object of type
#   DegVariant, which preserves all the original values and their
#   types so that no unnecessary precision is displayed upon
#   conversion to a string.  This also solves the design
#   problem of avoiding pathological back-conversions.
#----------------------------------------------------------------
# generic-angle ==
#   a string consisting of one or more digits followed by an
#   optional decimal point (".") and one or more digits, but
#   interpreted as an angle in mixed units depending on the
#   number of digits before the decimal (or all digits if there
#   is no decimal) according to this table:
#       Digits      Interpretation
#       ------      --------------
#           1       D degrees
#           2       DD degrees
#           3       DDD degrees
#           4       DDMM degrees and minutes
#           5       DDDMM degrees and minutes
#           6       DDMMSS degrees/minutes/seconds
#           7       DDDMMSS degrees/minutes/seconds
#   and the fraction, if any, belongs to the smallest unit.
#--
#   Examples:
#           1       1d                      1.1     1.1d
#          23       23d                    23.4     23.4d
#         179       179d                  179.56    179.56d
#        3406       34d 06'              3406.15    34d 6.15'
#       10753       107d 53'            10753.54    107d 53.54'
#      340639       34d 06' 39"        340639.2     34d 6' 39.2"
#     1075314       107d 53' 14"      1075314.6     107d 53' 14.6"
#----------------------------------------------------------------
# generic-lat ==
#   a latitude as a generic-angle followed by "n", "N", "s", or "S"
#----------------------------------------------------------------
# generic-lon ==
#   a longitude as a generic-angle followed by "e", "E", "w", or "W"
#----------------------------------------------------------------


#================================================================
# Imports
#----------------------------------------------------------------

from math import *              # For pi, sin(), sqrt(), etc.
import re                       # Regular expression package


#================================================================
# Manifest constants
#----------------------------------------------------------------

DEFAULT_DATUM  =  "NAD-27"          # Map datum for most U.S. topo maps
PI_OVER_180  =  pi / 180.0
PI_OVER_TWO  =  pi / 2.0
TWO_PI       =  pi * 2.0


#--
# The figure for the radius of the earth in miles is from the
# Aviation Formulary.  It is intermediate between the equatorial
# radius (3963) and polar radius (3950) given in CRC Math Tables,
# 15th ed.
#--

R_EARTH_FT   =  (3959.0 * 5280)     # Radius of earth in feet
FEET_PER_METER  =  3.28084          # Feet per meter

#--
# Derivation of accuracies for external display:
#   (a)  24730 mi       Earth diameter
#   (b)     68.70 mi    Per degree of latitude = (a) / 360
#   (c)      1.145 mi   Per minute of latitude = (b) / 60
#   (d)      0.0019 mi  Per second of latitude = (c) / 60
#   (e)    100.75 ft    Per second of latitude = (d) * 5280
# Since no GPS claims to be better than 3 meters, roughly 10 ft,
# an accuracy of 0.1 second should be sufficient for mapping,
# or 0.001 minute (==0.06 second), or 0.00001 degree (==0.036 second).
#
# Accuracies for degrees, recommend seven digits in the fraction:
#   (a) 68.70 mi        Per degree of latitude
#   (b) 3,627,736 ft    Per degree of latitude
#   (c) 36 ft           Per .00001 degree of latitude
#   (d) 4 ft            Per .000001 degree of latitude
#   (e) 5 in            Per .0000001 degree of latitude; should be plenty.
#--

L_LAT_DEG  =  2             # Number of digits in latitude degrees
L_LON_DEG  =  3             # Number of digits in longitude degrees
F_DEG      =  5             # Fraction length for degrees
L_DEG      =  L_LAT_DEG + F_DEG + 2     # Degrees with sign and decimal
F_MIN      =  3             # Fraction length for minutes
L_MIN      =  F_MIN + 3     # Minutes with tens, units, and decimal point
F_SEC      =  1             # Fraction length for seconds
L_SEC      =  F_SEC + 3     # Seconds with tens, units, and decimal point


# - - -   d e g R a d   - - -
# - - -   r a d D e g   - - -

def degRad ( deg ):
    """Convert degrees to radians

      [ if deg is a number in degrees ->
          return the equivalent float in radians ]
    """
    return deg * PI_OVER_180

def radDeg ( rad ):
    """Convert radians to degrees

      [ if rad is a float in radians ->
          return the equivalent in degrees ]
    """
    return rad / PI_OVER_180


# - - -   f e e t T o A n g l e   - - -
# - - -   a n g l e T o F e e t   - - -

def feetToAngle(feet):
    "Convert feet to distance angle"
    return feet / R_EARTH_FT

def angleToFeet(angle):
    "Convert distance angle to feet"
    return angle * R_EARTH_FT


# - - -   d e g D M S   - - -
# - - -   d m s D e g   - - -

def degDMS ( deg ):
    "Degrees to degrees/minutes/seconds."
    absDeg  =  abs(deg)
    sign    =  deg/absDeg
    degUnits, degFraction  =  divmod ( absDeg, 1.0 )
    minUnits, minFraction  =  divmod ( degFraction * 60.0, 1.0 )
    seconds                =  minFraction * 60.0
    return (sign*degUnits, sign*minUnits, sign*seconds)

def dmsDeg ( dms ):
    "Degrees/minutes[/seconds] to degrees."
    if  len(dms) < 3:
        d,m  =  dms
        s    =  0.0
    else:
        d,m,s  =  dms
    if  d<0:
        d,m,s,sign  =  -d, -m, -s, -1.0
    else:
        sign  =  1.0

    return sign*(d+(m/60.0)+(s/3600.0))


# - - -   d e g D M S f u z z    - - -

def degDMSfuzz ( deg, secDigits ):
    """Convert degrees to deg/min/sec avoiding the `60 seconds' syndrome.

        If we're displaying integral seconds, then seconds values
        whose fraction is in the range [0.5, 1.0) will round up,
        which will make a value like 59.6 display as 60, which is bad.
        So for that case, we can subtract 0.5 seconds from the degree
        value before conversion to avoid the problem.  Similarly,
        if we're displaying seconds with tenths, the trouble range is
        values with fractions in [0.95, 1.0).  If hundredths, the
        trouble range is [0.995, 1.0).  In general, for D digits
        of precision, subtracting (0.5/(10**D)) will prevent the
        `60 seconds syndrome.'

        However, we don't want to apply the fuzz unless it actually
        will cause rounding up.
    """

    #-- 1 --
    # [ fuzz   :=  0.5 / ( 10 ** secDigits )
    #   d,m,s  :=  deg converted to (deg,min,sec) ]
    fuzz   =  ( 0.5 / ( 10 ** secDigits ) )
    d,m,s  =  degDMS ( deg )

    #-- 2 --
    # [ if dms[2] >= (60-fuzz)
    #     return (deg-fudge)
    #   else ->
    #     return dms ]
    if  s >= (60 - fuzz):
        return (d, m, s - fuzz )
    else:
        return (d, m, s)



# - - - - -   c l a s s   T e r r a P o s i t i o n   - - - - -

class TerraPosition:
    """Terrestrial position object; parent class for LatLon, UTM, etc.
    """


# - - -   T e r r a P o s i t i o n . _ _ i n i t _ _   - - -

    def __init__ ( self, latRad, lonRad, altFeet=None, datumName=None):
        "Constructor for TerraPosition"
        self.latRad, self.lonRad  =  latRad, lonRad
        self.latDeg  =  radDeg ( self.latRad )
        self.lonDeg  =  radDeg ( self.lonRad )
        self.altFeet  =  altFeet

        if  datumName is None:  self.datumName  =  DEFAULT_DATUM
        else:                   self.datumName  =  datumName



# - - -   T e r r a P o s i t i o n . _ _ s t r _ _   - - -

    def __str__ ( self ):
        """Convert self to string form.

            0         1       1
            0123456789012345678
            -dd.dddd -ddd.dddd
        """
        return ( "%8.4f %9.4f" %
                 ( radDeg ( self.latRad ), radDeg ( self.lonRad ) ) )


# - - -   T e r r a P o s i t i o n . _ _ c m p _ _   - - -

    def __cmp__ ( self, other ):
        "Compare two TerraPosition objects"
        return cmp( (self.latRad, self.lonRad),
                    (other.latRad, other.lonRad) )


# - - -   T e r r a P o s i t i o n . c r o w F e e t   - - -

    def crowFeet ( self, other ):
        "Compute the distance in feet as the crow flies."
        d  =  2.0 * asin (
                sqrt ( ( sin ( ( self.latRad-other.latRad ) / 2 ) ) **2 +
                       cos(self.latRad) * cos(other.latRad) *
                       ( sin ( ( other.lonRad-self.lonRad ) / 2 ) ) ** 2
                     )
                         )
        return d * R_EARTH_FT


# - - -   T e r r a P o s i t i o n . b e a r i n g   - - -

    def bearing ( self, other ):
        """Compute the bearing from self to other (0 == due north).

            Source:  Aviation Formulary V1.40,
            http://williams.best.vwh.net/avform.htm
        """
        rise  =  sin ( other.lonRad - self.lonRad ) * cos ( other.latRad )
        run   =  ( cos ( self.latRad ) * sin ( other.latRad ) -
                   ( sin ( self.latRad ) * cos ( other.latRad ) *
                     cos ( self.lonRad - other.lonRad ) ) )
        result  =  atan2 ( rise, run ) % TWO_PI
        return result


# - - -   T e r r a P o s i t i o n . o f f s e t   - - -

    def offset ( self, bearing, distangle ):
        """Return the position at a given bearing and distance.

            Source:  Aviation Formulary V1.40,
            http://williams.best.vwh.net/avform.htm
        """
        lat  =  asin ( sin ( self.latRad ) * cos ( distangle ) +
                       ( cos ( self.latRad ) * sin ( distangle ) *
                         cos ( bearing ) ) )

        lon  =  ( ( ( - self.lonRad -
                      asin ( sin ( bearing ) * sin ( distangle ) /
                             cos ( lat ) ) + pi ) %
                    TWO_PI ) - pi )
        return TerraPosition ( lat, -lon )



# - - -   T e r r a P o s i t i o n . o f f s e t F e e t   - - -

    def offsetFeet ( self, bearing, feet ):
        """Return the position at a given bearing and distance in feet."""
        angle  =  feetToAngle ( feet )
        return  self.offset ( bearing, angle )



# - - - - -   c l a s s   L a t L o n   - - - - -

class LatLon(TerraPosition):
    "Represents a terrestrial position as latitude/longitude."


# - - -   L a t L o n . _ _ i n i t _ _   - - -

    def __init__ ( self, lat, lon, altFeet=None, datumName=None):
        "Constructor for LatLon"

        #-- 1 --
        # [ self.lat     :=  as invariant
        #   self.lon     :=  as invariant
        #   self.latVar  :=  as invariant
        #   self.latNS   :=  as invariant
        #   self.lonVar  :=  as invariant
        #   self.lonEW   :=  as invariant ]
        self.lat     =  lat
        self.lon     =  lon
        self.latVar  =  DegVariant ( lat )
        self.lonVar  =  DegVariant ( lon )

        if  self.latVar.sign >= 0:  self.latNS  =  "N"
        else:                       self.latNS  =  "S"

        if  self.lonVar.sign >= 0:  self.lonEW  =  "E"
        else:                       self.lonEW  =  "W"

        #-- 2 --
        # [ self  :=  self with parent class invariants established ]
        TerraPosition.__init__ ( self,
            degRad ( self.latVar.degFloat ),
            degRad ( self.lonVar.degFloat ),
            altFeet, datumName )



# - - -   L a t L o n . _ _ s t r _ _   - - -

    def __str__ ( self ):
        """Convert a LatLon to string form.

            It is safe to discard the first two characters of the
            latitude, because there will never be a minus sign,
            and the high-order digit will always be zero.  Similarly,
            it is safe to discard the first character of the
            longitude, because it will never be a minus sign.
        """
        #-- 1 --
        exLat  =  str(self.latVar)
        exLon  =  str(self.lonVar)
        return ( "%s%s %s%s" %
                 ( exLat[2:], self.latNS,
                   exLon[1:], self.lonEW ) )



# - - - - -   c l a s s   D e g V a r i a n t   - - - - -

class DegVariant:
    "Represents a signed angle in external and internal form."


# - - -   D e g V a r i a n t . _ _ i n i t _ _   - - -

    def __init__ ( self, value ):
        "Constructor for DegVariant."

        #-- 1 --
        # [ if value has type int or float ->
        #     self.value  :=  value as a 1-tuple
        #   else ->
        #     self.value  :=  value ]
        if  ( ( type(value) is int) or ( type(value) is float ) ):
            self.value  =  (value,)
        else:
            self.value  =  value

        #-- 2 --
        # [ if  self.value[0] is negative ->
        #     self.value  :=  self.value with its elements negated
        #     self.sign  :=  -1
        #   else ->
        #     self.sign  :=  1 ]
        if  self.value[0] < 0:
            self.sign  =  -1
            self.value  =  map ( abs, self.value )
        else:
            self.sign  =  1

        #-- 3 --
        self.deg  =  self.value[0]

        #-- 4 --
        if  len(self.value) == 1:
            self.min  =  self.sec  =  None
        else:
            self.min  =  self.value[1]
            if  len(self.value) > 2:
                self.sec  =  self.value[2]
            else:
                self.sec  =  None

        #-- 5 --
        # [ self.degFloat  :=  (angle (self.deg degrees + self.min minutes +
        #       self.sec seconds) as float degrees) * self.sign ]
        self.degFloat  =  float ( self.deg )

        if  self.min is not None:
            self.degFloat  +=  self.min / 60.0
            if  self.sec is not None:
                self.degFloat  +=  self.sec / 3600.0

        self.degFloat  *=  self.sign


# - - -   D e g V a r i a n t . _ _ s t r _ _   - - - -

    def __str__ ( self ):
        "Return self in string form."

        #-- 1 --
        if  self.sign < 0:  signChar  =  "-"
        else:               signChar  =  " "

        #-- 2 --
        if  type ( self.deg ) is float:
            return "%s%0*.*fd"% ( signChar, L_DEG, F_DEG, self.deg )
        else:
            degOut  =  "%s%0*dd"% ( signChar, L_LON_DEG, self.deg )

        #-- 3 --
        if  self.min is None:
            return degOut
        elif  type ( self.min ) is float:
            return "%s%0*.*f'"% ( degOut, L_MIN, F_MIN, self.min )
        else:
            minOut  =  "%02d'" % ( self.min )

        #-- 4 --
        if  self.sec is None:
            return "%s%s" % ( degOut, minOut )
        elif  type ( self.sec ) is int:
            return '%s%s%02d"' % ( degOut, minOut, self.sec )
        else:
            return '%s%s%0*.*f"'% ( degOut, minOut, L_SEC, F_SEC, self.sec )


# - - -   D e g V a r i a n t . n e g   - - -

    def neg ( self ):
        "Return self, negated."
        return DegVariant (  [ -x*self.sign for x in self.value ] )



# - - -   s c a n A n g l e   - - -

UNITS_F  =  "u"             # Units (up to decimal if any, or all digits)
FRAC_F   =  "f"             # Fraction (decimal & trailing digits if any)
angPat   =  re.compile (    # Regular expression for angles
    r'(?P<%s>'              # Start group UNITS_F
        r'[0-9]+'           # One or more digits
    r')'                    # End group UNITS_F
    r'(?P<%s>'              # Start group FRAC_F
        r'\.'               # Decimal point
        r'[0-9]+'           # Digits after the decimal, at least one
    r')?'                   # End group; this entire group is optional.
    r'$'                    # Anchor, ensures whole string is matched
    % (UNITS_F, FRAC_F) )

def scanAngle ( raw ):
    "Convert a generic-angle string to a degree-value."

    #-- 1 --
    # [ if raw matches angPat ->
    #     m  :=  a Match object representing that match
    #   else -> raise ValueError ]
    m  =  angPat.match ( raw )
    if  m is None:
        raise ValueError, ( "Not a valid angle: `%s'" % raw )

    #-- 2 --
    # [ units  :=  field from m matching UNITS_F
    #   frac   :=  field from m matching FRAC_F, or None if omitted ]
    units  =  m.group ( UNITS_F )
    frac   =  m.group ( FRAC_F )

    #-- 3 --
    # [ if (units+frac) is a valid generic-angle ->
    #     return a DegVariant representing that angle
    #   else -> raise ValueError ]
    return checkAngle ( units, frac )


# - - -   c h e c k A n g l e   - - -

def checkAngle ( units, frac ):
    """Convert (units+frac) to a DegVariant

      [ (units is the units digits of a generic-angle as a string) and
        (frac is the decimal and fraction, or None if missing) ->
          if (units+frac) is a valid generic-angle ->
            return a degree-value representing that angle
          else -> raise ValueError ]
    """

    #-- 1 --
    # [ if units is a valid units part of a generic-angle ->
    #     dmsTuple  :=  a degree-value representing units
    #   else -> raise ValueError ]
    if  len(units) <= 3:
        dmsTuple  =  (int(units),)
    elif  len(units) <= 5:
        dmsTuple  =  (int(units[:-2]), int(units[-2:]))
    elif  len(units) <= 7:
        dmsTuple  =  (int(units[:-4]), int(units[-4:-2]), int(units[-2:]))
    else:
        raise ValueError, "Angles must have 1 to 7 units digits."

    #-- 2 --
    # [ if frac is None ->
    #     I
    #   else ->
    #     dmsTuple  :=  dmsTuple with float(frac) added to its
    #                   last element ]
    if  frac is not None:
        dmsTuple  =  dmsTuple[:-1]+(dmsTuple[-1]+float(frac),)

    #-- 3 --
    return dmsTuple


# - - -   s c a n L a t   - - -

def scanLat ( rawLat ):
    "Check and convert a raw latitude to a degree-value."

    #-- 1 --
    # [ if rawLat ends with "n" or "N" ->
    #     sign      :=  1
    #     rawAngle  :=  rawLat[:-1]
    #   else if rawLat ends with "s" or "S" ->
    #     sign      :=  -1
    #     rawAngle  :=  rawLat[:-1] ]
    if  len(rawLat) < 2:
        raise ValueError, "Latitudes must be at least two characters."
    rawAngle, last  =  rawLat[:-1], rawLat[-1]
    if  ( ( last == "n" ) or ( last == "N" ) ):
        sign  =  1
    elif  ( ( last == "s" ) or ( last == "S" ) ):
        sign  =  -1
    else:
        raise ValueError, "Latitude must end with `n' or `s'."

    #-- 2 --
    # [ if rawAngle is a generic-angle ->
    #     degVar  :=  that angle as a degree-value
    #   else -> raise ValueError ]
    degVar  =  scanAngle ( rawAngle )

    #-- 3 --
    # [ if degVar[0] > 90 ->
    #     raise ValueError
    #   else -> I ]
    if  degVar[0] > 90:
        raise ValueError, "Latitudes cannot exceed 90 degrees."

    #-- 4 --
    # [ if sign < 0 ->
    #     return degVar negated
    #   else ->
    #     return degVar ]
    if  sign < 0:
        return tuple ( [ - x for x in degVar ] )
    else:
        return degVar


# - - -   s c a n L o n   - - -

def scanLon ( rawLon ):
    "Check and convert a raw longitude to a DegVariant."

    #-- 1 --
    # [ if rawLon ends with "e" or "E" ->
    #     sign      :=  1
    #     rawAngle  :=  rawLon[:-1]
    #   else if rawLon ends with "w" or "W" ->
    #     sign      :=  -1
    #     rawAngle  :=  rawLon[:-1] ]
    if  len(rawLon) < 2:
        raise ValueError, "Longitudes must be at least two characters."
    rawAngle, last  =  rawLon[:-1], rawLon[-1]
    if  ( ( last == "e" ) or ( last == "E" ) ):
        sign  =  1
    elif  ( ( last == "w" ) or ( last == "W" ) ):
        sign  =  -1
    else:
        raise ValueError, "Longitude must end with `n' or `s'."

    #-- 2 --
    # [ if rawAngle is a generic-angle ->
    #     degVar  :=  that angle as a DegVariant
    #   else -> raise ValueError ]
    degVar  =  scanAngle ( rawAngle )

    #-- 3 --
    # [ if sign < 0 ->
    #     return degVar negated
    #   else ->
    #     return degVar ]
    if  sign < 0:
        return tuple ( [ - x for x in degVar ] )
    else:
        return degVar


# - - -   s c a n L a t L o n   - - -

LAT_F  =  "y"           # Field identifier for latitude...
LON_F  =  "x"           # ...and longitude in latLonPat

latLonPat  =  re.compile (      # Reg. expr. for (generic-lat + generic-lon)
    r'(?P<%s>'          # Start group LAT_F
      r'[0-9]{1,6}'     # Up to six digits
      r'(\.[0-9]+)?'    # Optional decimal and fraction
      r'[nNsS]'         # North/south latitude
    r')'
    r'\s*'              # Allow any amount of whitespace here
    r'(?P<%s>'          # Start group LON_F
      r'[0-9]{1,7}'     # Up to seven digits
      r'(\.[0-9]+)?'    # Optional decimal and fraction
      r'[eEwW]'         # East/west longitude
    r')'
    % (LAT_F, LON_F) )

def scanLatLon ( rawLatLon ):
    "Check a lat-lon token and convert to a LatLon object."

    #-- 1 --
    # [ if rawLatLon matches latLonPat ->
    #     rawLat  :=  LAT_F field from the match
    #     rawLon  :=  LON_F field from the match
    #   else ->
    #     sys.stderr  +:=  (usage message) + (error message)
    #     stop execution ]
    m  =  latLonPat.match ( rawLatLon )
    if  m is None:
        raise ValueError, "Not a valid lat-lon: '%s'" % rawLatLon
    else:
        rawLat  =  m.group ( LAT_F )
        rawLon  =  m.group ( LON_F )

    #-- 2 --
    # [ if rawLat is a valid generic-lat ->
    #     lat  :=  that latitude as a degree-value
    #     sys.stderr  +:=  (usage message) + (error message)
    #     stop execution ]
    try:
        lat  =  scanLat ( rawLat )
    except ValueError, detail:
        sysargs.usage ( switchSpecs, posSpecs,
            "Invalid latitude: %s" % detail )

    #-- 3 --
    # [ if rawLon is a valid generic-lon ->
    #     lon  :=  that longitude as a degree-value
    #     sys.stderr  +:=  (usage message) + (error message)
    #     stop execution ]
    try:
        lon  =  scanLon ( rawLon )
    except ValueError, detail:
        sysargs.usage ( switchSpecs, posSpecs,
            "Invalid longitude: %s" % detail )

    #-- 4 --
    return LatLon ( lat, lon )       



# - - - - -   c l a s s   T e r r a B o x   - - - - -

class TerraBox:
    "Represents a rectangle in lat-lon space."


# - - -   T e r r a B o x . _ _ i n i t _ _   - - -

    def __init__ ( self, p1, p2 ):
        "Constructor for TerraBox."

        #-- 1 --
        swLat  =  min ( p1.latRad, p2.latRad )
        swLon  =  min ( p1.lonRad, p2.lonRad )
        neLat  =  max ( p1.latRad, p2.latRad )
        neLon  =  max ( p1.lonRad, p2.lonRad )

        #-- 2 --
        self.sw  =  TerraPosition ( swLat, swLon )
        self.ne  =  TerraPosition ( neLat, neLon )


# - - -   T e r r a B o x . _ _ s t r _ _   - - -

    def __str__ ( self ):
        "Return self as a string."
        return "[%s:%s]" % (self.sw,self.ne)


# - - -   T e r r a B o x . c o n t a i n s   - - -

    def contains ( self, p ):
        "Does self contain point p?"
        if  ( ( p.latRad < self.sw.latRad ) or        # Too far south
              ( p.lonRad < self.sw.lonRad ) or        # Too far west
              ( p.latRad > self.ne.latRad ) or        # Too far north
              ( p.lonRad > self.ne.lonRad ) ):
            return 0
        else:
            return 1


# - - -   T e r r a B o x . o v e r l a p s   - - -

    def overlaps ( self, b2 ):
        "Does self overlap b2?"
        if  ( ( b2.ne.latRad < self.sw.latRad ) or  # Too far south
              ( b2.ne.lonRad < self.sw.lonRad ) or  # Too far west
              ( b2.sw.latRad > self.ne.latRad ) or  # Too far north
              ( b2.sw.lonRad > self.ne.lonRad ) ):  # Too far east
            return 0
        else:
            return 1


# - - -   T e r r a B o x . u n i o n   - - -

    def union ( self, b2 ):
        "Returns the smallest rectangle enclosing self and b2."
        swLat  =  min ( self.sw.latRad, b2.sw.latRad )
        swLon  =  min ( self.sw.lonRad, b2.sw.lonRad )
        neLat  =  max ( self.ne.latRad, b2.ne.latRad )
        neLon  =  max ( self.ne.lonRad, b2.ne.lonRad )
        return  TerraBox ( TerraPosition ( swLat, swLon ),
                           TerraPosition ( neLat, neLon ) )


# - - -   T e r r a B o x . i n t e r s e c t   - - -

    def intersect ( self, b2 ):
        "Return the rectangle where self intersects b2, or None if disjoint."

        #-- 1 --
        # [ if self intersects b2 ->
        #     I
        #   else -> return None ]
        if  not self.overlaps ( b2 ):
            return None

        #-- 2 --
        # [ return a new TerraBox representing the overlap of self and b2 ]
        swLat  =  max ( self.sw.latRad, b2.sw.latRad )
        swLon  =  max ( self.sw.lonRad, b2.sw.lonRad )
        neLat  =  min ( self.ne.latRad, b2.ne.latRad )
        neLon  =  min ( self.ne.lonRad, b2.ne.lonRad )
        return TerraBox ( TerraPosition ( swLat, swLon ),
                          TerraPosition ( neLat, neLon ) )
