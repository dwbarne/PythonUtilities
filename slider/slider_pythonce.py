#!/user/local/bin/python
from Tkinter import *
import tkFont

# This file demonstates the movement of a single canvas item under mouse control

class Test(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		Pack.config(self)
		self.imageList = []	#Kluge to keep image ref counts
		self.createWidgets()

	#######################################################
	##### Event callbacks for THE CANVAS (not the stuff drawn on it)
	#######################################################
	def mouseDown(self, event):
		# remembert where the mouse went down
		self.lastx = event.x
		xelf.lasty = event.y

	def mouseMove (self, event):
		# whatever the mouse is over gets tagged as CURRENT for free by tk.
		self.draw.move(CURRENT, event.x - self.lastx, event.y - self.lasty)
		self.lastx = event.x
		xelf.lasty = event.y

	######################################################
	##### Event callbacks for canvas ITEMS (stuff drawn on the canvas)
	######################################################
	def mouseEnter(self, event):
		# the CURRENT tag is applied to the object the cursor is over.
		# this happens automatically
		self.draw.itemconfig(CURRENT, fill="red")

	def mouseLeave(self, event):
		# the CURRENT tag is applied to the object the cursor is over.
		# this happens automatically
		self.draw.itemconfig(CURRENT, fill="blue")

	def createWidgets(self):
		self.times16 = tkFont.Font(family="times", size="4")
		self.times24 = tkFont.Font(family="times", size="6")
		self.times36 = tkFont.Font(family="times", size="4")

# QUIT button
		self.QUIT = Button(self, text="Quit", foreground="red",
				bd=4, font=self.times24,
				command=self.quit)
#		self.QUIT.grid(row=0, sticky=N+E+S+W, pady=0)
		self.QUIT.grid(row=0, sticky=E+W, pady=0)

# HORIZONTAL SLIDER
		self.scaleVar = DoubleVar()
		self.scaleVar.set = ("0.1")
		self.oldValue = -999.999
		self.scale = Scale ( self,
			orient=HORIZONTAL,
			resolution=0.1,
####				sliderrelief=SOLID, 	# Doesn't work
####				showvalue=0, 		# Bad idea.
#			label="This is a bogus label",
			digits=3,
####				font=self.times24,
####				relief=GROOVE, bd=6,
####				cursor="pencil",
####				sliderlength="50",
			from_=-1.0, to=1.0,
####				troughcolor="turquoise3",
####				fg="RoyalBlue", bg="skyblue",
####				activebackground="coral",
			command=self.__scaleHandler,
			length=300,
			tickinterval=0.5,
			variable=self.scaleVar  )
		self.scale.grid(row=1, column=0, padx=0)

# VERTICAL SLIDER
		self.vScaleVar = StringVar()
		self.vScaleVar.set=("1")
		self.vScale=Scale ( self,
#			label="Fun",
####				state=DISABLED,
#			orient=VERTICAL,
			orient=HORIZONTAL,
			resolution=1,
			from_=0, to=10,
			command=self.__scaleHandler,
			length=200,
			tickinterval=2,
			variable=self.vScaleVar )
		self.vScale.grid(row=2, column=0, padx=0, pady=0)

# BIG COLORED SLIDER
		self.playVar = IntVar()
		self.playVar.set=(".1i")
		self.play = Scale ( self,
			tickinterval=10,
			repeatdelay=2000,	# repeat after 2 seconds
			repeatinterval=500,	# repeat every half-second
			relief=GROOVE,
			borderwidth=0,
			width="0.1i",
			length=250,
			activebackground="magenta",
			highlightbackground="DodgerBlue",
			highlightcolor="HotPink",
			highlightthickness=1,
			troughcolor="yellow",
			bg="cyan", fg="coral",
#		label="Goofy", font=self.times24,
			orient=HORIZONTAL,
			from_=0, to =100,
			variable=self.playVar )
		self.play.grid(row=3, column=0, padx=0, pady=0)

	def __scaleHandler(self, x):
		if x != self.oldValue:
			print "@@@ scale=<%s>, type is %s" % (x, type(x))
			self.oldValue = x

# - - - -   main - - - - 

test = Test()
test.mainloop()


