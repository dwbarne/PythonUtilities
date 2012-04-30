#!/usr/bin/env python
#================================================================
# entries: Complex entry field layout
#
#    0              1
#   +--------------+------------+
#  0| Label                     |
#   +--------------+------------+
#  1| '# nodes'    | nodesField |
#   +--------------+------------+
#  2| '# procs'    | procsField |
#   +--------------+------------+
#  3| 'cores/proc' | coresField |
#   +--------------+------------+---+---------+
#  4|                      | 'HH'       |    | 'MM'    |
#   +--------------+------------+---+---------+
#  5| 'max runtime'| hhField    | : | mmField |
#   +--------------+------------+---+---------+
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
        self.topLabel = Label ( self, text='QSUB command',
            font=self.buttonFont )
        self.topLabel.grid ( row=0, column=0, columnspan=99,
          sticky=E+W )

        self.nodesLabel = Label ( self, text='# nodes' )
        self.nodesLabel.grid ( row=1, column=0, sticky=E )

        self.nodesValue = StringVar()
        self.nodesValue.set('1')

        self.nodesField = Entry ( self, width=5, 
            textvariable=self.nodesValue )
        self.nodesField.grid ( row=1, column=1, columnspan=3,
            sticky=W )
        self.nodesField.bind ( '<Any-KeyRelease>', self.__nodesHandler )

        self.procsValue = StringVar()
        self.procsValue.set ( '1' )

        self.procsLabel = Label ( self, text='# processors' )
        self.procsLabel.grid ( row=2, column=0, sticky=E )

        self.procsField = Entry ( self, width=3,
            textvariable=self.procsValue )
        self.procsField.grid ( row=2, column=1, columnspan=3, sticky=W )
        self.procsField.bind ( '<Any-KeyRelease>', self.__procsHandler )

        self.hhLabel = Label ( self, text='HH' )
        self.hhLabel.grid ( row=4, column=1, sticky=W )
        self.mmLabel = Label ( self, text='MM' )
        self.mmLabel.grid ( row=4, column=3 )
        self.maxLabel = Label ( self, text='max runtime' )
        self.maxLabel.grid ( row=5, column=0, sticky=E )
        self.hhField  =  Entry ( self, width=2 )
        self.hhField.grid ( row=5, column=1, sticky=W )
        self.colonLabel  =  Label ( self, text=':' )
        self.colonLabel.grid ( row=5, column=2 )
        self.mmField  =  Entry ( self, width=2 )
        self.mmField.grid ( row=5, column=3 )

        self.quitButton = Button ( self, text="Quit",
            font=self.buttonFont,
            command=self.quit )
        self.quitButton.grid(row=99, column=0, columnspan=99, sticky=E+W)

    def __nodesHandler ( self, event ):
        value = self.nodesValue.get()
        try:
            intValue = int(value)
        except ValueError, details:
            print "*** Nodes: '%s' is not an integer!" % value
        else:
            print "We love this nodes value %d!" % intValue

    def __procsHandler ( self, event ):
        value = self.procsValue.get()
        print "@@@ __procsHandler: value is", value
        try:
            intValue = int(value)
        except ValueError, details:
            print "*** Procs: '%s' is not an integer!" % value
            return

        if not ( 1 <= intValue <= 8 ):
            print "*** Procs: must be between 1 and 8"
            return

        print "We love this procs value %d!" % intValue

app = Application()
app.master.title("Sample application")
app.mainloop()

