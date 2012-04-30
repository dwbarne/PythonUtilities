#!/usr/bin/env python
#================================================================

from Tkinter import *
import tkFont
import Pmw

grayed = '#aaaaaa'

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont = tkFont.Font ( family="Helvetica",
            size="40" )
        self.createWidgets()

    def createWidgets(self):
        self.disVar = IntVar()
        self.dis = Checkbutton ( self, text='Disable',
            variable=self.disVar,            
            command=self.__disHandler)
        self.dis.grid(row=0, sticky=W)

        self.box = Pmw.RadioSelect ( self, labelpos=W,
            command=self.boxHandler,
            label_text='This Is Your Label',
            label_font=('Helvetica', 20),
            hull_borderwidth=2,
            hull_relief=RIDGE,
            )                                     
        self.box.grid(row=1, sticky=W)

        self.go = Button ( self, text='Go' )
        self.go.grid(row=2, sticky=W)

        self.quitButton = Button ( self, text="Quit",
            font=self.buttonFont,
            command=self.quit )
        self.quitButton.grid()

    def __disHandler(self):
        '''Changed of state of the 'disabled' checkbox
        '''
        if self.disVar.get():
            self.box['label_fg'] = grayed
####            self.go['state'] = DISABLED
            self.go.configure(state=DISABLED)
        else:
            self.box['label_fg'] = 'black'
            self.go['state'] = NORMAL

    def boxHandler(self):
        print "boxHandler!"

app = Application()
app.master.title("Sample application")
app.mainloop()

