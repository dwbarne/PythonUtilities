#!/usr/local/bin/python
from Tkinter import *
import tkFont

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.buttonFont=tkFont.Font (family="Helvetica",
						size=14) # use neg for pixels
		self.createWidgets()

	def createWidgets(self):
		self.panicButton = Button ( self, text="PANIC!!",
			font=self.buttonFont, command=self.panicHandler )
		self.panicButton.grid(row=0, column=0)

		self.panicLabel = Label ( self,
			text="Press panic button when panicky.",
			font=self.buttonFont )
		self.panicLabel.grid ( row=1, column=1)

		self.quitButton = Button ( self, text="Quit",
			font=self.buttonFont, bg="black", fg="white",
			activebackground="cyan", activeforeground="magenta",
			command=self.quit )
		self.quitButton.grid (row=2, column=0, columnspan=99,
			sticky=E+W )

	def panicHandler(self):
		print "PANIC BUTTON PRESSED!! RUN!!!"
		print "" 

#- - - - - -  main  - - - - -
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.master.title("Panic Button Application")
    app.mainloop()
	
				
