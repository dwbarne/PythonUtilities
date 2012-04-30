"""canscroll.py:  ScrolledCanvas widget for Tkinter
"""

RCS_REVISION    =   "$Revision: 1.7 $"
RCS_DATE        =   "$Date: 2005/07/07 22:58:13 $"

#================================================================
# Exports:
#   class ScrolledCanvas ( master, vwide=None, vhigh=None, **options ):
#     [ ( ( master is a Frame ) and
#         ( vwide is the virtual width, defaulting to DEFAULT_VWIDE) and
#         ( vhigh is the virtual height, defaulting to DEFAULT_VHIGH) and
#         ( options is a dictionary containing options
#           to be used in creating a canvas) ) ->
#         master  :=  master with a new ScrolledCanvas widget added
#                     but not gridded, with those options, that has
#                     scrollbars and a binding allowing dragging with
#                     the middle mouse button
#         return that widget ]
#   .can:               [ self's Canvas ]
#----------------------------------------------------------------


# - - -   I m p o r t s   - - -

from Tkinter import *       # Python-Tk GUI widgets



# - - -   M a n i f e s t   c o n s t a n t s   - - -

DEFAULT_VWIDE  =  600        # Default virtual width
DEFAULT_VHIGH  =  600        # Default virtual height



# - - - - -   c l a s s   S c r o l l e d C a n v a s   - - - - -

class ScrolledCanvas(Frame):
    """Widget for a canvas with integrated scrollbars.

      Gridding plan:

          0                1
        +----------------+----------------+
      0 | self.can       | self.__scrollY |
        +----------------+----------------+
      1 | self.__scrollY |                |
        +----------------+----------------+

      Row 0 and column 0 are expandable (that is, we call
      .rowconfigure() and .columnconfigure() and assign them
      a weight of 1).

      Internal widgets:
        .__scrollX:     [ self's horizontal scrollbar ]
        .__scrollY:     [ self's vertical scrollbar ]

      State/Invariants:
        .__vwide:           [ effective virtual width ]
        .__vhigh:           [ effective virtual height ]
        .__normalCursor:    [ self's cursor when not dragging ]
        .__dragging:
          [ if button 2 is down -> 1
            else -> 0 ]
        .__dragStart:
          [ if button 2 is down ->
              the canvas (not widget) coordinates (x,y) where it went down
            else -> <anything> ]
        .__offsetStart:
          [ if button 2 is down ->
              the canvas offset (x,y) where it went down
            else -> <anything> ]
    """

# - - -   S c r o l l e d C a n v a s . _ _ i n i t _ _   - - -

    def __init__ ( self, master, vwide=None, vhigh=None, **options ):
        "Constructor for ScrolledCanvas"

        #-- 1 --
        # [ master  :=  master with a new Frame added and gridded
        #   self    :=  that Frame ]
        Frame.__init__ ( self, master, relief=RIDGE, borderwidth=5 )
        self.grid(sticky=N+S+E+W)

        #-- 2 --
        # [ self.__vwide, self.__vhigh  :=  as invariants
        #   self.__dragging, self.__normalCursor  :=  as invariants ]
        if  vwide==None:    self.__vwide  =  DEFAULT_VWIDE
        else:               self.__vwide  =  vwide

        if  vhigh==None:    self.__vhigh  =  DEFAULT_VHIGH
        else:               self.__vhigh  =  vhigh
            
        self.__normalCursor  =  self["cursor"]
        self.__dragging  =  0

        #-- 3 --
        # [ self  :=  self with all internal widgets created ]
        self.__createWidgets(options)


# - - -   S c r o l l e d C a n v a s . _ _ c r e a t e W i d g e t s   - - -

    def __createWidgets(self, options):
        "Create all self's internal widgets."

        #-- 1 --
        # [ self  :=  self with grid row 0 and column 0 expandable ]
        self.columnconfigure ( 0, weight=1 )
        self.rowconfigure ( 0, weight=1 )

        #-- 2 --
        # [ self  :=  self with a new Canvas object gridded, its scroll
        #             extent determined from self.__vwide and self.__vhigh ]
        #   self.can  :=  that Canvas
        self.can  =  Canvas ( self,
            takefocus=1,        # Allow focus to visit the canvas
            highlightcolor="coral",     # Color of focus highlight
            highlightthickness=2,       # Size of focus highlight
            scrollregion=(0,0,self.__vwide, self.__vhigh ) )
        self.can.config(**options)      # Add user's options
        self.can.grid ( row=0, column=0, sticky=N+S+E+W )

        #-- 3 --
        # [ self.can  :=  self.can with horizontal and vertical Scrollbar
        #       widgets added and gridded
        #   self.__scrollX  :=  that horizontal Scrollbar
        #   self.__scrollY  :=  that vertical Scrollbar ]
        self.__scrollX  =  Scrollbar ( self,
            highlightcolor="coral",
            highlightthickness=2,
            orient=HORIZONTAL )
        self.__scrollX.grid ( row=1, column=0, sticky=E+W )

        self.__scrollY  =  Scrollbar ( self,
            highlightcolor="coral",
            highlightthickness=2,
            orient=VERTICAL )
        self.__scrollY.grid ( row=0, column=1, sticky=N+S )

        self.can["xscrollcommand"]  =  self.__scrollX.set
        self.__scrollX["command"]   =  self.can.xview

        self.can["yscrollcommand"]  =  self.__scrollY.set
        self.__scrollY["command"]   =  self.can.yview

        #-- 4 --
        # [ self.can  :=  self.can with the input focus, and the four
        #       cursor keys bound to a handler that will scroll the
        #       canvas ]
        self.can.focus_set()
        self.can.bind ( "<Key-Up>",     self.__arrowHandler )
        self.can.bind ( "<Key-Down>",   self.__arrowHandler )
        self.can.bind ( "<Key-Left>",   self.__arrowHandler )
        self.can.bind ( "<Key-Right>",  self.__arrowHandler )

        #-- 5 --
        # [ self.can  :=  self.can with button 2 and motion set up
        #       to allow the user to drag-scroll the canvas ]
        self.can.bind ( "<Button-2>",           self.__b2Down )
        self.can.bind ( "<ButtonRelease-2>",    self.__b2Up )
        self.can.bind ( "<Motion>",             self.__motion )


# - - -   S c r o l l e d C a n v a s . _ _ a r r o w H a n d l e r   - - -

    __arrowMap  =  {    # Maps arrow key name -> (delta x, delta y) in UNITS
        "Up":   (0, -1),        "Left":     (-1, 0),
        "Down": (0, 1),         "Right":    (1, 0) }

    def __arrowHandler ( self, event ):
        "Handles the four cursor arrow keys"
        try:
            dx, dy  =  self.__arrowMap[event.keysym]
            if  dx != 0:    self.can.xview_scroll ( dx, "units" )
            if  dy != 0:    self.can.yview_scroll ( dy, "units" )
        except KeyError:
            sys.stderr.write ( "*** Programming error: unknown key "
                               "in canvas arrow key handler" )


# - - -   S c r o l l e d C a n v a s . _ _ b 2 D o w n   - - -

    def __b2Down ( self, event ):
        """Button 2 has gone down.  Prepare to drag the canvas.

          [ event is an Event object ->
              self.can            :=  self.can with a `hand' cursor
              self.__dragging     :=  1
              self.__dragStart    :=  canvas coordinates of cursor
              self.__offsetStart  :=  current canvas offset vs virtual size ]
        """
        self.__dragging      =  1
        self.__normalCursor  =  self.can["cursor"]
        self.can["cursor"]   =  "hand2"
        self.__dragStart     =  (event.x, event.y)
        self.__offsetStart   =  (self.can.canvasx(0), self.can.canvasy(0))


# - - -   S c r o l l e d C a n v a s . _ _ b 2 U p   - - -

    def __b2Up ( self, event ):
        """Button 2 has gone up.  Stop dragging.

          [ self.__dragging  :=  0
            self.__normalCursor  :=  self's current cursor
            self.can  :=  self.can with cursor self.__normalCursor ]
        """
        self.__dragging      =  0
        self.can["cursor"]   =  self.__normalCursor


# - - -   S c r o l l e d C a n v a s . _ _ m o t i o n   - - -

    def __motion ( self, event ):
        """If button 2 is down, drag the imag along with the mouse.

          [ event is an Event object ->
              if  self.__dragging ->
                self.can  :=  self.can scrolled in both coordinates
                    an amount equal to the mouse position's offset
                    relative to self.__dragStart, but no further than
                    the edges of the virtual size
              else -> I ]
        """

        #-- 1 --
        if  not self.__dragging:
            return

        #-- 2 --
        xoffset  =  ( self.__offsetStart[0] -
                      (event.x - self.__dragStart[0] ) )
        yoffset  =  ( self.__offsetStart[1] -
                      (event.y - self.__dragStart[1] ) )

        #-- 3 --
        # [ xfraction  :=  xoffset expressed as a scroll fraction of
        #       the virtual size self.image[0]
        #   yfraction  :=  yoffset expressed as a scroll fraction of
        #       the virtual size self.image[1] ]
        xfraction  =  self.__scrollFraction ( xoffset, self.__vwide )
        yfraction  =  self.__scrollFraction ( yoffset, self.__vhigh )

        #-- 4 --
        # [ self.can  :=  self.can scrolled to x=xfraction, y=yfraction ]
        self.can.xview_moveto ( xfraction )
        self.can.yview_moveto ( yfraction )


# - - -   S c r o l l e d C a n v a s . _ _ s c r o l l F r a c t i o n   - - -

    def __scrollFraction ( self, offset, vsize ):
        """Compute the `scroll fraction' for a given offset.

          Definitions:
            offset:  The desired distance between the virtual and
                physical windows.
            vsize:   The virtual size.

          The `scroll fraction' is 0.0 when the physical window is scrolled
          to its leftmost extent (offset=0) and 1.0 at its rightmost extent
          (offset = vsize-psize).  The same calculation is used for both
          x and y; here's a diagram for the x dimension:

            <------- vsize -------->    <------- vsize -------->
            +======================+    +======================+
            |+------------+////////|    |////////+------------+|
            ||            |////////|    |////////|            ||
            ||<- psize -> |////////|    |////////|<- psize -> ||
            ||            |////////|    |////////|            ||
            |+------------+////////|    |////////+------------+|
            +======================+    +======================+
              offset=0                    offset=vsize
              fraction=0.0                fraction=1.0

          [ if (offset is an integer)
            and (vsize is an integer) ->
              return the floating fraction corresponding to offset but
              never less than 0.0 or greater than 1.0             
            else -> return 0.0 ]
        """

        #-- 1 --
        fraction  =  float(offset) / vsize

        #-- 2 --
        # [ if fraction < 0.0 ->
        #     return 0.0
        #   else if fraction > 1.0 ->
        #     return 1.0
        #   else ->
        #     return fraction ]
        return max ( 0.0, min ( 1.0, fraction ) )
