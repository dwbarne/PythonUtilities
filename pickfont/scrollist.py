"""scrollist.py:  Scrolled listbox compound widget

    $Revision: 1.1 $  $Date: 2000/12/19 01:39:29 $
"""

import string
from Tkinter import *

DEFAULT_WIDTH   =  40
DEFAULT_HEIGHT  =  25

class ScrolledList(Frame):
    """Scrolled list widget

      Exports:
        ScrolledList ( parent, width=None, height=None, callback=None ):
          [ if (parent is a Frame widget)
            and (width is the width in characters, defaulting to
            DEFAULT_WIDTH)
            and (height is the number of lines visible, defaulting to
            DEFAULT_HEIGHT)
            and (callback is a procedure with calling sequence
            callback ( lineNo )) ->
              parent  :=  parent with a new Frame added containing an empty
                          listbox and scrollbar, ungridded, that will call
                          callback(i) when double-clicked on the (i)th item
              return that new Frame ]
        .parent:    [ as passed to constructor ]
        .width:     [ as passed to constructor, or default ]
        .height:    [ as passed to constructor, or default ]
        .callback:  [ as passed to constructor ]
        .count():   [ returns number of lines in self ]
        self[i]:
          [ if 0 <= i < self.count() ->
              return the (i)th element of self's listbox
            else -> raise IndexError ]
        .append ( s ):
          [ if s is a string ->
              self  :=  self with s added as its new last line ]
        .insert ( linex, s ):
          [ if (linex is an integer) and (s is a string) ->
              if 0<=linex<=(number of lines in self) ->
                self  :=  self with s inserted as a new line before
                          position linex
              else ->
                self  :=  self with s added as its new last line ]
        .delete ( linex ):
          [ if (0<=linex<(number of lines in self)) ->
              self  :=  self with line linex deleted
            else -> I ]
        .clear():   [ self  :=  self without any lines ]

      State/Invariants:
        .listbox:   [ self's Listbox component ]
        .yscroll:   [ self's vertical scrollbar component ]
    """


# - - -   S c r o l l e d L i s t . _ _ i n i t _ _   - - -

    def __init__ ( self, master, width=None, height=None, callback=None ):
        """Constructor for ScrolledList compound widget
        """

        #-- 1 --
        # [ self  :=  a new Frame in master ]
        Frame.__init__ ( self, master )

        #-- 2 --
        self.master    =  master
        self.callback  =  callback

        if  width:  self.width  =  width
        else:       self.width  =  DEFAULT_WIDTH

        if  height:  self.height  =  height
        else:        self.height  =  DEFAULT_HEIGHT

        #-- 3 --
        # [ self  :=  self with all widgets added and gridded ]
        self.__createWidgets ()


# - - -   S c r o l l e d L i s t . _ _ c r e a t e W i d g e t s   - - -

    def __createWidgets ( self ):
        """ [ self  :=  self with all widgets added and gridded ]
        """

        #-- 1 --
        # [ self.yscroll  :=  a new vertical Scrollbar in self ]
        self.yscroll  =  Scrollbar ( self, orient=VERTICAL )
        self.yscroll.grid ( row=0, column=1, sticky=N+E+S )

        #-- 2 --
        # [ self.listbox  :=  a new Listbox in self with its vertical
        #                     scrolling slaved to self.yscroll, and
        #                     calling self.__pickHandler() when a line
        #                     is double-clicked ]
        self.listbox  =  Listbox ( self, relief=SUNKEN,
            width=self.width, height=self.height, borderwidth=2,
            yscrollcommand=self.yscroll.set )
        self.listbox.grid ( row=0, column=0, sticky=N+W+S )
        self.listbox.bind ( "<Double-Button-1>", self.__pickHandler )
        self.yscroll["command"]  =  self.listbox.yview


# - - -   S c r o l l e d L i s t . _ _ p i c k H a n d l e r   - - -

    def __pickHandler ( self, event ):
        """Handler for double-clicking on self.listbox
        """

        #-- 1 --
        if  self.callback is None:
            return

        #-- 2 --
        # [ if there is a current selection ->
        #     linex  :=  its index as an integer
        #   else ->
        #     return ]
        curSel  =  self.listbox.curselection()
        if  len(curSel) == 0:
            return
        else:
            linex  =  string.atoi(curSel[0])

        #-- 3 --
        self.callback ( linex )


# - - -   S c r o l l e d L i s t . c o u n t   - - -

    def count ( self ):
        """Returns the number of lines in self's listbox

            NOTE:  Originally I called this method __len__(), so that
            anyone could use the len() built-in function to get the
            number of entries.  But doing so led to bizarre bugs inside
            the basic Tkinter Widget class.  Apparently someone needs
            to call len() on Frame widgets, and my overriding it made
            something break.
        """
        return self.listbox.size()


# - - -   S c r o l l e d L i s t . _ _ g e t i t e m _ _    - -

    def __getitem__ ( self, k ):
        """Get the (k)th item from self's listbox
        """
        if  not ( 0 <= k < self.count() ):
            raise IndexError, ( "ScrolledList[%d] out of range" % k )
        else:
            return self.listbox.get ( k )


# - - -   S c r o l l e d L i s t . a p p e n d   - - -

    def append ( self, s ):
        """Add s as the new last element of self's listbox
        """
        self.listbox.insert ( END, s )


# - - -   S c r o l l e d L i s t . i n s e r t   - - -

    def insert ( self, linex, s ):
        """Insert s before position linex
        """

        #-- 1 --
        if  not ( 0 <= linex < self.count() ):
            where  =  END
        else:
            where  =  linex

        #-- 2 --
        self.listbox.insert ( where, s )


# - - -   S c r o l l e d L i s t . d e l e t e   - - -

    def delete ( self, linex ):
        """Delete a line from self's listbox
        """
        #-- 1 --
        if  not ( 0 <= linex < self.count() ):
            return

        #-- 2 --
        self.listbox.delete ( linex )


# - - -   S c r o l l e d L i s t . c l e a r   - - -

    def clear ( self ):
        """Delete all lines from self's listbox
        """
        self.listbox.delete ( 0, END )
