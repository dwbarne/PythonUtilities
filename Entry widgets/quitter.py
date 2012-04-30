############################################
# a quit button that verifies exit requests;
# to reuse, attach an instance to other guis

# Reference:
# "Programming Python - 2nd Edition" by Mark Lutz, p. 305
############################################

from Tkinter import *			# get widget classes
from tkMessageBox import askokcancel	# get canned std dialog

class Quitter(Frame):
	def __init__(self, master=None, parent=None):
		Frame.__init__(self, parent)
		self.pack()

		widget=Button(self, text='Quit',command=self.quit)
		widget.pack(side=LEFT)

	def quit(self):
		ans=askokcancel('Verify exit', "Really quit?")
		if ans: Frame.quit(self)

if __name__=='__main__': Quitter().mainloop()

