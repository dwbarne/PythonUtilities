#!/usr/bin/env python
#================================================================
from Tkinter import *			# for gui
from tkFileDialog import *		# for 'askfilename'

class App(Frame):									# App inherits from Frame
    def __init__ ( self ):							# defines mainloop
        Frame.__init__(self, None)
        self.grid()
        b1=Button(self, text="Get a file name", command=self.get)
        b1.grid()
        b2=Button(self, text="Print file name", command=self.printer)
        b2.grid()
        qb=Button(self, text="Quit", command=self.quit)
        qb.grid()

    def get(self):									# get filename
        self.filenm = askopenfilename()

    def printer(self):
        print "FILE NAME IS <%s>" % self.filenm		# print filename

# - - - m a i n - - -

app=App()			# instantiate App()
app.mainloop()		# run mainloop