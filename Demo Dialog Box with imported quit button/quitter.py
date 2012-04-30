############################################
# a quit button that verifies exit requests;
# to reuse, attach an instance to other guis
############################################

from Tkinter import *			# get widget classes
from tkMessageBox import askokcancel	# get canned std dialog

class Quitter(Frame):
	def __init__(self, master=None, parent=None):
		Frame.__init__(self, parent)
		self.pack()

		widget=Button(self, text='Quit',command=self.quit)
		widget.pack(side=LEFT)

		widget2=Button(self, text='quit',command=self.quit)
		widget2.pack(side=RIGHT)

	def quit(self):
		ans=askokcancel('Verify exit', "Really quit?")
		if ans: Frame.quit(self)

if __name__=='__main__': Quitter().mainloop()

