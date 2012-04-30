from Tkinter import *
from tkMessageBox import *   # askyesno function comes from here

def callback():
	if askyesno('Verify', 'Do you really want to quit?'):
		showwarning('Yes', 'Quit not yet implemented')
	else:
		showinfo('Nope', 'Quit has been cancelled')

errmsg = 'Sorry, no Spam allowed!'
Button(text='Quit', command=callback).pack(fill=X)
Button(text='Spam', command=(lambda: showerror('SpamDWB', errmsg))).pack(fill=X)
mainloop()

