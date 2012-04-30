"""waypointset.py:  Object to represent an XML waypoint file.

        $Revision: 1.5 $  $Date: 2006/04/26 18:51:10 $

Exports:
  class WaypointSet:    Represents a file full of GPS waypoints.
    WaypointSet(fileName):
      [ fileName is a string ->
          if fileName names a readable, valid waypoint file conforming
          to waypoints.dtd ->
            return a new WaypointSet object representing that file
          else -> raise IOError ]
    .fileName:      [ as passed to constructor, read-only ]
    .geoBox:
      [ if self contains no routes ->
          None
        else ->
          a TerraBox object representing the geographic limits
          of all routes in self ]
    .genRoutes():
      [ generate the routes in self as WayRoute objects in ascending
        order by route name ]
    .getRoute(routeId):
      [ routeId is a string ->
          if self contains a route whose id matches routeId ->
            return a WayRoute object representing that route
          else -> raise KeyError ]

  class WayRoute:       Represents one waypoint route
    WayRoute(name, id):
      [ (name is the route name as a string) and
        (id is the route ID as a string) ->
          return a new, empty Wayroute object with that name & id ]
    .name:          [ as passed to constructor, read-only ]
    .id:            [ as passed to constructor, read-only ]
    .geoBox:
      [ if self contains no waypoints ->
          None
        else ->
          a TerraBox object representing the geographic limits
          of all waypoints in self ]
    .addWaypoint(pt):
      [ pt is a Waypoint object ->
          self  :=  self with pt added as the next waypoint ]
    .genWaypoints():
      [ generate the waypoints in self in file order (generally
        in order of the mapping route ]

  class Waypoint:       Represents one waypoint
    Waypoint(latLon, desc, gpsElevation=None, mapElevation=None,
             mapDatum=None):
      [ (latLon is a LatLon object from terrapos.py) and
        (desc is the description as a string or None) and
        (gpsElevation is the GPS elevation in feet or None) and
        (mapElevation is the map elevation in feet or None) and
        (mapDatum is the map datum name string or None) ->
          return a new Waypoint object with those values ]
    .latLon:        [ as passed to constructor, read-only ]
    .desc:          [ as passed to constructor, read-only ]
    .gpsElevation:  [ as passed to constructor, read-only ]
    .mapElevation:  [ as passed to constructor, read-only ]
    .__str__(self): [ return a string representing self ]
"""


#================================================================
# Imports
#----------------------------------------------------------------

#--
# Standard Python modules
#--
from __future__ import generators       # Allow generators
import xml.dom.minidom as dom           # Document Object Model

#--
# Modules from Shipman's standard Python library
#--
from dom_helpers import *       # Domain Object Model helper routines

#--
# Application-specific modules
#--
from terrapos import *          # TerraPosition, LatLon objects
from waypointsDTD import *      # waypoints.dtd element & attr. names


#================================================================
# Manifest constants
#----------------------------------------------------------------

#--
# XML element node (_N) and attribute (_A) names
#--


# - - - - -   c l a s s   W a y p o i n t S e t   - - - - -

class WaypointSet:
    """Represents a file of GPS waypoints.

      State/invariants:
        .__idMap:
          [ a dictionary whose values are the WayRoute objects representing
            the routes in self, and whose keys are the corresponding
            .id members of those objects ]
        .__routeList:
          [ a list of the WayRoute objects in self in file order ]
    """


# - - -   W a y p o i n t S e t . _ _ i n i t _ _   - - -

    def __init__ ( self, fileName ):
        "Constructor for WaypointSet."

        #-- 1 --
        self.fileName  =  fileName
        self.geoBox    =  None 

        #-- 2 --
        # [ if fileName contains a readable, well-formed XML file ->
        #     doc  :=  a DOM Document object representing fileName
        #   else -> raise IOError ]
        try:
            doc  =  dom.parse ( fileName )
        except Exception, detail:
            raise IOError, ( "Failure to parse input file `%s': %s" %
                             (fileName, detail) )

        #-- 3 --
        # [ if doc is valid according to waypoints.dtd ->
        #     self.__idMap  :=  a dictionary whose values are
        #         the WayRoute objects representing the routes in doc,
        #         and whose keys are the corresponding .id members
        #         of those objects
        #     self.__routeList  :=  a list of those WayRoute objects
        #         in file order
        #     self.geoBox  :=  self.geoBox union (all waypoints added) ]
        self.__readDocument ( doc )


# - - -   W a y p o i n t S e t . _ _ r e a d D o c u m e n t   - - -

    def __readDocument ( self, doc ):
        """Process the XML input document.

          [ doc is a DOM Document object representing a file
            conforming to waypoints.dtd ->
              self.__idMap  :=  a dictionary whose values are
                  the WayRoute objects representing the routes in doc,
                  and whose keys are the corresponding .id members
                  of those objects
              self.__routeList  :=  a list of those WayRoute objects
                  in file order
              self.geoBox  :=  self.geoBox union (all waypoints added) ]
            else -> raise IOError ]
        """

        #-- 1 --
        # [ self.__idMap      :=  a new, empty dictionary
        #   self.__routeList  :=  a new, empty list
        #   root              :=  an Element object representing
        #                         doc's root element ]
        self.__idMap      =  {}
        self.__routeList  =  []
        rootList  =  doc.getElementsByTagName ( ROOT_N )
        if  len(rootList) != 1:
            raise IOError, ( "Missing root <%s> element in `%s'" %
                (ROOT_N, self.fileName) )
        else:
            root  =  rootList[0]

        #-- 2 --
        # [ routeList  :=  a list of ROUTE_N children of root ]
        routeList  =  root.getElementsByTagName ( ROUTE_N )

        #-- 3 --
        # [ if routeList contains only valid elements ->
        #     self.__idMap  +:=  new WayRoute objects representing
        #         the ID_N elements in routeList
        #     self.__routeList  +:=  those WayRoute objects in file order
        #     self.geoBox  :=  self.geoBox union (all waypoints in routeList)
        #   else -> raise IOError ]
        for  routeNode in routeList:
            #-- 3 body --
            # [ if routeNode is valid ->
            #     self.__idMap   +:=  a new WayRoute object representing
            #                         routeNode
            #     self.__routeList  +:=  that WayRoute object
            #     self.geoBox  :=  self.geoBox union (all waypoints in
            #                      that WayRoute object)
            #   else -> raise IOError ]
            self.__readRoute ( routeNode )



# - - -   W a y p o i n t S e t . _ _ r e a d R o u t e   - - -

    def __readRoute ( self, routeNode ):
        """Process one route's worth of waypoints.

          [ routeNode is a DOM Element representing a ROUTE_N element ->
              if routeNode is valid ->
                self.__idMap  +:=  a new WayRoute object representing
                                   routeNode
                self.__routeList  +:=  that WayRoute object
                self.geoBox  :=  self.geoBox union (all waypoints in
                                 that WayRoute object)
              else -> raise IOError ]
        """

        #-- 1 --
        # [ pointList  :=  a list of routeNode's PT_N children
        #   routeName  :=  routeNode's NAME_A attribute ]
        pointList  =  routeNode.getElementsByTagName ( PT_N )
        routeName  =  getAttr ( routeNode, NAME_A, "route name" )
        routeId    =  getAttr ( routeNode, ID_A, "route ID" )

        #-- 2 --
        # [ route  :=  a new, empty WayRoute object named (routeName) ]
        route  =  WayRoute ( routeName, routeId )

        #-- 3 --
        # [ if pointList contains only valid point elements ->
        #       route  +:=  Waypoint objects representing the elements of
        #           pointList in the same order
        #       self.geoBox  :=  self.geoBox union (all waypoints in
        #                        that WayRoute object)
        #   else -> raise IOError ]
        for  ptNode in pointList:
            #-- 3 body --
            # [ ptNode is a DOM Element for a PT_N element ->
            #     if ptnode is valid ->
            #       route  +:=  a new Waypoint object representing ptNode
            #       self.geoBox  :=  self.geoBox union ptNode
            #     else -> raise IOError ]
            self.__readWaypoint ( route, ptNode )

        #-- 4 --
        # [ if self.__idMap has no entry for key (routeId) ->
        #     self.__idMap[routeId]  :=  route
        #   else -> raise IOError ]
        if  self.__idMap.has_key ( routeName ):
            raise IOError, ( "Duplicate route id `%s'" % routeId )
        else:
            self.__idMap[routeId]  =  route
            self.__routeList.append ( route )


# - - -   W a y p o i n t S e t . _ _ r e a d W a y p o i n t   - - -

    def __readWaypoint ( self, route, ptNode ):
        """Read one PT_N element.

          [ (route is a WayRoute object) and
            (ptNode is a DOM Element representing a PT_N element) ->
              if ptNode is valid ->
                route  +:=  a new Waypoint object representing ptNode
                self.geoBox  :=  self.geoBox union ptNode
              else -> raise IOError ]
        """

        #-- 1 --
        # [ latLon   :=  a LatLon object representing the geographic
        #                coordinates from ptNode ]
        latLon  =  self.__findLatLon ( ptNode )

        #-- 2--
        # [ desc     :=  the text from ptNode, or None if no text
        #   gpsElev   :=  GPS_ELEV_A attribute of ptNode, or None
        #   mapElev   :=  MAP_ELEV_A attribute of ptNode, or None
        #   mapDatum  :=  MAP_DATUM_A attribute of ptNode, or None ]
        desc     =  textContent ( ptNode )
        gpsElev  =  getAttr ( ptNode, GPS_ELEV_A )
        mapElev  =  getAttr ( ptNode, MAP_ELEV_A )
        mapDatum  =  getAttr ( ptNode, MAP_DATUM_A )

        #-- 3 --
        # [ waypoint  :=  a new Waypoint object with latLon=latLon,
        #       desc=desc, gpsElevation=gpsElev, mapElevation=mapElev,
        #       and mapDatum=mapDatum ]
        waypoint  =  Waypoint ( latLon, desc, gpsElev, mapElev,
                                mapDatum )

        #-- 4 --
        # [ route  +:=  waypoint ]
        route.addWaypoint ( waypoint )

        #-- 5 --
        # [ self.geoBox  :=  self.geoBox union waypoint ]
        pointBox  =  TerraBox ( waypoint.latLon, waypoint.latLon )
        if  self.geoBox is None:
            self.geoBox  =  pointBox
        else:
            self.geoBox  =  self.geoBox.union ( pointBox )


# - - -   W a y p o i n t S e t . _ _ f i n d L a t L o n   - - -

    def __findLatLon ( self, ptNode ):
        """Convert the point's coordinates to a LatLon object.

          [ ptNode is a DOM Element representing a PT_N node ->
              return a LatLon object representing the coordinates
              from ptNode ]
        """

        #-- 1 --
        # [ rawLatLon  :=  LATLON_A attribute from ptNode ]
        rawLatLon  =  getAttr ( ptNode, LATLON_A )

        #-- 2 --
        # [ if rawLatLon is valid ->
        #     latLon  :=  a new LatLon object made from rawLatLon ]
        latLon  =  scanLatLon ( rawLatLon )

        #-- 4 --
        return latLon


# - - -   W a y p o i n t S e t . g e n R o u t e s   - - -

    def genRoutes ( self ):
        "Generate the routes in self."
        for  route  in self.__routeList:
            yield route
        raise StopIteration


# - - -   W a y p o i n t S e t . g e t R o u t e   - - -

    def getRoute ( self, routeId ):
        "Retrieve a specific route by name."
        return self.__idMap[routeId]



# - - - - -   c l a s s   W a y R o u t e   - - - - -

class WayRoute:
    """Represents one route on which waypoints were taken.

      State/Invariants:
        .__pointList:
          [ a list containing self's Waypoint objects in order ]
    """


# - - -   W a y R o u t e . _ _ i n i t _ _   - - -

    def __init__ ( self, name, id ):
        "Constructor for WayRoute"
        self.name         =  name
        self.id           =  id
        self.geoBox       =  None
        self.__pointList  =  []


# - - -   W a y R o u t e . a d d W a y p o i n t   - - -

    def addWaypoint ( self, waypoint ):
        "Add a waypoint to self."

        #-- 1 --
        # [ self.__pointList  +:=  waypoint ]
        self.__pointList.append ( waypoint )

        #-- 2 --
        # [ self.geoBox  :=  self.geoBox unioned with waypoint ]
        pointBox  =  TerraBox ( waypoint.latLon, waypoint.latLon )
        if  self.geoBox is None:
            self.geoBox  =  pointBox
        else:
            self.geoBox  =  self.geoBox.union ( pointBox )


# - - -   W a y R o u t e . g e n W a y p o i n t s   - - -

    def genWaypoints ( self ):
        "Generate self's waypoints in order."
        for  pt in self.__pointList:
            yield pt

        raise StopIteration



# - - - - -   c l a s s   W a y p o i n t   - - - - -

class Waypoint:
    "Class to represent one waypoint."


# - - -   W a y p o i n t . _ _ i n i t _ _   - - -

    def __init__ ( self, latLon, desc, gpsElevation=None,
                   mapElevation=None, mapDatum=None ):
        "Constructor for Waypoint."
        self.latLon         =  latLon
        self.desc           =  desc
        self.gpsElevation   =  gpsElevation
        self.mapElevation   =  mapElevation
        self.mapDatum       =  mapDatum


# - - -   W a y p o i n t . _ _ s t r _ _   - - -

    def __str__ ( self ):
        "Return self as a string."
        return "%s %s" % ( self.latLon, self.desc )
