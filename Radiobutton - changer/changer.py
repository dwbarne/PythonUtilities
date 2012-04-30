#!/usr/bin/env python
#================================================================
# changer: Left frame has radiobuttons that make different
#   things display in the right frame
#================================================================

from Tkinter import *
import tkFont

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont = tkFont.Font ( family="Helvetica",
            size="10" )
        self.createWidgets()

    def createWidgets(self):
        self.leftFrame = Frame ( self )
        self.leftFrame.grid ( row=0, column=0 )

        self.which = IntVar()
        self.which.set(0)

        self.radio1 = Radiobutton ( self.leftFrame,
            command=self.radioHandler,
            text='A', variable=self.which, value=0 )
        self.radio1.grid ( row=0 )

        self.radio2 = Radiobutton ( self.leftFrame,
            command=self.radioHandler,
            text='B', variable=self.which, value=1 )
        self.radio2.grid ( row=1 )

        self.rightFrame = Frame ( self )
        self.rightFrame.grid ( row=0, column=1 )

        self.sub1 = Canvas ( self.rightFrame, width=50, height=50,
            bg='red' )
        self.sub2 = Canvas ( self.rightFrame, width=50, height=50,
            bg='green' )

        self.sub2.grid(padx=30, pady=50)
        self.sub2.grid_remove()
        self.sub1.grid(padx=5, pady=10)
        self.showing = self.sub1

        self.quitButton = Button ( self, text="Quit",
            font=self.buttonFont,
            command=self.quit )
        self.quitButton.grid(row=99, column=0, columnspan=99,
            sticky=E+W)

    def radioHandler(self):
        '''Handle radiobutton changes.
        '''
        value = self.which.get()
        if value==0:
            theFrame = self.sub1
        else:
            theFrame = self.sub2

        if self.showing is not theFrame:
            self.showing.grid_remove()
            theFrame.grid()
            self.showing = theFrame

app = Application()
app.master.title("Sample application")
app.mainloop()

