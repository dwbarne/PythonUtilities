from Tkinter import *
import tkFont

class Application(Frame) :
	def __init__(self):
		Frame.__init__(self, None)
		self.grid()
		self.bigFont = tkFont.Font ( 
			family="lucidatypewriter", 
			size=20,
			weight="bold" 
		)
		self.tk_focusFollowsMouse()
		self.createWidgets()

	print "\nThis is step 1 \n"

	def createWidgets(self):
		self.canv=Canvas(self, width=220, height=120)
		self.canv.pack()

		self.canv.bind (
			"<Button-1>",
			self.__drawOrangeBlob
		)


	def __drawOrangeBlob (self, event):
		""" Draws an orange blob in self.canv where the mouse is.
		"""
		r=10		#Blob radius
		print " >> Radius = ",r
	
		self.canv.create_oval (
			event.x-r, 
			event.y-r,
			event.x+r,
			event.y+r,
			fill="orange"
		)
		print "character = ", event.char, " \n"
		print " x = ",(event.x+r + event.x-r)/2., ", y = ",(event.y+r + event.y-r)/2., " \n"
	

	
#	================= main ================================
app=Application()
app.mainloop()