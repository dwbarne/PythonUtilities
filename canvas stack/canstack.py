#!/usr/bin/env python
#================================================================
# canstack: play with canvas stacking
#================================================================

from Tkinter import *
import tkFont

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont = tkFont.Font ( family="Helvetica",
            size="40" )
        self.createWidgets()
              
        

    def createWidgets(self):
        """Create all widgets."""
        self.can = Canvas ( self, width=600, height=600,
                            bg="#eeeeee" )
        self.can.grid(row=0, column=0, columnspan=99)

        recList = []
        for i in range(5):
            oid = self.can.create_rectangle(i*20+20, i*20+20,
                    i*20+120, i*20+120,
                    fill="green",
                    outline="red", width="5")
            recList.append(oid)
        print "oids are:", recList

        self.cycleButton = Button ( self, text="Cycle",
            font=self.buttonFont,
            command=self.cycleHandler )
        self.cycleButton.grid ( row=99, column=1)

        self.quitButton = Button ( self, text="Quit",
            font=self.buttonFont,
            command=self.quit )
        self.quitButton.grid(row=99, column=0)

    def cycleHandler ( self ):
        """Take the thing on top of the stack and make it the bottom.
        """
        #-- 1 --
        # [ dList  :=  oids of all objects in self.can in display
        #              order, lowest to highest
        #   topId  :=  oid of the highest thing on the display list ]
        dList  =  self.can.find_all()
        print "Display list is now:", dList
        topId  =  dList[-1]

        #-- 2 --
        # [ self.can  :=  self.c
        an with object topId moved to 
        #       the bottom of the display list ]
        self.can.tag_lower ( topId, dList[0] )        

#================================================================

app = Application()
app.master.title("Sample application")
app.mainloop()


