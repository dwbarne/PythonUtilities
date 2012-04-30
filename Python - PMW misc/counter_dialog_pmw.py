from Tkinter import *

import Pmw

root = Tk()

# root.withdraw() # not in original code; uncomment to
                  # suppress extra window, but killing PMW
                  # window will not terminate program

Pmw.initialise()

dialog = Pmw.Dialog(
        title = 'Counter dialog',
        buttons = ('OK', 'Cancel')
        )

interior = dialog.interior()
counter = Pmw.Counter(interior)
counter.pack(padx = 10, pady = 10)


root.mainloop()