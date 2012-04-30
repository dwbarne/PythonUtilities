#!/usr/bin/env python
# flasher.py
#================================================================

from Tkinter import *
import tkFont

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.flashing = False
        self.buttonFont = tkFont.Font ( family="Helvetica",
            size="10" )            
        self.createWidgets()

    def createWidgets(self):
        self.panicButton = Button ( self, text="Panic",
            activebackground="red", activeforeground="green",
            font=self.buttonFont, command=self.panicHandler )
        self.panicButton.grid ( row=0, column=0 )
        self.count=0
        self.afterNo = self.panicButton.after(1500, self.flash)
        self.count=1
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
        print "\nPanic!"
        self.panicButton.after(5500, self.flash)
        self.flashing = True

    def shutUp ( self ):
        print "\nI'll be quiet now!"
        self.flashing = False
        self.panicButton.after_cancel(self.afterNo)

    def flash(self):
        print '\n self.count = %d' % self.count
        self.panicButton.flash()
        if  self.flashing:
            self.panicButton.after(1500, self.flash)

app1 = Application()
app1.master.title("Sample application #1")
app1.mainloop()
