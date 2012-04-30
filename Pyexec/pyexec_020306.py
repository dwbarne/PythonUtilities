#!/usr/local/bin/python
#--
# pyexec.py: An interactive selection tool that allows mpi runs on
#   various Sandia parallel clusters and supercomputers.  Should work
#   anywhere Python is installed with the Tkinter widget set.
#
#   Written by 
#      1. John W. Shipman (john@nmt.edu), New Mexico Tech
#         Computer Center, Socorro, NM 87801.
#      2. Daniel W. Barnette, Sandia National Labs, Albuquerque, NM
#
#  This program's classes have invariants, and intended functions 
#   are used to define the semantics of the methods.  
#--

EXTERNAL_VERSION = "0.1"

#--
# $Revision: 1.12 $
# $Date: 2004/11/12 01:45:28 $
#--
# Table of contents (indentation shows widget hierarchy):
#   Imports
#   class Color:  Object to represent an arbitrary color
#   class Application:  Main class
#   class ColorNamePicker:  Controls for picking colors by name
#     class ColorPickList:  Pick list for standard color names
#   class ColorAdjuster:  Controls for displaying the color parameters
#                         in a particular color model, and providing
#                         sliders for color adjustment
#     class ColorSliders:  Sliders for color adjustment
#       class VSlider:  Vertical slider control group
#   class Swatch:  Controls for displaying colored text on a colored
#                  background, and fg/bg selection
#   class ColorModel: A way of encoding a color space into
#                     three numbers; an abstract class with
#                     these concrete classes:
#     class HSV_Model:  The hue-saturation-value color model
#     class RGB_Model:  The red-green-blue color model
#     class CMY_Model:  The cyan-magenta-yellow color model
#--
# Major version history (most recent version listed first)
#   0.1   Feb-1-2006  First released version
#--


from Tkinter import *       # Import the Tk graphic user interface
from Dialog import Dialog   # Import the dialog-box code
import tkFont               # Import the font creation module

import sys, string, math    # Import other vital modules


#================================================================

class Color:
    """ Object to represent a color in a generic way.
    """

    def __init__ ( self, rgb ):
        """ [ if (rgb is a sequence of three floats in the range
              [0.0, 1.0] ->
                return a new Color object representing a color
                with red rgb[0], green rgb[1], and blue rgb[2] ]
        """
        self.r  =  rgb[0]
        self.g  =  rgb[1]
        self.b  =  rgb[2]

    def __str__ ( self ):
        """ [ return self as a string in human-readable form ]
        """
        return "(%5.3fr %5.3fg %5.3fb)" % (self.r, self.g, self.b)

    def xName ( self ):
        """ [ return self's color as a valid X color name. ]
        """
        return "#%04X%04X%04X" % ( self._fixColor ( self.r ),
                                   self._fixColor ( self.g ),
                                   self._fixColor ( self.b ) )

    def show ( self, digits=4 ):
        """ [ return self's color showing each of the RGB values as
              4-digit hexadecimals, with spaces between the components
              for legibility ]
        """
        #--
        # The default format is "#%04X %04X %04X", but use
        # the precision given
        #--
        format  =  ( "#%%0%dX %%0%dX %%0%dX" %
                     ( digits, digits, digits ) )
        return format % ( self._fixColor ( self.r, digits ),
                          self._fixColor ( self.g, digits ),
                          self._fixColor ( self.b, digits ) )

    def _fixColor ( self, f, digits=4 ):
        """ [ if (f is a float in [0.0, 1.0])
              and (digits is a positive integer) ->
                return f, scaled to the integer interval [0,N) where
                N is 2**(digits*4) ]
        """
        base  =  float ( 1 << (digits * 4) ) - 1.0
        return int ( base * f )


#================================================================

class Application(Frame):
    """ This object encapsulates the entire "xhue" application.
        Its purpose is to allow the user to explore color space
        and pick colors for his on-screen applications.

        Widget hierarchy:
            ._menuBar:  The menu bar across the top of the window.
            ._colorNamePicker:  A ColorNamePicker widget for
                selecting colors by name.
            ._colorAdjuster:  A ColorAdjuster widget for selecting
                a color model and adjusting colors.
            ._swatch:  A Swatch widget that shows some text in the
                foreground color, and allows the user to select
                whether the ._colorAdjuster is connected to the
                foreground or background color

        Grid plan:
              0                  1                2
            +------------------+----------------+---------+
          0 | _menuBar                                    |
            +------------------+----------------+---------+
          1 | _colorNamePicker | _colorAdjuster | _swatch |
            +------------------+----------------+---------+

        Control linkages between these widgets:

          - Whenever the user picks a valid color name on the
            ColorNamePicker widget, that widget tells the
            ColorAdjuster widget to display that color.

          - Whenever the user adjusts a color on the ColorAdjuster
            widget, or when that widget is told by another widget
            to change its color, it tells the Swatch widget to
            display that color.  It also positions its sliders to
            show that color as a group of three parameters in the
            currently selected color model.

          - Whenever the user changes the Swatch widget between
            foreground and background mode, that widget tells the
            ColorAdjuster widget to display the current fg or bg
            color, whichever is now selected.
    """


# - - -   Class variables   - - -

    BUTTON_FONT  = "-*-lucida-medium-r-*-*-*-120-*-*-*-*-*-*"
    DEFAULT_BG   = Color ( ( 1.0, 0.0, 0.0 ) )   # Red
    DEFAULT_FG   = Color ( ( 0.0, 0.0, 0.0 ) )   # Black


# - - -   _ _ i n i t   _ _

    def __init__ ( self, master=None ):
        """ The __init__ method of a Tkinter application is pretty
            stereotyped:
                1. Call the initialization method of the parent class.
                2. Call self.grid() to put the application in the window.
                3. Create all the application's widgets.
        """
        Frame.__init__ ( self, master )
        self.grid()
        self._createWidgets()
        self._colorAdjuster.set ( self.DEFAULT_BG )


# - - -   c r e a t e W i d g e t s   - - -

    def _createWidgets ( self ):
        """ Our widgets are managed in the four broad groups
            described above---the menu bar, the color name picker panel,
            the color adjustment panel, and the color swatch.
        """

        #-- 1 --
        # [ self  :=  self with a menu bar ]
        self._menuBar  =  self._createMenuBar ( )
        self._menuBar.grid ( row=0, columnspan=3, sticky=W )

        #-- 2 --
        # [ self  :=  self with a new ColorNamePicker set up so that
        #             any valid color name selection tells
        #             self._colorAdjuster to set that color ]
        self._colorNamePicker  =  ColorNamePicker ( self, self._nameHandler )
        self._colorNamePicker.grid ( row=1, column=0,
                                     padx="0.1i", pady="0.1i" )

        #-- 3 --
        # [ self  :=  self with a new Swatch set up so that any change in
        #             fg/bg mode tells self._colorAdjuster to set the new
        #             fg or bg color ]
        self._swatch  =  Swatch ( self, self.DEFAULT_BG, self.DEFAULT_FG,
                                  self._swatchHandler )
        self._swatch.grid ( row=1, column=2, padx="0.1i", pady="0.1i" )

        #-- 4 --
        # [ self  :=  self with a new ColorAdjuster added and
        #             set up so that any color change tells self._swatch
        #             to set that color ]
        self._colorAdjuster    =  ColorAdjuster ( self, self._adjustHandler )
        self._colorAdjuster.grid ( row=1, column=1, padx="0.1i", pady="0.1i" )


# - - -   _ c r e a t e M e n u B a r     - - -

    def _createMenuBar ( self ):
        """ Only two things in the menu bar, a Quit button on the left
            and a Help button on the right.
        """

        #--
        # Place the menu bar at the top of its parent and allow it
        # to fill to the width of the parent.
        #--
        mb  =  Frame ( self, relief=RAISED, borderwidth=2 )

        mb.help  =  self._createHelpMenuButton ( mb )
        mb.help.grid ( row=0, column=0, sticky=W )

        mb.quit  =  Button ( mb, text="Quit", command=self.quitButton )
        mb.quit.grid ( row=0, column=1, sticky=E )

        return mb


# - - -   q u i t B u t t o n   - - -

    def quitButton ( self ):
        """ Handler for the Quit button.
        """
	print ""
	print "   -- End of Performance Analysis Session -- "
	print " "
        raise SystemExit


# - - -   _ c r e a t e H e l p M e n u B u t t o n   - - -

    def _createHelpMenuButton ( self, master ):
        mb  =  Menubutton ( master, text="Help", underline=0 )

        #--
        # mb.m is the menu activated by mb
        #--
        mb.m  =  Menu ( mb )
        mb["menu"]  =  mb.m

        #--
        # mb.m.select is the `select by colorname' cascade
        #--
        mb.m.select = Menu ( mb.m )
        mb.m.select.add_command ( command=self._helpTyping,
            label="Typing in a standard color name" )
        mb.m.select.add_command ( command=self._helpPicking,
            label="Picking a standard color name" )

        #--
        # mb.m.create is the `create new color' cascade
        #--
        mb.m.create = Menu ( mb.m )
        mb.m.create.add_command ( command=self._helpSliders,
            label="Using the color sliders" )
        mb.m.create.add_command ( command=self._helpColorModels,
            label="Color models and color space" )
        mb.m.create.add_command ( command=self._helpHSV,
            label="The HSV color model" )
        mb.m.create.add_command ( command=self._helpRGB,
            label="The RGB color model" )
        mb.m.create.add_command ( command=self._helpCMY,
            label="The CMY color model" )

        #--
        # mb.m.view is the `viewing colors' cascade
        #--
        mb.m.view = Menu ( mb.m )
        mb.m.view.add_command ( command=self._helpSwatch,
            label="The color swatch" )
        mb.m.view.add_command ( command=self._helpReadouts,
            label="The RGB readouts" )
        mb.m.view.add_command ( command=self._helpTextColor,
            label="Changing the text color" )

        #--
        # Now add the cascades and first-level items to the
        # menu pulldown
        #--
        mb.m.add_cascade ( menu=mb.m.select,
            label="Selecting a standard color" )
        mb.m.add_cascade ( menu=mb.m.create,
            label="Creating new colors" )
        mb.m.add_cascade ( menu=mb.m.view,
            label="Viewing colors" )
        mb.m.add_command ( command=self._helpColorImporting,
            label="Importing colors into other applications" )
        mb.m.add_command ( command=self._helpAuthor,
            label="Who made this tool?" )
        return mb

# - - -   _ h e l p T y p i n g   - - -

    def _helpTyping(self):
        Dialog ( self, title="Help: Typing in a standard color name",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="If you already know the name of the "
                      "color you want, move the cursor into "
                      "the field labeled \"Enter a color name:\", "
                      "type the color name, and press Enter."
                      "\n\tYour color should then be displayed."
                      "\n\tIf the color name you type is not"
                      "known to the system, you will get a "
                      "popup dialog menu." )


# - - -   _ h e l p P i c k i n g   - - -

    def _helpPicking(self):
        Dialog ( self, title="Help: Picking a standard color name",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="Under the label \"Or double-click on a name:\""
                      "you will see a list of all the standard X "
                      "color names.  To see a color, move the cursor "
                      "onto its name and double-click the left button."
                      "\n\tYou can use the scrollbar to the "
                      "right of the list to scroll through the list." )


# - - -   _ h e l p S l i d e r s   - - -

    def _helpSliders(self):
        Dialog ( self, title="Help: Using the color sliders",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="To adjust a color, drag any of the three "
                      "sliders with the mouse.  Each one controls "
                      "one component of the color; see ``Help -> "
                      "Creating new colors -> Color models and "
                      "color space'' for an explanation of these "
                      "components."
                      "\n\tYou can also click on the ``+'' or ``-' "
                      "buttons to make very fine adjustments." )


# - - -   _ h e l p C o l o r M o d e l s   - - -

    def _helpColorModels(self):
        Dialog ( self, title="Help: Color models and color space",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="You can select any of three different ways "
                      "of viewing color space: the HSV model (hue, "
                      "saturation, and value); the RGB model (red, "
                      "green, and blue); or the CMY model (cyan, "
                      "magenta, and yellow).  To change the current "
                      "color model, click on one of the radiobuttons "
                      "below the label \"Select a color model:\""
                      "\n\tFor more information on color theory, "
                      "see Foley and van Dam, ``Computer graphics: "
                      "principles and practice,'' the section on color "
                      "models." )


# - - -   _ h e l p H S V   - - -

    def _helpHSV(self):
        Dialog ( self, title="Help: The HSV color model",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="In the HSV color model, color is specified "
                      "by these three parameters:"
                      "\n\t* Hue controls the base color.  As you "
                      "drag the Hue slider, the color goes through "
                      "red, yellow, green, cyan, blue, magenta, and "
                      "then back to red again."
                      "\n\t* Saturation controls color intensity.  "
                      "Drag the Saturation slider down for pale "
                      "colors, drag it up for intense colors."
                      "\n\t* Value controls brightness.  "
                      "Drag the Value slider down to darken a color, "
                      "up to lighten it." )


# - - -   _ h e l p R G B   - - -

    def _helpRGB(self):
        Dialog ( self, title="Help: The RGB color model", 
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="In the RGB color model, color is specified "
                      "by these three parameters: red, green, and "
                      "blue.  These are called the ``additive "
                      "primary colors;'' if you drag all three "
                      "sliders all the way up, you get white.  "
                      "RGB color mixing is used in printing and "
                      "also in stage lighting." )


# - - -   _ h e l p C M Y   - - -

    def _helpCMY(self):
        Dialog ( self, title="Help: The CMY color model",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="In the CMY color model, color is specified "
                      "by these three parameters: cyan, magenta, "
                      "and yellow.  These are called the ``subtractive "
                      "primary colors;'' if you drag all three "
                      "sliders all the way up, you get black."
                      "CMY color mixing is used in color darkroom work." )


# - - -   _ h e l p S w a t c h   - - -

    def _helpSwatch(self):
        Dialog ( self, title="Help: The color swatch",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="The lower right part of the window displays "
                      "the current background color, with some text "
                      "shown in the current foreground color "
                      "(initially black).  The two radiobuttons on "
                      "the top right allow you to select whether you "
                      "are adjusting the background color or the "
                      "foreground color." )


# - - -   _ h e l p R e a d o u t s   - - -

    def _helpReadouts(self):
        Dialog ( self, title="Help: the RGB readouts",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="You can see the exact background and "
                      "foreground colors at any time by looking "
                      "at the two readouts that start with a ``#'' "
                      "character.  The top one shows the background "
                      "color, and the bottom one the foreground "
                      "(text) color."
                      "\n\tEach readout shows the red, green, and "
                      "blue values of that color as a string of "
                      "four hexadecimal digits."
                      "\n\tSee ``Help -> Importing colors'' for "
                      "more information on using these readouts." )


# - - -   _ h e l p T e x t C o l o r   - - -

    def _helpTextColor ( self ):
        Dialog ( self, title="Help: Changing the text color",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="Initially, the text is shown in black against "
                      "the background color that you select.  To see "
                      "what different text colors look like against "
                      "your background color, click on the "
                      "radiobutton labeled ``Foreground (text) "
                      "color.''"
                      "\n\tNow you can select or adjust the text "
                      "color."
                      "\n\tTo go back to selecting the background "
                      "color, click on the radiobutton labeled "
                      "``Background color.''" )


# - - -   _ h e l p C o l o r I m p o r t i n g   - - -

    def _helpColorImporting(self):
        Dialog ( self,
                 title="Help: Importing colors into other applications",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="To use one of the standard color names "
                      "in an application, you can just use the name "
                      "as it appears in the list of standard colors."
                      "\n\tYou can also use the hexadecimal form "
                      "of the color name that appears in the RGB "
                      "readouts on the top right; just omit the "
                      "spaces."
                      "\n\tFor example, if the background "
                      "color readout shows #FFFF 7FFF 0000, the "
                      "equivalent color name is \"#FFFF7FFF0000\"." )


# - - -   _ h e l p A u t h o r   - - -

    def _helpAuthor(self):
        Dialog ( self, title="Help: Who made this tool?",
                 default=0, strings=( "Dismiss", ), bitmap="info",
                 text="xhue was written by John W. Shipman "
                      "(john@nmt.edu) of the New Mexico Tech "
                      "Computer Center, Socorro, NM 87801."
                      "\n\tThis is version " +
                      EXTERNAL_VERSION + "." )
        

# - - -   _ n a m e H a n d l e r   - - -

    def _nameHandler ( self, color ):
        self._colorAdjuster.set ( color )


# - - -   _ a d j u s t H a n d l e r   - - -

    def _adjustHandler ( self, color ):
        self._swatch.set ( color )


# - - -   _ s w a t c h H a n d l e r   - - -

    def _swatchHandler ( self, color ):
        self._colorAdjuster.set ( color )


#================================================================

class ColorNamePicker ( Frame ):
    """ A widget for picking colors by name.  Contains:
          - A text entry field for typing an arbitrary color name.
          - A scrollable listbox containing all the standard X
            color names (except those with embedded blanks).
        Exports:
            ColorNamePicker ( master, callback )
                [ if (master is a widget) and (callback is a function) ->
                    master  :=  master with our widgets inside it
                                in a frame, so that on any event
                                that selects a valid color, we call
                                  callback ( c )
                                where c is a Color object representing the
                                color picked ]

        Widget hierarchy [and grid coordinates]:
            ._entryLabel:  Label for color name entry field [0,0]
            ._entry:  Color name entry field [1,0]
            ._pickLabel:  Label for the color pick list [2,0]
            ._pickList:  A ColorPickList object [3,0]
        State and invariants:
            ._callback:  The callback function to be called when
                the user picks a valid color
            ._entryVar:  a StringVar linked to the color name
                entry field
    """

    #--
    # Manifest constants
    #--
    NAME_WIDTH = 20     # Width of a name in characters


# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self, master, callback ):
        #-- 1 --
        # [ master  :=  master with a new, empty Frame
        #   self    :=  that frame ]
        Frame.__init__ ( self, master )

        #-- 2 --
        self._callback  =  callback
        self._entryVar  =  StringVar()

        #-- 3 --
        # [ self  :=  self with all widgets created and gridded ]
        self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

    def _createWidgets ( self ):
        """ [ self  :=  self with all widgets created and gridded
        """

        #-- 1 --
        # [ self              :=  self with a new Label to label the
        #                         color name field
        #   self._entryLabel  :=  that widget ]
        self._entryLabel  =  Label ( self, text="Enter a computer's hostname:" )
        self._entryLabel.grid ( row=0, sticky=W )

        #-- 2 --
        # [ self         :=  self with a new Entry, with Enter bound to
        #                    a routine that will call self._callback
        #                    when a valid color is entered
        #   self._entry  :=  that widget ]
        self._entry   =  Entry ( self, relief=SUNKEN,
                                 width=self.NAME_WIDTH,
                                 textvariable=self._entryVar )
        self._entry.grid ( row=1, sticky=W )
        self._entry.bind ( "<Key-Return>", self._entryHandler )

        #-- 3 --
        # [ self             :=  self with a new Label to label the color
        #                        pick list
        #   self._pickLabel  :=  that widget ]
        self._pickLabel  =  Label ( self,
                                    text="Or double-click on a name:" )
        self._pickLabel.grid ( row=2, sticky=W )

        #-- 4 --
        # [ self            :=  self with a new ColorPickList widget,
        #                       with its callback set up to call self._callback
        #                       when a color is picked
        #   self._pickList  :=  that widget ]
        self._pickList  =  ColorPickList ( self,
                                           callback=self._pickListHandler )
        self._pickList.grid ( row=3, sticky=W )


# - - -   _ e n t r y H a n d l e r   - - -

    def _entryHandler ( self, event ):
        """ [ if event is an event in self._entry ->
                if self._entryVar is a valid color name ->
                    call self._callback ( a Color representing that name )
                else ->
                    pop up a dialog box to tell the user self._entryVar
                    is not valid ]
        """
        self._setByName ( self._entryVar.get() )


# - - -   _ s e t B y N a m e   - - -

    def _setByName ( self, colorName ):
        """ [ if colorName is a string ->
                if colorName is a valid X color name in self's window ->
                  call self._callback ( a Color representing that name )
                  return 1
                else ->
                  pop up a dialog box to tell the user (colorName)
                    is not valid
                  return 0 ]
        """

        #-- 1 --
        # [ if colorName is a valid X color name in self's window ->
        #     rgb  :=  a tuple ( r, g, b ) representing that color,
        #              where each value is an integer in [0,65535]
        #   else ->
        #     pop up a dialog box to tell the user (colorName)
        #       is not valid
        #     return 0 ]
        try:
            rgb = Misc.winfo_rgb ( self, colorName )
        except:
            d = Dialog ( self, title="Message", bitmap="info",
                         text="Computer `" + colorName + "' is not defined.",
                         default=0,           # First button is the default
                         strings=("OK",) )    # Only one button: OK
            return 0

        #-- 2 --
        # [ if rgb is a tuple ( r, g, b ) representing a color in the RGB
        #   model, where each value is an integer in [0,65535] ->
        #     call self._callback ( c ) where c is a Color object
        #       representing rgb ]
        self._callback ( Color ( ( self._scale16 ( rgb[0] ),
                                   self._scale16 ( rgb[1] ),
                                   self._scale16 ( rgb[2] ) ) ) )


# - - -   _ s c a l e 1 6   - - -

    def _scale16 ( self, color16 ):
        """ Takes an integer color value in the range [0,65535]
            and normalizes it to a float in [0.0, 1.0].
        """
        return float ( color16 ) / 65535.0


# - - -   _ p i c k L i s t H a n d l e r   - - -

    def _pickListHandler ( self, color ):
        """ [ if color is a Color object ->
                call self._callback ( a Color representing colorName ) ]
        """
        self._callback ( color )


#================================================================

class ColorPickList ( Frame ):
    """ A widget for selecting standard X window colors.
        A frame containing a Listbox with color names and an
        associated vertical Scrollbar.

        Exports:
            ColorPickList ( master, callback )
                [ if (master is a widget) and (callback is a function) ->
                    master  :=  master with our widgets in a frame, so that
                                on any event that selects a valid color,
                                we call
                                  callback ( c )
                                where c is a Color object representing
                                that color ]

        Widget hierarchy [and grid coordinates]:
            ._names:  The Listbox containing the color names [0,0]
            ._scroll:  The Scrollbar for scrolling the listbox [0,1]
        State and invariants:
            ._callback:  The callback function
            ._colors:  A list of Color objects such that ._colors[i]
                       represents the color from the (i)th name in ._names
    """

    #--
    # Manifest constants
    #--
    COLOR_NAMES_FILE = "/usr/lib/X11/rgb.txt"       # Color names file
    NAME_WIDTH = 20     # Width of the Listbox in characters
    # NAME_LINES = 22     # Number of lines in the Listbox
    NAME_LINES = 10     # Number of lines in the Listbox


# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self, master, callback ):
        #-- 1 --
        # [ master  :=  master with a new Frame
        #   self    :=  that Frame ]
        Frame.__init__ ( self, master )

        #-- 2 --
        self._callback  =  callback

        #-- 3 --
        # [ self  :=  self with all widgets created and gridded ]
        self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

    def _createWidgets ( self ):
        """ [ self  :=  self with all widgets created and gridded ]
        """

        #-- 1 --
        # [ self          :=  self with a new Scrollbar
        #   self._scroll  :=  that Scrollbar ]
        self._scroll  =  Scrollbar ( self, orient=VERTICAL )
        self._scroll.grid ( row=0, column=1, sticky=N+E+S )

        #-- 2 --
        # [ self         :=  self with a new Listbox, scrolled by
        #                    self._scroll, with single-click events on the
        #                    (i)th name bound to a method that calls
        #                    self._callback(c) where c is self._colors(i) 
        #   self._names  :=  that Listbox ]
        self._names  =  Listbox ( self, width=self.NAME_WIDTH,
            height=self.NAME_LINES, relief=SUNKEN,
            borderwidth=2, exportselection=0,
            yscrollcommand=self._scroll.set )
        self._names.grid ( row=0, column=0, sticky=N+W+S )
        self._names.bind ( "<Double-Button-1>", self._pickHandler )
        self._scroll["command"] = self._names.yview

        #-- 3 --
        # [ self._names   :=  self._names with all color names from 
        #                     self.COLOR_NAMES_FILE inserted in the order
        #                     they occur in the file, except for names with
        #                     embedded blanks
        #   self._colors  :=  a list of Color objects representing those
        #                     names in the same order ]
        self._readColorNames ( )


# - - -   _ p i c k H a n d l e r   - - -

    def _pickHandler ( self, event ):
        """ [ if event is an event in self._names ->
                call self._callback(c) where c is the self._colors(i)
                  and i is the index of the selected name ]
        """
        current = self._names.curselection()    # An Index tuple
        if  len(current) > 0:                   # Ignore when empty
            i   =  string.atoi ( current[0] )
            self._callback ( self._colors[i] )


# - - -   _ r e a d C o l o r N a m e s   - - -

    def _readColorNames ( self ):
        """ [ if self.COLOR_NAMES_FILE names a readable file in which
              "!" is the comment character and lines have the format
              "r g b name" where r, g, and b are red, green and blue
              values in [0,255] and the name may have embedded blanks ->
                self._names   :=  self._names with all color names from 
                                  self.COLOR_NAMES_FILE inserted in the order
                                  they occur in the file, except for names with
                                  embedded blanks
                self._colors  :=  a list of Color objects representing those
                                  names in the same order ]
        """

        #-- 1 --
        self._colors  =  []

        #-- 2 --
        # [ if self.COLOR_NAMES_FILE can be opened for reading ->
        #     colorFile  :=  that file so opened
        #   else ->
        #     stdout  ||:=  message about unavailable color file
        #     return ]
        try:
            colorFile = open ( self.COLOR_NAMES_FILE )
        except:
            print ( "*** Can't open the standard color names file `" +
                    self.COLOR_NAMES_FILE + "'." )
            return

        #-- 3 --
        # [ colorList  :=  a list of the lines from colorFile ]
        colorList  =  colorFile.readlines()
        colorFile.close()

        #-- 4 --
        # [ self._colors  ||:=  a Color object representing each line from
        #                       colorList that doesn't start with "!",
        #                       where the format of the line is "r g b name",
        #                       ignoring names with embedded blanks, and
        #                       the (r,g,b) values are in [0,255] ]
        for line in colorList:
            #-- 4 body --
            # [ if line starts with "!" or doesn't have 4 fields -> I
            #   else ->
            #     self._colors  ||:=  a Color whose (r,g,b) values are
            #                         taken from the first three fields
            #                         of line, integers in [0,255]
            #     self._names   ||:=  the fourth field from line ]
            if line[0] != "!":  # Ignore comment lines

                #-- 4.1 --
                # [ fields  :=  a list of the whitespace-delimited fields
                #               from line ]
                fields = string.split ( line )      

                #-- 4.2 --
                # [ if fields has 4 elements ->
                #     self._colors  ||:=  a Color whose (r,g,b) values are
                #                         taken from fields[0:2], integers
                #                         in [0,255]
                #     self._names   ||:=  fields[3]
                #   else -> I ]
                if len(fields) == 4:
                    self._colors.append ( self._rgbScale ( fields ) )
                    self._names.insert ( END, fields[3] )


# - - -   _ r g b S c a l e   - - -

    def _rgbScale ( self, fields ):
        """ [ if fields is a sequence of at least three strings
              representing integers in [0,255] ->
                return a Color object using fields[0:2] as the RGB
                  values
        """
        return Color ( ( string.atof ( fields[0] ) / 255.0,
                         string.atof ( fields[1] ) / 255.0,
                         string.atof ( fields[2] ) / 255.0 ) )


#================================================================

class ColorAdjuster ( Frame ):
    """ A widget that allows the user to select a color model,
        and displays and allows the user to adjust a color.

        Exports:
            ColorAdjuster ( master, callback )
                [ if (master is a widget) and (callback is a function) ->
                    master  :=  master with a new ColorAdjuster widget,
                                set up so that any color change due to
                                explicit .set() or user events calls
                                  callback(c)
                                where c is a Color widget representing the
                                new color ]
            .set ( color ):
                [ if (color is a Color object) ->
                    display (color) in self's sliders
                    call self's callback with (color) ]
            .get ( ):
                [ returns a Color object representing self's current color ]

        Widget hierarchy [and grid coordinates]:
            ._radioLabel:  Label for radiobuttons [0,0]
            ._radioFrame:  Frame for radiobuttons [1,0]
                ._radios:  A list of radiobuttons, one per color model
            ._slidersLabel:  Label for the ColorSliders widget [2,0]
            ._sliders:  A ColorSliders widget [3,0]

        State and invariants:
            ._callback:  Our callback function
            ._models:  A list of ColorModel objects such that
                       self._radios[i] selects self._models[i]
            ._modelx:  An IntVar linked to self._radios
            ._radios: A list of radiobuttons, one per color model
    """

    def __init__ ( self, master, callback ):
        #-- 1 --
        # [ master  :=  master with a new Frame inserted
        #   self    :=  that Frame ]
        Frame.__init__ ( self, master )

        #-- 2 --
        # [ self._callback  :=  callback
        #   self._models    :=  a list of one or more ColorModel objects
        #   self._modelx    :=  an IntVar set to 0 ]
        self._callback  =  callback
        self._models    =  []
        self._models.append ( HSV_Model ( ) )
        self._models.append ( RGB_Model ( ) )
        self._models.append ( CMY_Model ( ) )
        self._modelx   =  IntVar ( )
        self._modelx.set ( 0 )

        #-- 3 --
        # [ self  :=  self with all widgets created and gridded ]
        self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

    def _createWidgets ( self ):
        """ [ self  :=  self with all widgets created and gridded ]
        """

        #-- 1 --
        # [ self          :=  self with one or more new Radiobutton widgets,
        #                     one per element of self._models, such that the
        #                     Nth radiobutton sets self._modelx to N and has
        #                     a label derived from self._models[N], and each
        #                     radiobutton tells self._sliders when the
        #                     color model changes
        #   self._radios  :=  a list of those Radiobuttons in the same order ]
        self._radioLabel  =  Label ( self, text="Select a color model:" )
        self._radioLabel.grid ( row=0, sticky=W )

        self._radioFrame  =  Frame ( self, relief=RIDGE, borderwidth=4 )
        self._radioFrame.grid ( row=1, sticky=W, padx="0.1i", pady="0.1i" )

        self._radios = []
        for i in xrange(len(self._models)):
            self._radios.append ( self._addRadioButton ( i ) )

        #-- 2 --
        # [ self                :=  self with a new Label to label the
        #                           ColorSliders widget 
        #   self._slidersLabel  :=  that new Label ]
        self._slidersLabel = Label ( self,
          text="Drag these sliders to change\nthe displayed color:" )
        self._slidersLabel.grid ( row=2, sticky=W )

        #-- 3 --
        # [ self           :=  self with a new ColorSliders widget,
        #                      with its callback set to self._callback(),
        #                      and its color model the (self._modelx)th
        #                      element of self._models
        #   self._sliders  :=  that new widget ]
        self._sliders  =  ColorSliders ( self,
                                         self._models[self._modelx.get()],
                                         self._sliderChanged )
        self._sliders.grid ( row=3, sticky=E+W )


# - - -   _ s l i d e r C h a n g e d   - - -

    def _sliderChanged ( self, color ):
        self._callback ( color )


# - - -   _ a d d R a d i o B u t t o n   - - -

    def _addRadioButton ( self, n ):        
        """ [ if n is in range(len(self._models)) ->
                self  :=  self with a new Radiobutton widget
                          that sets self._modelx to (n) and has a label
                          derived from self._models[n], and set up to
                          tell self._sliders when the model changes
                return that new widget ]
        """

        #-- 1 --
        model  =  self._models[n]

        #-- 2 --
        # [ text  :=  model.name + " (" + s1 + "-" + s2 + "-" + s3 + ")"
        #             where si is the (i)th slider name of model ]
        text   =  model.name() + " ("
        for i in xrange(3):
            if  i != 0:
                text = text + "-"
            text = text + model.sliderLabel(i)
        text  =  text + ")"

        #-- 3 --
        # [ self  :=  self with a new Radiobutton with variable=self._modelx,
        #             value=i, and text=text
        #   rb    :=  that new Radiobutton ]
        rb  =  Radiobutton ( self._radioFrame, variable=self._modelx, value=n,
                 text=text, command=self._modelChanged, anchor=W )
        rb.grid ( row=n, sticky=W )
        return rb


# - - -   _ m o d e l C h a n g e d - - -

    def _modelChanged ( self ):
        newModel  =  self._models [ self._modelx.get() ]
        self._sliders.setColorModel ( newModel )


# - - -   s e t   - - -

    def set ( self, color ):
        self._sliders.set ( color )
        self._callback ( color )


# - - -   g e t   - - -

    def get ( self ):
        return self._sliders.get()


#================================================================

class ColorSliders ( Frame ):
    """ A set of three sliders (scale widgets) for displaying,
        and allowing the user to modify, a color---given a
        ColorModel object that describes how colors are
        specified as a set of three numbers.

        Exports:
            ColorSliders ( master, colorModel, callback ):
                [ if (master is a widget)
                  and (colorModel is a ColorModel object)
                  and (callback is a function) ->
                    master  :=  master with a new ColorSliders widget
                                inserted, using colorModel as
                                its color model, and set up to call
                                callback(c) whenever user events cause
                                selection of a new color and c is a
                                Color object representing that new color ]
            .set ( color ):
                [ if color is a Color object ->
                    set self's sliders to the representation of (color)
                      using self's current color model
                    call callback(color) ]
            .get ( ):
                [ return self's current color as a Color object ]
            .setColorModel ( cm ):
                [ if cm is a ColorModel object ->
                    self  :=  self with its current color model set to
                              cm and its sliders representing its current
                              color in the new model ]

        Widget hierarchy:
            ._sliders:  An array of three VSlider widgets for the
                        three parameters of the color model

        State and invariants:
            ._callback:  Self's callback function
            ._color:  Self's current color
            ._colorModel:  Self's current color model as a ColorModel object
            ._externalSet:  Normally 0, but 1 during execution of .set()
    """

    #--
    # Manifest constants
    #--
    SCALE_MAX_VALUE = 1000


# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self, master, colorModel, callback ):
        #-- 1 --
        # [ master  :=  master with a new Frame
        #   self    :=  that new Frame ]
        Frame.__init__ ( self, master )

        #-- 2 --
        self._callback     =  callback
        self._colorModel   =  colorModel
        self._color        =  Color ( ( 1.0, 1.0, 1.0 ) )  # White initially
        self._externalSet  =  0

        #-- 3 --
        # [ self  :=  self with all widgets created and gridded ]
        self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

    def _createWidgets ( self ):
        """ [ self  :=  self with all widgets created and gridded ]
        """

        #-- 1 --
        # [ self  :=  self with three VSlider widgets, each one labeled
        #             from the corresponding parameter of colorModel,
        #             maxValue=self.SCALE_MAX_VALUE, and callback set to
        #             call self._callback with the the sliders translated
        #             to a new color according to self._colorModel
        #   self._sliders  :=  those three widgets in the same order ]
        self._sliders      =  []

        for i in xrange(3):
            slider = VSlider ( self,
                       labelText=self._colorModel.sliderLabel(i),
                       callback =self._sliderChanged )
            slider.grid ( row=0, column=i, sticky=E+W )
            self._sliders.append ( slider )


        #-- 2 --
        # [ self  :=  self with sliders displaying self._color ]
        self.set ( self._color )


# - - -   _ s l i d e r C h a n g e d   - - -

    def _sliderChanged ( self, value ):
        """ [ self._color  :=  a Color object representing the current
                               values of self._sliders interpreted
                               according to self._colorModel ]
        """

        #-- 1 --
        # [ sliderList  :=  a list of the current positions of the
        #                   sliders in self._sliders, each in [0.0,1.0] ]
        sliderList  =  []

        for i in xrange(3):
            sliderList.append ( self._sliders[i].get() )

        #-- 2 --
        # [ self._color  :=  the Color representing the three
        #                    parameters in sliderList interpreted by
        #                    self._colorModel ]
        self._color  =  self._colorModel.slidersToColor ( sliderList )

        #-- 3 --
        if  not self._externalSet:
            self._callback ( self._color )


# - - -   s e t   - - -

    def set ( self, color ):
        #-- 1 --
        self._externalSet  =  1

        #-- 2 --
        # [ sliderTuple  :=  a triple of normalized slider values from
        #                    self._color interpreted by self._colorModel ]
        sliderTuple  =  self._colorModel.colorToSliders ( color )

        #-- 3 --
        # [ self._sliders  :=  self._sliders with the corresponding
        #                      positions set from sliderTuple ]
        for i in xrange(3):
            self._sliders[i].set ( sliderTuple[i] )

        #-- 4 --
        self._callback ( color )
        self._externalSet = 0


# - - -   g e t   - - -

    def get ( self ):
        return self._color


# - - -   s e t C o l o r M o d e l   - - -

    def setColorModel ( self, colorModel ):
        #-- 1 --
        self._colorModel  =  colorModel

        #-- 2 --
        # [ self._sliders  :=  self._sliders with their labels changed
        #                      to conform to the slider labels from
        #                      self._colorModel ]
        for i in xrange(3):
            self._sliders[i].setLabel ( colorModel.sliderLabel(i) )

        #-- 3 --
        # [ self._sliders  :=  self._sliders with their positions
        #                      changed to reflect self._color interpreted
        #                      self._colorModel ]
        self.set ( self._color )


#================================================================

class VSlider ( Frame ):
    """ A vertical slider widget for adjusting a value in the range
        [0.0, 1.0].  Contains four widgets:
          - A text label
          - A "+" button for incrementing the slider value
          - The actual slider (a Scale widget)
          - A "-" button for decrementing the slider value

        Exports:
            VSlider ( master, labelText, callback )
                [ if (master is a widget) and (labelText is a string)
                  and (callback is a function) ->
                    master  :=  master with a new VSlider labeled with
                                (labelText), and set up so that any
                                change to the value calls callback(v)
                                where v is the new value in [0.0, 1.0] ]
            .set ( value ):
                [ if value is in [0.0, 1.0] ->
                    self  :=  self with the scale adjusted to (value) ]
            .get ( ):
                [ return self's value in [0.0, 1.0] ]
            .setLabel ( text ):
                [ self  :=  self with its label changed to (text) ]

        Widget hierarchy:
            ._label:  The Label widget
            ._scale:  The Scale widget
            ._minus:  The "-" button
            ._plus:  The "+" button

        State and invariants:
            ._callback:  The callback function
            ._labelText:  Text for our label
    """

    #--
    # Manifest constants:
    #--
    MAX_VALUE = 1000        # Scale maximum value
    SCALE_LENGTH = "3i"     # Scale length


# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self, master, labelText, callback ):
        #-- 1 --
        # [ master  :=  master with a new Frame widget inserted
        #   self    :=  that new Frame widget ]
        Frame.__init__ ( self, master )

        #-- 2 --
        self._callback   =  callback
        self._labelText  =  labelText

        #-- 3 --
        # [ self  :=  self with all widgets created and gridded ]
        self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

    def _createWidgets ( self ):
        """ [ self  :=  self with all widgets created and gridded ]
        """

        #-- 1 --
        # [ self         :=  self with a new Label widget whose text is
        #                    (labelText)
        #   self._label  :=  that new Label widget ]
        self._label  =  Label ( self, text=self._labelText )
        self._label.grid ( row=0, sticky=E+W )

        #-- 2 --
        # [ self        :=  self with a new Button widget with its command
        #                   set up to increment the scale widget, and
        #                   labeled "+"
        #   self._plus  :=  that new Button ]
        self._plus  =  Button ( self, text="+",
                                command=self._plusHandler )
        self._plus.grid ( row=1 )

        #-- 3 --
        # [ self         :=  self with a new vertical Scale widget set up to
        #                    call self._callback whenever the scale changes
        #   self._scale  :=  that new Scale widget ]
        #--
        # Note: You can't give a `from=' option since `from' is a
        # reserved word.  However, Fredrik Lundh (fredrik_lundh@ivab.se)
        # answered my post to comp.lang.python to say that `to_=' and
        # `from_=' will work.
        #--
        self._scale  =  Scale ( self, orient=VERTICAL,
                          to=0, from_=self.MAX_VALUE,
                          length=self.SCALE_LENGTH,
                          command=self._scaleHandler )
        self._scale.grid ( row=2, sticky=N+S )

        #-- 4 --
        # [ self        :=  self with a new Button widget with its command
        #                   set up to decrement the scale widget, and
        #                   labeled "-", with its .scale set to self._scale
        #   self._minus  :=  that new Button ]
        self._minus  =  Button ( self, text="-",
                                command=self._minusHandler )
        self._minus.grid ( row=3 )


# - - -   _ p l u s H a n d l e r   - - -

    def _plusHandler ( self ):
        oldValue  =  self._scale.get()
        if  oldValue < self.MAX_VALUE:
            self._scale.set ( oldValue + 1 )


# - - -   _ m i n u s H a n d l e r   - - -

    def _minusHandler ( self ):
        oldValue  =  self._scale.get()
        if  oldValue > 0:
            self._scale.set ( oldValue - 1 )


# - - -   _ s c a l e H a n d l e r   - - -

    def _scaleHandler ( self, value ):
        self._callback ( self.get() )


# - - -   s e t   - - -

    def set ( self, value ):
        self._scale.set ( value * self.MAX_VALUE )


# - - -   g e t   - - -

    def get ( self ):
        return float ( self._scale.get() ) / self.MAX_VALUE


# - - -   s e t L a b e l   - - -

    def setLabel ( self, labelText ):
        self._label["text"]  =  labelText


#================================================================

class Swatch ( Frame ):
    """ A widget for display colored foreground text on a colored
        background.  It also contains two radiobuttons for changing
        whether the caller's color inputs affect the foreground or
        background color.

        Exports:
            Swatch ( master, bgColor, fgColor, callback ):
                [ if (master is a widget)
                  and (bgColor and fgColor are Color objects)
                  and (callback is a function) ->
                    master  :=  master with a new Swatch gridded
                                and set up so that callback(c) is called
                                whenever the user changes the foreground/
                                background mode, with c a Color object
                                representing the color now in the foreground
                                or background, whichever the user selected ]
            .set ( color ):
                [ if (color is a Color object) ->
                    self  :=  self with either the foreground or background
                              color set to (color), depending on the
                              fg/bg radiobuttons ]
            .get ( color ):
                [ return a Color object representing the foreground or
                  background color, depending on the fg/bg radiobuttons ]

        Widget hierarchy [and grid locations]:
            ._topLabel:  The label on the top of the widget [0,0]
            ._radioFrame:  A Frame containing the fg/bg radiobuttons [1,0]
              ._bgRadio:  The radiobutton for selecting background color [0,0]
              ._bgShowLabel:  Readout for the current bg RGB value [1,0]
              ._fgSpacer:  An empty spacer Frame [2,0]
              ._fgRadio:  The radiobutton for selecting foreground color [3,0]
              ._fgShowLabel:  Readout for the current fg RGB value [4,0]
              ._columnLabel:  A label that shows how to interpret the RGB
                              readouts [5,0]
            ._spacerFrame:  Empty spacer frame [2,0]
            ._swatchLabel:  Label above the color swatch [3,0]
            ._swatch:  Text widget displaying bg and fg colors [4,0]

        State and invariants:
            ._bgColor:  Current background color as a Color object
            ._bgShow:   StringVar displaying self._bgColor, as #rrrr gggg bbbb
            ._callback:  Our callback function
            ._fgColor:  Current foreground color as a Color object
            ._fgShow:   StringVar displaying self._bgColor, as #rrrr gggg bbbb
            ._isBackground:  A BooleanVar, true if we are currently
                             setting background, false if foreground
    """

    #--
    # Manifest constants
    #--
    MONO_FONT    =  "-*-lucidatypewriter-bold-r-*-*-*-140-*-*-*-*-*-*"
    SWATCH_TEXT  =  \
      "The quick brown fox jumps over the lazy dog.\n" + \
      "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n" + \
      "abcdefghijklmnopqrstuvwxyz\n" + \
      "0123456789 !\"#$%&'()*+,-./\n" + \
      ":;<=>?@[\\]^_/{|}~"      # Initial foreground text
    SWATCH_WIDE  =  "40"        # Width of the color swatch in characters
    SWATCH_HIGH  =  "15"        # Height of the color swatch in lines
    SPACER_HIGH  =  "0.2i"      # Vertical space below radiobuttons
    HEX_DIGITS   =  3           # How many hex digits of color we show


# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self, master, bgColor, fgColor, callback ):

        #-- 1 --
        # [ master  :=  master with a new Frame gridded
        #   self    :=  that Frame ]
        Frame.__init__ ( self, master )

        #-- 2 --
        self._bgColor   =  bgColor
        self._fgColor   =  fgColor
        self._callback  =  callback

        #-- 3 --
        # [ self._isBackground  :=  a BooleanVar set to 1
        #   self._bgShow        :=  a StringVar containing the RGB readout
        #                           for color self._bgColor
        #   self._fgShow        :=  a StringVar containing the RGB readout
        #                           for color self._fgColor ]
        self._isBackground  =  BooleanVar ( )
        self._isBackground.set ( 1 )        # Background is default

        self._bgShow    =  StringVar ( )
        self._bgShow.set ( bgColor.show(self.HEX_DIGITS) )

        self._fgShow    =  StringVar ( )
        self._fgShow.set ( fgColor.show(self.HEX_DIGITS) )

        #-- 4 --
        # [ self  :=  self with all widgets created and gridded ]
        self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

    def _createWidgets ( self ):
        """ [ self  :=  self with all widgets created and gridded ]
        """

        #-- 1 --
        # [ self            :=  self with a new Label widget labeling
        #                       the whole mode radiobuttons
        #   self._topLabel  :=  that new Label widget ]
        self._topLabel  =  Label ( self,
          text="Select which color you're setting:" )
        self._topLabel.grid ( row=0, sticky=W )

        #-- 2 --
        # [ self              :=  self with a new Frame gridded
        #   self._radioFrame  :=  that new Frame ]
        self._radioFrame  =  Frame ( self, relief=RIDGE, borderwidth=4 )
        self._radioFrame.grid ( row=1, sticky=W, padx="0.1i", pady="0.1i" )

        #-- 3 --
        # [ self._radioFrame :=  self._radioFrame with a new Radiobutton,
        #                        variable=self._isBackground, value=1,
        #                        text="Background color", and set to
        #                        call self._callback(self._bgColor)
        #                        when selected
        #   self._bgRadio    :=  that new Radiobutton ]
        self._bgRadio  =  Radiobutton ( self._radioFrame,
                            command=self._fgBgHandler,
                            variable=self._isBackground, value=1,
                            text="Background color", anchor=W )
        self._bgRadio.grid ( row=0, sticky=W )

        #-- 4 --
        # [ self._radioFrame  :=  self._radioFrame with a new Label
        #                         linked to self._bgShow
        #   self._bgShowLabel :=  that Label ]
        self._bgShowLabel  =  Label ( self._radioFrame, anchor=W,
            font=self.MONO_FONT, textvariable=self._bgShow, relief=GROOVE )
        self._bgShowLabel.grid ( row=1, sticky=E )

        #-- 5 --
        # [ self._radioFrame  :=  self._radioFrame with a new Radiobutton,
        #                         variable=self._isBackground, value=0,
        #                         text="Foreground (text) color", and set to
        #                         call self._callback(self._fgColor)
        #                         when selected
        #   self._fgRadio     :=  that new Radiobutton ]
        self._fgSpacer  =  Frame ( self._radioFrame, height="0.1i" )
        self._fgSpacer.grid ( row=2 )

        self._fgRadio  =  Radiobutton ( self._radioFrame,
                            command=self._fgBgHandler,
                            variable=self._isBackground, value=0,
                            text="Foreground (text) color", anchor=W )
        self._fgRadio.grid ( row=3, sticky=W )

        #-- 6 --
        # [ self._radioFrame   :=  self._radioFrame with a Label linked
        #                          to self._fgShow
        #   self._fgShowLabel  :=  that Label ]
        self._fgShowLabel  =  Label ( self._radioFrame,
            font=self.MONO_FONT, textvariable=self._fgShow, relief=GROOVE )
        self._fgShowLabel.grid ( row=4, sticky=E )

        #-- 7 --
        # [ self._radioFrame   :=  self._radioFrame with a new label for the
        #                          foreground/background readouts
        #   self._columnLabel  :=  that new Label ]
        self._columnLabel  =  Label ( self._radioFrame,
                                      font=self.MONO_FONT,
                                      text="#RRR GGG BBB" )
        self._columnLabel.grid ( row=5, sticky=E )

        #-- 8 --
        # [ self               :=  self with a new Frame of height
        #                          self.SPACER_HIGH
        #   self._spacerFrame  :=  that new Frame ]
        self._spacerFrame  =  Frame ( self, height=self.SPACER_HIGH )
        self._spacerFrame.grid ( row=2 )

        #-- 9 --
        # [ self               :=  self with a new Label
        #                          with text to label the swatch
        #   self._swatchLabel  :=  that new Label ]
        self._swatchLabel  =  Label ( self,
          text="You can add to or change this text:" )
        self._swatchLabel.grid ( row=3, sticky=W )

        #-- 10 --
        # [ self          :=  self with a new Text widget using
        #                     self._bgColor and self._fgColor as the
        #                     background and foreground colors
        #   self._swatch  :=  that new Text widget ]
        self._swatchFont  =  tkFont.Font ( family="Helvetica", size="18" )

        self._swatch  =  Text ( self, width=self.SWATCH_WIDE,
                                bg=self._bgColor.xName(),
                                fg=self._fgColor.xName(),
                                font=self._swatchFont,
                                padx="24p", pady="24p",
                                height=self.SWATCH_HIGH )
        self._swatch.grid ( row=4, sticky=W )
        self._swatch.insert ( "1.0", self.SWATCH_TEXT )


# - - -   _ f g B g H a n d l e r   - - -

    def _fgBgHandler ( self ):
        if  self._isBackground.get():
            self._callback ( self._bgColor )
        else:
            self._callback ( self._fgColor )


# - - -   s e t   - - -

    def set ( self, color ):
        if  self._isBackground.get():
            self._bgColor  =  color                 # Save the color
            self._swatch["bg"]  =  color.xName()    # Set the swatch bg
            # Set the readout
            self._bgShow.set ( color.show(self.HEX_DIGITS) )
        else:
            self._fgColor  =  color
            self._swatch["fg"]  =  color.xName()
            self._fgShow.set ( color.show(self.HEX_DIGITS) )


# - - -   g e t   - - -

    def get ( self ):
        if  self._isBackground.get():
            return self._bgColor
        else:
            return self._fgColor


#================================================================


class ColorModel:
    """ Abstract class for the three color-space objects (RGB, CMY, HSV):

        Exports:
            ColorModel ( modelName, labelList ):
              [ if (modelName is a nonempty string)
                and (labelList is a list of three strings describing
                the parameters of this color model) ->
                  return a ColorModel object with those names ]
            .name():
              [ return self's model name ]
            .sliderLabel(i):
              [ if i is an integer in [0,2] ->
                  return the label for the (i)th color parameter
                  in self's model ]
            .slidersToColor ( sliders ):
              [ if sliderTuple is a sequence of three slider values
                in [0.0,1.0] representing the three parameters of
                self's color model ->
                  return a Color object representing the color ]
            .colorToSliders ( c ):
              [ if c is a Color object ->
                  return a tuple (s1, s2, s3) representing that color
                  as the three parameters of this color model ]

        The concrete classes must provide the .slidersToColor()
        and .colorToSliders() methods.

        For general information on the theory of the physics and
        representation of color, see: Foley, James D., Andries
        van Dam, Steven K. Feiner, and John F. Hughes.  Computer
        graphics: principles and practice, 2nd ed.
        Addison-Wesley, 1990, ISBN 0-201-12110-7.  See section
        13.3, "Color models."
    """


# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self, modelName, labelList ):
        self.modelName  =  modelName
        self.labelList  =  labelList


# - - -   n a m e   - - -

    def name ( self ):
        return self.modelName


# - - -   s l i d e r L a b e l   - - -

    def sliderLabel ( self, i ):
        return self.labelList[i]        


#================================================================

class HSV_Model(ColorModel):
    """ Hue-saturation-value color space model; value is sometimes
        called brightness.
    """


# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self ):
        ColorModel.__init__ ( self, "HSV", [ "hue", "saturation", "value" ] )


# - - -   s l i d e r s T o C o l o r   - - -

    def slidersToColor ( self, sTuple ):
        """ See Foley & van Dam's algorithm HSV_To_RGB.
        """     
        h  =  sTuple[0]
        s  =  sTuple[1]
        v  =  sTuple[2]

        if  s == 0.0:
            return Color ( ( v, v, v ) )

        if  h == 1.0:       # Treat hue of 1 as hue of 0 (wraparound)
            h = 0.0
        else:
            h = h * 6.0     # Normalize to [0,6)

        (f,i) = math.modf(h)        # (fractional part, integer part)
        i     = int ( i )           # Truncate integer part
        p     = v * ( 1.0 - s )
        q     = v * ( 1.0 - s * f )
        t     = v * ( 1.0 - s * ( 1.0 - f ) )

        if  i == 0:
            return Color ( ( v, t, p ) )
        elif i == 1:
            return Color ( ( q, v, p ) )
        elif i == 2:
            return Color ( ( p, v, t ) )
        elif i == 3:
            return Color ( ( p, q, v ) )
        elif i == 4:
            return Color ( ( t, p, v ) )
        else:
            return Color ( ( v, p, q ) )


# - - -   c o l o r T o S l i d e r s   - - -

    def colorToSliders ( self, c ):
        """ See Foley & van Dam's algorithm RGB_To_HSV.
        """
        v = maxColor = max ( c.r, c.g, c.b )
        minColor = min ( c.r, c.g, c.b )

        #--
        # Calculate saturation
        #--

        if  maxColor == 0.0:
            s = 0.0     # Saturation is 0 if all colors are 0
        else:
            s = ( maxColor - minColor ) / maxColor

        #--
        # Now find the hue
        #--
        
        if  s == 0.0:
            h = 0.0     # Hue is undefined; use red arbitrarily
        else:
            delta = maxColor - minColor

            if  c.r == maxColor:        # Between Y and M
                h = ( c.g - c.b ) / delta
            elif c.g == maxColor:       # Between C and Y
                h = 2.0 + ( c.b - c.r ) / delta
            else:                       # Between M and C
                h = 4.0 + ( c.r - c.g ) / delta

            if h < 0.0:         # Rotate negative values to [0,6]
                h = h + 6.0

            h  =  h / 6.0       # Normalize to [0,1]

        return ( h, s, v )


#================================================================

class RGB_Model(ColorModel):
    """ RGB color space model.
    """

# - - -   _ _ i n i t _ _   - - -
        
    def __init__ ( self ):
        ColorModel.__init__ ( self, "RGB", [ "red", "green", "blue" ] )


# - - -   s l i d e r s T o C o l o r   - - -

    def slidersToColor ( self, sTuple ):
        return Color ( sTuple )


# - - -   c o l o r T o S l i d e r s   - - -

    def colorToSliders ( self, c ):
        return ( c.r, c.g, c.b )


#================================================================

class CMY_Model(ColorModel):
    """ CMY color space model.
    """


# - - -   _ _ i n i t _ _   - - -

    def __init__ ( self ):
        ColorModel.__init__ ( self, "CMY", [ "cyan", "magenta", "yellow" ] )



# - - -   s l i d e r s T o C o l o r   - - -

    def slidersToColor ( self, sTuple ):
        return Color ( ( 1.0 - sTuple[0],
                         1.0 - sTuple[1],
                         1.0 - sTuple[2] ) )


# - - -   c o l o r T o S l i d e r s   - - -

    def colorToSliders ( self, c ):
        return ( 1.0 - c.r, 1.0 - c.g, 1.0 - c.b )


#================================================================
# Main
#----------------------------------------------------------------

app = Application()
app.master.title("D-PAT %s: Performance Analysis Tool" % EXTERNAL_VERSION)
app.mainloop()
