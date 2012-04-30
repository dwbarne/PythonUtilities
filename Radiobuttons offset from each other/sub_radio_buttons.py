#!/usr/bin/env python
#================================================================

from Tkinter import *
import tkFont

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont = tkFont.Font ( 
            family="Helvetica",
            size="10" 
            )
        self.createWidgets()

    def createWidgets(self):

        self.topRadio = StringVar()
        self.topRadio.set('qsub')
        self.radio1 = Radiobutton ( self, 
            text='Just run',
            command=self.__topHandler,
            variable=self.topRadio, 
            value='just',
#            activebackground='red',
#            activeforeground='white',
            borderwidth=5,
            justify=LEFT,
            height=2,
            selectcolor='green',
#            highlightbackground='red',
#            highlightcolor='blue'
            )
        self.radio1.grid ( 
            row=0, 
            column=0, 
            sticky=W 
            )

        self.radio2 = Radiobutton ( self, 
            text='Qsub',
            command=self.__topHandler,
            variable=self.topRadio, 
            value='qsub',
            selectcolor='green'
            )
        self.radio2.grid ( 
            row=1, 
            column=0, 
            sticky=W 
            )

        self.subRadioFrame = Frame ( self )
        self.subRadioFrame.grid ( 
            row=2, 
            column=0, 
            sticky=W 
            )

        self.radio3 = Radiobutton ( self, 
            text='MS-DOS',
            command=self.__topHandler,
            variable=self.topRadio, 
            value='msdos' 
            )
        self.radio3.grid ( 
            row=3, 
            column=0, 
            sticky=W 
            )

        self.subRadio = StringVar()
        self.subRadio.set('q1')
        self.sub1 = Radiobutton ( self.subRadioFrame,
            variable=self.subRadio,
            text='Q1', 
            value='q1' 
            )
        self.sub1.grid ( 
            row=0, 
            column=0, 
            padx=20, 
            sticky=W 
            )

        self.sub2 = Radiobutton ( self.subRadioFrame,
            variable=self.subRadio,
            text='Q2', 
            value='q2' 
            )
        self.sub2.grid ( 
            row=1, 
            column=0, 
            padx=20, 
            sticky=W 
            )

        self.readButton = Button ( self, 
            text='Read',
            command=self.__readHandler 
            )
        self.readButton.grid ( 
            row=4, 
            column=0, 
            sticky=E+W 
            )

        self.quitButton = Button ( self, 
            text="Quit",
            font=self.buttonFont,
            command=self.quit 
            )
        self.quitButton.grid()

    def __readHandler ( self ):
        print ( "Outer=%s Inner=%s" %
              (self.topRadio.get(), self.subRadio.get()) 
              )

    def __topHandler ( self ):
        '''If self.topRadio is 'Qsub', then enable 2nd level,
           otherwise disable it.
        '''
        state = self.topRadio.get()
        if state=='qsub':
            self.sub1['state'] = NORMAL
            self.sub2['state'] = NORMAL
        else:
            self.sub1['state'] = self.sub2['state'] = DISABLED
#            self.sub2['state'] = DISABLED


app = Application()
app.master.title("Sample application")
app.mainloop()

