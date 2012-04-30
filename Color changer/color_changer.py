from Tkinter import *

tk = Tk()

# Left frame to hold buttons
left = Frame(tk)
left.pack(side=LEFT, expand=True, fill=Y)

# Right frame to hold display
right = Frame(tk, height=200, width=200)
right.pack(expand=True, fill=BOTH)

# change the colour of the right-hand frame
def changeColour(c):
    def change():
        right.config(background=c)
    return change

# Buttons
colours = ['red', 'green', 'blue', 'yellow']
for c in colours:
    b = Button(left, text=c, command=changeColour(c))
    b.pack(side=TOP, expand=True)

tk.mainloop()