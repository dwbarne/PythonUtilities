#!/usr/local/bin/python
#--
# dropdown.py:  Generic drop-down widget (using radiobuttons)
#   $Revision: 1.4 $  $Date: 2003/11/01 04:49:22 $
#--

from Tkinter import *       # Interface to Tk widgets


# - - - - -   c l a s s   D r o p D o w n   - - - - -

class DropDown(Frame):
    """Generic drop-down menus using radiobuttons

      Exports:
        DropDown ( parent, var, choiceList ):
          [ if (parent is a Frame)
            and (var is a StringVar)
            and (choiceList is a list of strings) ->
              parent  :=  parent with a new Frame widget added (ungridded)
                          containing a drop-down menu allowing the user to
                          select elements of choiceList with radiobuttons,
                          displaying the currently selected string on the
                          button, and with the first element selected, and
                          with the current choice slaved to var
              return that new Frame widget
        .choiceList:    [ as passed to constructor ]
        .var:           [ as passed to constructor ]
        .set(i):
          [ if (0 <= i < len(self.choiceList)) ->
              self  :=  self with self.choiceList[i] selected and displayed
            else -> raise IndexError ]
        .get():
          [ return the index of the currently selected choice in choiceList ]

      State/Invariants/Widgets:
        .__mb:      [ the MenuButton widget for self ]
        .__menu:    [ the Menu widget for self.__mb ]
        .__rbList:  [ list of radiobuttons in self.__menu ]
        .__index:   [ the index of the currently selected choice ]
    """

# - - -   D r o p D o w n . _ _ i n i t _ _   - - -

    def __init__ ( self, parent, var, choiceList ):
        """Constructor for a DropDown widget
        """
        #-- 1 --
        # [ parent  :=  parent with self added as a new frame ]
        Frame.__init__ ( self, parent, relief=RAISED, borderwidth=2 )

        #-- 6 --
        self.var         =  var
        self.choiceList  =  choiceList
        self.__index     =  0

        #-- 2 --
        # [ self  :=  self with self.__mb added ]
        self.__mb  =  Menubutton ( self, text=choiceList[0] )
        self.__mb.grid ( row=0, column=0 )

        #-- 3 --
        # [ self.__mb    :=  self.__mb with a new Menu added
        #   self.__menu  :=  that new Menu ]
        self.__menu  =  Menu ( self.__mb )

        #-- 4 --
        # [ self.__mb  :=  self.__mb with radiobuttons added for each
        #       choice in choiceList, such that each radiobutton
        #       sets self.__mb's text to self.var and self.__index
        #       to the index of the radiobutton ]
        self.__rbList  =  []
        for  i in range(len(choiceList)):
            choice  =  choiceList[i]
            def handler(s=self, i=i):
                self.__index  =  i
                self.__mb["text"]  =  self.var.get()
            rb  =  self.__menu.add_radiobutton ( label=choice,
                value=choice, variable=self.var, command=handler )
            self.__rbList.append ( rb )

        #-- 5 --
        # [ self.__mb  :=  self.__mb with self.__menu as its menu ]
        self.__mb["menu"]  =  self.__menu


# - - -   D r o p D o w n . s e t   - - -

    def set ( self, i ):
        """Set self to the (i)th choice.
        """
        #-- 1 --
        # [ if (0 <= i < len(self.choiceList)) ->
        #     value  :=  self.choiceList[i]
        #   else -> raise IndexError ]
        value  =  self.choiceList[i]

        #-- 2 --
        # [ self.var      :=  var with self.choiceList[i] as its value
        #   self          :=  self displaying self.choiceList[i]
        #   self.__index  :=  i ]
        self.var.set ( self.choiceList[i] )
        self.__mb["text"]  =  self.choiceList[i]
        self.__index       =  i


# - - -   D r o p D o w n . g e t   - - -

    def get ( self ):
        """Return the index of the currently selected entry
        """
        return self.__index
