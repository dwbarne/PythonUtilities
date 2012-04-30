#!/usr/bin/env python
#--
# pickfont.py:  A tool allowing interactive selection of fonts
#--

PRODUCT_NAME      =  "pickfont.py"
EXTERNAL_VERSION  =  "1.0"
INTERNAL_VERSION  =  "$Revision: 1.3 $  $Date: 2001/03/18 23:40:42 $"

#================================================================
# Imports
#----------------------------------------------------------------

import sys
import string
from Tkinter import *       # Tk widgets
from Dialog import *        # Popup Tk dialogs
from tkFont import *        # Tk fonts

sys.path.insert(0, "/u/john/tcc/python/lib")
from dropdown import *      # DropDown menu widget
from scrollist import *     # ScrolledList widget

#================================================================
# Globals for widget appearance
#----------------------------------------------------------------

FAM_HIGH    =  30        # Number of lines visible in family list
FAM_WIDE    =  30        # Width of family list in characters
TEXT_HIGH   =  4         # Number of lines in text widget
TEXT_WIDE   =  60        # Width of Text widget
BACKGROUND  =  "#fff4e0" # Default background
ACTIVE_FG   =  "#664400"      # Standard active foreground color
ACTIVE_BG   =  "#ffdd77"      # Standard active background color
TROUGH      =  "#997744"      # Standard trough color


#================================================================
# Verification functions
#----------------------------------------------------------------
# selected-font(app) ==
#   the font specified by family app.__families[app.__familyx],
#   size app.__sizeVar, weight app.__wtVar, and slant app.__slantVar
#----------------------------------------------------------------



# - - - - -   c l a s s   A p p   - - - - -

class App(Frame):
    """Tkinter application root for the font-picker

      Exported methods:
        Application():
          [ X  :=  X with a new font-picker tool ]

      Grid plan:       0              1
          +--------------+--------------+
        0 | .__mainLabel                |
          +--------------+--------------+
        1 | .__famPanel  | .__mainPanel |
          +--------------+--------------+

      Widgets:
        .__mainLabel:  Label for entire app
        .__famPanel:
            .__famLabel:  Label for families scrolling list
            .__famList:  ScrolledList for font families
        .__mainPanel:
            .__sizePanel:  Means of setting font size
                .__sizeLabel:  Label for size entry
                .__sizeEntry:  Entry for point size
                .__sizeSuffix:  Label following entry
                .__sizeSetButton:  Button to set size
            .__wtPanel:  Means of setting font weight
                .__wtLabel:  Label for font weight panel
                .__wtRB0:  Radiobutton for weight normal
                .__wtRB1:  Radiobutton for weight bold
            .__slantPanel:  Means for setting font slant
                .__slantLabel:  Label for font slant panel
                .__slantRB1:  Radiobutton for slant normal
                .__slantRB2:  Radiobutton for slant italic
            .__text:  Text widget for displaying selected font
            .__actualLabel:  Label to show actual font in use
            .__quitButton:  Button to terminate execution

      State/Invariants:
        .__families:  List of family names
        .__familyx:  Index in self.__families of current family
        .__sizeVar:  StringVar for font size
        .__wtVar:  BooleanVar for weight radiobuttons
        .__slantVar:  BooleanVar for slant radiobuttons
        .__defaultFont:  Starting font
    """


# - - -   A p p . _ _ i n i t _ _   - - -

    def __init__ ( self, master=None ):
        """Constructor for App
        """
        #-- 1 --
        # [ if master is None ->
        #     root window  :=  new Frame containing self
        #     self         :=  that Frame ]
        Frame.__init__ ( self, master )
        self.grid()
        self["bg"] = BACKGROUND
        self.master.option_add("*background", BACKGROUND)
        self.master.option_add("*activeforeground", ACTIVE_FG)
        self.master.option_add("*activebackground", ACTIVE_BG)
        self.master.option_add("*troughcolor", TROUGH)

        #-- 2 --
        # [ self.__defaultFont  :=  a Font
        #   self.__bigFont      :=  a Font ]
        self.__defaultFont  =  Font ( family="times", size=12 )
        self.__bigFont      =  Font ( family="lucidabright", size=24 )

        #-- 3 --
        self.__familyVar  =  StringVar()
        self.__sizeVar    =  StringVar()
        self.__wtVar      =  BooleanVar()
        self.__slantVar   =  BooleanVar()

        #-- 4 --
        # [ self.__families   :=  list of all font families, sorted
        #   self.__familyx    :=  index of self.__defaultFont in that list
        #   self.__familyVar  :=  name of self.__defaultFont
        #   self.__sizeVar    :=  size of self.__defaultFont
        #   self.__wtVar      :=  1 if self.__defaultFont is bold, else 0
        #   self.__slantVar   :=  1 if self.__defaultFont is italic, else 0
        self.__families  =  map ( None, families() )
        self.__families.sort()
        self.__familyx  =  self.__families.index("Times")
        self.__familyVar.set(self.__defaultFont)
        self.__sizeVar.set ( self.__defaultFont.actual("size") )

        if  self.__defaultFont.actual("weight") != "normal":
            self.__wtVar.set ( 1 )
        else:
            self.__wtVar.set ( 0 )

        if  self.__defaultFont.actual("slant") != "roman":
            self.__slantVar.set ( 1 )
        else:
            self.__slantVar.set ( 0 )

        #-- 5 --
        # [ self  :=  self with all widgets created and gridded ]
        self.__createWidgets()

        #-- 6 --
        # [ self.__famList  :=  self.__famList with names from
        #                       self.__families appended ]
        for  family in self.__families:
            self.__famList.append ( family )

        #-- 5 --
        # [ if self.__sizeVar is a valid integer in string form ->
        #     self.__text  :=  self.__text with its font set to
        #         selected-font(self)
        #   else ->
        #     X  :=  X with a popup error dialog
        #     terminate execution ]
        result  =  self.__setFont()
        if  not result:
            sys.exit(0)

        #-- 6 --
        # [ self.__text  :=  self.__text with sample text inserted ]
        self.__text.insert ( END,
            "0O 1Il| Daft buxom jonquil, Zephyr's gawky vice.\n"
            "abcdefghijklmnopqrstuvwxyz\n"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ" )


# - - -   A p p . _ _ c r e a t e W i d g e t s   - - -

    def __createWidgets ( self ):
        """ [ self  :=  self with all widgets created and gridded ]
        """
        self.__mainLabel  =  Label ( self, text="Tkinter Font selector",
            font=self.__bigFont )
        self.__mainLabel.grid ( row=0, column=0, columnspan=2,
            sticky=N+W, pady=5 )

        self.__famPanel  =  self.__createFamPanel ()
        self.__famPanel.grid ( row=1, column=0, sticky=N+W, padx=5, pady=5 )

        self.__mainPanel  =  self.__createMainPanel ()
        self.__mainPanel.grid ( row=1, column=1, sticky=N+W, padx=5, pady=5 )


# - - -   A p p . _ _ c r e a t e F a m P a n e l   - - -

    def __createFamPanel ( self ):
        """Create self.__famPanel() and its contained widgets

          [ self  :=  self with a new Frame widget added, ungridded,
                      containing all widgets in self.__famPanel
            return that new Frame ]
        """
        rowx  =  0
        f     =  Frame ( self, relief=RIDGE, borderwidth=4 )

        self.__famLabel  =  Label ( f, text="Double-click to select family:" )
        self.__famLabel.grid ( row=rowx, column=0, sticky=N+W, pady=5 )
        rowx  =  rowx + 1

        self.__famList  =  ScrolledList ( f,
            width=FAM_WIDE, height=FAM_HIGH,
            callback=self.__familyHandler )
        self.__famList.grid ( row=rowx, column=0, sticky=N+W, pady=5 )
        self.__famList.listbox["font"]  =  self.__defaultFont
        self.__famList.yscroll["troughcolor"]  =  TROUGH
        self.__famList.yscroll["activebackground"]  =  ACTIVE_BG
        rowx  =  rowx + 1

        return f


# - - -   A p p . _ _ c r e a t e M a i n P a n e l   - - -

    def __createMainPanel ( self ):
        """Create self.__mainPanel() and its contained widgets

          [ self  :=  self with a new Frame widget added, ungridded,
                      containing all widgets in self.__mainPanel ]
        """
        rowx  =  0
        f     =  Frame ( self )

        self.__sizePanel  =  self.__createSizePanel ( f )
        self.__sizePanel.grid ( row=rowx, column=0, sticky=N+W, pady=5 )
        rowx  =  rowx + 1

        self.__wtPanel  =  self.__createWtPanel ( f )
        self.__wtPanel.grid ( row=rowx, column=0, sticky=N+W, pady=5 )
        rowx  =  rowx + 1

        self.__slantPanel  =  self.__createSlantPanel ( f )
        self.__slantPanel.grid ( row=rowx, column=0, sticky=N+W, pady=5 )
        rowx  =  rowx + 1

        self.__text  =  Text ( f, width=TEXT_WIDE, height=TEXT_HIGH,
            relief=SUNKEN, borderwidth=3 )
        self.__text.grid ( row=rowx, column=0, sticky=N+W, pady=5 )
        rowx  =  rowx + 1

        self.__actualLabel  =  Label ( f, text="" )
        self.__actualLabel.grid ( row=rowx, column=0, sticky=N+W, pady=5 )
        rowx  =  rowx + 1

        self.__quitButton  =  Button ( f, text="Quit", command=self.quit,
            borderwidth=6,
            font=self.__bigFont,
            padx=20, pady=20,
            activeforeground=ACTIVE_FG,
            activebackground=ACTIVE_BG )
        self.__quitButton.grid ( row=rowx, column=0, sticky=N+W, pady=5 )
        rowx  =  rowx + 1

        return f


# - - -   A p p . _ _ c r e a t e S i z e P a n e l   - - -

    def __createSizePanel ( self, parent ):
        """Create self.__sizePanel and its widgets

          [ self  :=  self with a new Frame widget added, ungridded,
                      containing all widgets in self.__sizePanel ]
        """
        colx  =  0
        f     =  Frame ( parent )

        self.__sizeLabel  =  Label ( f, text="Size:" )
        self.__sizeLabel.grid ( row=0, column=colx, sticky=N+W )
        colx  =  colx + 1

        self.__sizeEntry  =  Entry ( f, width=4,
            relief=SUNKEN, borderwidth=2,
            textvariable=self.__sizeVar )
        self.__sizeEntry.grid ( row=0, column=colx, sticky=N+W )
        colx  =  colx + 1
        self.__sizeEntry.bind ( "<Key-Return>", self.__bindSizeHandler )

        self.__sizeSuffix  =  Label ( f, text="points (- for pixels)" )
        self.__sizeSuffix.grid ( row=0, column=colx, sticky=N+W )
        colx  =  colx + 1

        self.__sizeSetButton  =  Button ( f, text="Set size",
            activeforeground=ACTIVE_FG,
            activebackground=ACTIVE_BG,
            command=self.__setSizeHandler )
        self.__sizeSetButton.grid( row=0, column=colx, sticky=N+W, padx=5 )
        colx  =  colx + 1

        return f


# - - -   A p p . _ _ c r e a t e W t P a n e l   - - -

    def __createWtPanel ( self, parent ):
        """Create self.__wtPanel and its widgets

          [ self  :=  self with a new Frame widget added, ungridded,
                      containing all widgets in self.__wtPanel ]
        """
        colx  =  0
        f     =  Frame ( parent )

        self.__wtLabel  =  Label ( f, text="Weight:" )
        self.__wtLabel.grid ( row=0, column=colx, sticky=N+W )
        colx  =  colx + 1

        self.__wtRB0  =  Radiobutton ( f, variable=self.__wtVar, value=0,
            activebackground=ACTIVE_BG,
            text="normal", command=self.__wtHandler )
        self.__wtRB0.grid ( row=0, column=colx, sticky=N+W, padx=5 )
        colx  =  colx + 1

        self.__wtRB1  =  Radiobutton ( f, variable=self.__wtVar, value=1,
            activebackground=ACTIVE_BG,
            text="bold", command=self.__wtHandler )
        self.__wtRB1.grid ( row=0, column=colx, sticky=N+W, padx=5 )
        colx  =  colx + 1

        return f


# - - -   A p p . _ _ c r e a t e S l a n t P a n e l   - - -

    def __createSlantPanel ( self, parent ):
        """Create self.__slantPanel and its widgets

          [ self  :=  self with a new Frame widget added, ungridded,
                      containing all widgets in self.__slantPanel ]
        """
        colx  =  0
        f     =  Frame ( parent )

        self.__slantLabel  =  Label ( f, text="Slant:" )
        self.__slantLabel.grid ( row=0, column=colx, sticky=N+W )
        colx  =  colx + 1

        self.__slantRB0  =  Radiobutton ( f, variable=self.__slantVar, value=0,
            activebackground=ACTIVE_BG,
            text="normal", command=self.__slantHandler )
        self.__slantRB0.grid ( row=0, column=colx, sticky=N+W, padx=5 )
        colx  =  colx + 1

        self.__slantRB1  =  Radiobutton ( f, variable=self.__slantVar, value=1,
            activebackground=ACTIVE_BG,
            text="italic", command=self.__slantHandler )
        self.__slantRB1.grid ( row=0, column=colx, sticky=N+W, padx=5 )
        colx  =  colx + 1

        return f


# - - -   A p p . _ _ s e t F o n t   - - -

    def __setFont ( self ):
        """Set self.__text's font to the currently selected font

          [ if self.__sizeVar is a valid integer in string form ->
              self.__text  :=  self.__text with its font set to
                  selected-font(self)
              return 1
            else ->
              X  :=  X with a popup error dialog
              return 0
        """
        #-- 1 --
        family  =  self.__families[self.__familyx]

        #-- 2 --
        # [ if self.__sizeVar contains a valid integer as a string ->
        #     size  :=  that value as an integer
        #   else ->
        #     X  :=  X with a popup error dialog
        #     return ]
        try:
            size    =  int(self.__sizeVar.get())
        except:
            d  =  Dialog ( self, title="Message", bitmap="info",
                           text="Size must be an integer",
                           default=0,   # First button is the default
                           strings = ("OK",) )    # Only one button: OK
            return 0

        #-- 3 --
        if  self.__wtVar.get(): wt  =  "bold"
        else:                   wt  =  "normal"

        #-- 4 --
        if  self.__slantVar.get():      slant  =  "italic"
        else:                           slant  =  "roman"

        #-- 5 --
        # [ font         :=  the font specified by family, size, wt, and slant
        #   self.__text  :=  self.__text switched to that font ]
        font  =  Font ( family=family, size=size, weight=wt, slant=slant )
        self.__text["font"]  =  font

        #-- 6 --
        # [ self.__actualLabel  :=  self.__actualLabel displaying the actual
        #       family, size, weight, and slant of font ]
        attrs    =  [ font.actual("family"), font.actual("size") ]
        weight   =  font.actual("weight")
        slant    =  font.actual("slant")

        if  weight != "normal":
            attrs.append ( weight )

        if  slant != "roman":
            attrs.append ( slant )

        self.__actualLabel["text"]  =  string.join ( attrs, " " )

        #-- 7 --
        return 1


# - - -   A p p . _ _ f a m i l y H a n d l e r   - - -

    def __familyHandler ( self, linex ):
        """Handler for selection of a family from self.__famList

          [ if linex is the index of a line in self.__famList ->
              self.__familyx  :=  linex
              self.__text     :=  self.__text with its font set to
                  selected-font(self) ]
        """
        self.__familyx  =  linex
        self.__setFont()


# - - -   A p p . _ _ b i n d S i z e H a n d l e r   - - -

    def __bindSizeHandler ( self, event ):
        """Handler for enter key in size entry, .bind() version

          [ if self.__sizeVar is a valid integer ->
              self.__text  :=  self.__text with its font size changed to
                               selected-font(self)
            else ->
              X  :=  X with an error popup ]
        """
        self.__setFont()


# - - -   A p p . _ _ s e t S i z e H a n d l e r   - - -

    def __setSizeHandler ( self ):
        """Handler for enter key in size entry, button version

          [ if self.__sizeVar is a valid integer ->
              self.__text  :=  self.__text with its font size changed to
                               selected-font(self)
            else ->
              X  :=  X with an error popup ]
        """
        self.__setFont()


# - - -   A p p . _ _ w t H a n d l e r   - - -

    def __wtHandler ( self ):
        """Handler for weight radiobuttons

          [ if self.__sizeVar is a valid integer ->
              self.__text  :=  self.__text with its font size changed to
                               selected-font(self)
            else ->
              X  :=  X with an error popup ]

        """
        self.__setFont()


# - - -   A p p . _ _ s l a n t H a n d l e r   - - -

    def __slantHandler ( self ):
        """Handler for slant radiobuttons

          [ if self.__sizeVar is a valid integer ->
              self.__text  :=  self.__text with its font size changed to
                               selected-font(self)
            else ->
              X  :=  X with an error popup ]
        """
        self.__setFont()


# - - - - -   M a i n   - - - - -

app  =  App()
app.master.title ( "%s %s" % ( PRODUCT_NAME, EXTERNAL_VERSION ) )
app.mainloop()
