#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: myScrollbar.py
# Author: dwbarne
# Creation date: Sat, 01-17-2009

# Purpose:
"""
check out the Tkinter scrollbar
"""


# >> INSERT: Global Imports <<
# ===== Global Imports =====
from Tkinter import *                    # Tkinter widgets
import tkFont                    # fonts


# ===== main class ===== # 
class Demo_Scrollbar(Frame):
    def __init__(self, parent):
        print '\n\n ***** Welcome **********'

        Frame.__init__(self)

        self.frameParent = parent

        self.frameParent.geometry(
            '+%d+%d' % (100, 100) 
            )


        self.createWidgets()



# >> INSERT: def createWidgets <<
    def createWidgets(self):

        myScrollBar = Scrollbar(
            self.frameParent,
            bg='tan',
            borderwidth=5,
            relief=RIDGE,
            )
        myScrollBar.grid(
            row=0,
            column=0,
             )

# ===== Handlers go below ===== #


# >> INSERT: If Name=Main <<
# ===== main ===== # 
if __name__ == '__main__':
    root = Tk()
    app = Demo_Scrollbar(root)
    app.master.title(
       'Main window'
        )
    app.master.configure(
        bg='lightblue',
        )
    app.mainloop()





