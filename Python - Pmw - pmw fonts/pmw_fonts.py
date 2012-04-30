#Pmw copyright
# reference: http://www.java2s.com/Code/Python/GUI-Pmw/PmwLogicalFontdemonstration.htm

#Copyright 1997-1999 Telstra Corporation Limited, Australia 
#Copyright 2000-2002 Really Good Software Pty Ltd, Australia

#Permission is hereby granted, free of charge, to any person obtaining a copy 
#of this software and associated documentation files (the "Software"), to deal 
#in the Software without restriction, including without limitation the rights 
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
#copies of the Software, and to permit persons to whom the Software is furnished 
#to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all 
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
#PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
#HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
#OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

title = 'Pmw LogicalFont demonstration'

# Import Pmw from this directory tree.
import sys
sys.path[:0] = ['../../..']

import string
import Tkinter
import Pmw

class Demo:

    # The fonts to demonstrate.
    fontList = (
      (('Times', 0), {}),
      (('Helvetica', 0), {}),
      (('Typewriter', 0), {}),
      (('Fixed', 0), {}),
      (('Courier', 0), {}),
      (('Helvetica', 2), {'slant' : 'italic'}),
      (('Helvetica', 0), {'size' : 18}),
      (('Helvetica', 0), {'weight' : 'bold'}),
      (('Helvetica', 12), {'weight' : 'bold', 'slant' : 'italic'}),
      (('Typewriter', 0), {'size' : 8, 'weight' : 'bold'}),
      (('Fixed', 0), {'size' : 8, 'weight' : 'bold'}),
      (('Times', 0), {'size' : 24, 'weight' : 'bold', 'slant' : 'italic'}),
      (('Typewriter', 0), {'width' : 'condensed'}),
      (('Typewriter', -1), {'width' : 'condensed'}),
      (('Fixed', 0), {'width' : 'condensed'}),
      (('Fixed', -1), {'width' : 'condensed'}),
      (('Helvetica', 0), {'weight' : 'bogus'}),
    )

    fontText = []

    def __init__(self, parent):

        self.parent = parent

  # Create the text to display to the user to represent each font.
        if Demo.fontText == []:
            for args, dict in Demo.fontList:
                text = args[0]
                if args[1] != 0:
                    text = text + ' ' + str(args[1])
                for name, value in dict.items():
                    text = text + ' ' + name + ': ' + str(value)
                Demo.fontText.append(text)

  # Create a listbox to contain the font selections.
        self.box = Pmw.ScrolledListBox(parent, listbox_selectmode='single', 
            listbox_width = 35,
            listbox_height = 10,
            items=Demo.fontText,
            label_text='Font', labelpos='nw', 
            selectioncommand=self.selectionCommand)
        self.box.pack(fill = 'both', expand = 1, padx = 10, pady = 10)

  # Create a label to display the selected font.
        self.target = Tkinter.Label(parent,
            text = 'The quick brown fox jumps\nover the lazy dog',
            relief = 'sunken', padx = 10, pady = 10)
        self.target.pack(fill = 'both', expand = 1, padx = 10, pady = 10)

    def selectionCommand(self):
        sel = self.box.curselection()
        if len(sel) > 0:
            args, dict = Demo.fontList[string.atoi(sel[0])]
            font = apply(Pmw.logicalfont, args, dict)
            self.target.configure(font = font)
            print font
######################################################################

# Create demo in root window for testing.
if __name__ == '__main__':
    root = Tkinter.Tk()
    Pmw.initialise(root)
    root.title(title)

    exitButton = Tkinter.Button(root, text = 'Exit', command = root.destroy)
    exitButton.pack(side = 'bottom')
    widget = Demo(root)
    root.mainloop()
