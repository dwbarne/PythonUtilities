#!/usr/local/bin/python
from Tkinter import *
import tkFont

class Application(Frame):
    def __init__(me):
        Frame.__init__(me, None)
        me.grid()
        me.bigFont = tkFont.Font ( 
		family="lucidatypewriter", 
		size=20,
		weight="bold" 
	)
	me.tk_focusFollowsMouse()
        me.createWidgets()

    def createWidgets(self):
        """
	Create all widgets.
        """

# SCALE slider widget
        self.scaleValue = DoubleVar()  # Control variable
# Constructor
        self.slider = Scale ( 
		self, 
		from_=0.0, 
		to=1.0,
		resolution=0.01, 
		tickinterval=0.1, 
		length=600,
		command=self.scaleHandler,
		variable=self.scaleValue,
		orient=HORIZONTAL 
	)
        self.slider.grid ( 
		row=0, 
		column=0
	)

# ENTRY window widget
        self.readoutValue = StringVar()
# constructor
        self.readout = Entry ( 
		self, 
		textvariable=self.readoutValue,
		font=self.bigFont 
	)
        self.readout.grid ( 
		row=0, 
		column=1 
	)
        self.readout.bind ( 
		"<KeyPress-Return>", 
		self.returnEvent 
	)

# READ button
        self.readButton = Button ( 
		self, 
		text="Read",
		font=self.bigFont,
		command=self.reader
	)
	self.readButton.grid ( 
		row=1, 
		column=0 
	)

# QUIT button
        self.quitButton = Button ( self, 
		text="Quit",
		font=self.bigFont, 
		fg="white", 
		bg="black",
		activeforeground="black", 
		activebackground="white",
		command=self.quit 
	)
	self.quitButton.grid(
		row=99, 
		column=0, 
		columnspan=99,
#		sticky=E+W
	)

# READ button handler
    def reader ( self ):
        """
	Handler for the 'Read' button.
        """
        print self.scaleValue.get(), self.readoutValue.get()

# RETURN key handler
    def returnEvent ( self, event ):
        """
	Handler for the Return key inside self.readout.
        """
        try:
            newValue = float(self.readoutValue.get())
            self.scaleValue.set(newValue)
        except ValueError, detail:
            print "\n================================"
            print "\nThat's not a float!\n\n", detail

# SCALE widget handler
    def scaleHandler ( self, value ):
        """
	Handle changes to the scale widget.
        """
        self.readoutValue.set(value)


#================================================================
# Main program
#----------------------------------------------------------------

app = Application()
app.master.title("Sample application - D. Barnette")
app.mainloop()
