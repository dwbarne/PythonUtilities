"""waypointsDTD.py:  Constants relating to waypoints.dtd
    $Revision: 1.4 $  $Date: 2005/02/11 22:35:21 $
"""

#--
# Name of the Document Type Definition for generated output
#--
WAYPOINTS_DTD  =  "waypoints.dtd"

#--
# Element names (..._N) and attribute names (..._A)
#--
ROOT_N          =  "waypoint-set"   # <waypoint-set>
ROUTE_N         =  "route"          #   <route
ID_A            =  "id"             #       id="nf"
NAME_A          =  "name"           #       name="North Fork"> 
PT_N            =  "pt"             #     <pt
LATLON_A        =  "latlon"         #       latlon="340132n 1070752w"
GPS_ELEV_A      =  "gps-elev"       #       gps-elev="6850"
MAP_ELEV_A      =  "map-elev"       #       map-elev="6800"
MAP_DATUM_A     =  "mapdatum"       #       mapdatum="WGS-84">North Fork Rd...
