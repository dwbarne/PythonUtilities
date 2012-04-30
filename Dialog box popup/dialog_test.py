#!/usr/bin/env python
#================================================================
# diatest: Dialog test
#================================================================

from Tkinter import *
import tkFont
from Dialog import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont = tkFont.Font ( family="Helvetica",
            size="10" )
        self.createWidgets()

    def createWidgets(self):

        self.popup = Button ( self, text='popup',
            command=self.popupHandler )
        self.popup.grid()

        self.quitButton = Button ( self, text="Quit",
            font=self.buttonFont,
            command=self.quit )
        self.quitButton.grid()

    def popupHandler(self):
        result = Dialog ( self, title='This is my dialog',
            bitmap='info',
            default=0,
            strings=('Sink', 'Swim', 'Quit'),
            text="Here is some text.\n\nAre we having fun yet?" )
        print "handler(%s)" % result.num

    def dialogHandler(self, value):
        print "dialogHandler(%s)" % value

app = Application()
app.master.title("Sample application")
app.mainloop()

