#!/usr/bin/env python
#================================================================

from Tkinter import *
import tkFont

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        self.flashing = False

        self.buttonFont = tkFont.Font ( family="Helvetica",
            size="20" )
        self.createWidgets()

    def createWidgets(self):
        self.panicButton = Button ( self, text="Panic",
            activebackground="red", activeforeground="green",
            font=self.buttonFont, command=self.panicHandler )
        self.panicButton.grid ( row=0, column=0 )
        self.afterNo = self.panicButton.after(500, self.flash)
        print "@@@ self.afterNo=", self.afterNo
        print "@@@ type(self.afterNo)=", type(self.afterNo)
        self.flashing = True

        self.quietButton = Button ( self, text="Quiet",
            command=self.shutUp,
            font=self.buttonFont )
        self.quietButton.grid ( row=0, column=1 )

        self.quitButton = Button ( self, text="Quit",
            font=self.buttonFont,
            command=self.quit )
        self.quitButton.grid( row=0, column=99)

    def panicHandler(self):
        print "Panic!"
        self.panicButton.after(500, self.flash)
        self.flashing = True

    def shutUp ( self ):
        print "Shut up"
        self.flashing = False
        print "@@@ self.afterNo=", self.afterNo
        self.after_cancel(self.afterNo)

    def flash(self):
        self.panicButton.flash()
        if  self.flashing:
            self.panicButton.after(500, self.flash)

app = Application()
app.master.title("Sample application")
app.mainloop()