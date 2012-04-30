#!/usr/bin/env python
#================================================================
# mybutton:  Demonstrate how to subclass Tkinter widgets for style.
#   This application has a class named 'MyButton' that works just
#   like Button, except a MyButton will have brown text, a yellow
#   background, and 32-point bold Helvetica font.
#================================================================

from Tkinter import *
import tkFont
import copy

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont = tkFont.Font ( family="Helvetica",
            size="40" )
        self.createWidgets()

    def createWidgets(self):
        '''There are four widges in a vertical row: three
           of the 'MyButton' style, and an exit button.
        '''

        self.button1 = MyButton ( self, text='One' )
        self.button1.grid(row=0)

        self.button2 = MyButton ( self, text='Two ridiculous' )
        self.button2.grid(row=1)

        #--
        # This button demonstrates how you can override the
        # default attributes of a MyButton by simply passing in
        # new attributes: this button will use a 12-point Times
        # font instead of the 32-point Helvetica of MyButton.
        #--
        self.button3 = MyButton ( self, text='Three',
            font=('times', 12, 'italic') )
        self.button3.grid(row=2)

        self.quitButton = Button ( self, text="Quit",
            font=self.buttonFont,
            command=self.quit )
        self.quitButton.grid(row=99, column=0, columnspan=100,
            stick=E+W)

#--
# Class MyButton inherits from Button, so it is a Button for all
# intents and purposes.
#
# However, the class variable myOptions contains entries for
# the attributes that we want to have for all our buttons.
#--

class MyButton(Button):

    myOptions = {
        'font': ('Helvetica', 32, 'bold'),
        'fg': 'brown', 'bg': 'yellow' }

    def __init__(self, *p, **k):
        '''Constructor for MyButton.

          All positional arguments are bound to 'p' as a tuple.
          All keyword arguments are bound to 'k' as a dictionary.
        '''

        #--
        # Make a copy of self.myOptions
        #--
        opts = copy.copy(self.myOptions)

        #--
        # Merge in all the keyword arguments that were passed
        # to this constructor.  Note that if there is an attribute
        # that exists in both self.myOptions and 'k', the one in
        # 'k' (passed in) will win.
        #--
        opts.update(k)

        #--
        # Call the parent constructor with the new set of 
        # keyword arguments.
        #--
        Button.__init__(self, *p, **opts)

app = Application()
app.master.title("Sample application")
app.mainloop()

