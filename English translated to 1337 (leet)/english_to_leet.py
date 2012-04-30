"""
Reference:
http://blenderartists.org/forum/archive/index.php/t-101270.html
Ever wanted to speak 1337 but not been #4><0R enough?
Now you can, thanks to the Eng-1337 Translator:D
http://uploader.polorix.net//files/123/Version%202%20interface.jpg

Something I wrote this morning in Python - you'll need to have Python installed to run it. It also uses the TKinter module but that normally comes as part of the installation:yes:
Enter the English text you want to translate into the top text field, click translate and the 1337 - 5|*34|< translation will appear at the bottom.
"""

# Eng-1337 translator version 2.0

# Importing the Tkinter module
import Tkinter

#Don't doss with the DOS!
print "WARNING: Closing this window will terminate the application"

#Creating the eng_leet class
class eng_1337(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

# Initializing the GUI
    def initialize(self):
        self.grid()
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
        self.grid_rowconfigure(6, weight = 1)
        self.grid_rowconfigure(7, weight = 1)
        self.grid_rowconfigure(8, weight = 1)

# "English:" label
        self.eng_label = Tkinter.Label(self, text = "English:", anchor = "w",
        fg = "green", bg = "black")
        self.eng_label.grid(column = 0, row = 0, columnspan = 5, sticky = "EW")

# English text field
        self.engtextfield = Tkinter.Text(self, bd = 5, wrap = "word")
        self.engtextfield.grid(column = 0, row = 1, columnspan = 4, rowspan = 3,sticky = "NEWS")

# The first scrollbar
        self.scrollbar1 = Tkinter.Scrollbar(self)
        self.scrollbar1.grid(column = 4, row = 1, rowspan = 3, sticky = "NS")

# Making the first scrollbar control the english text field
        self.scrollbar1.config(command = self.engtextfield.yview)
        self.engtextfield.config(yscrollcommand = self.scrollbar1.set)

# The middle padding
        self.midpad = Tkinter.Label(self, text = " ", anchor = "n", bg = "black")
        self.midpad.grid(column = 0, row = 4, columnspan = 5, sticky = "NEWS")

# The "1337:" label
        self.leet_label = Tkinter.Label(self, text = "1337:", anchor = "w", fg = "green", bg = "black")
        self.leet_label.grid(column = 0, row = 5, columnspan = 5, sticky = "EW")

# The 1337 text field
        self.leettextfield = Tkinter.Text(self, bd = 5, wrap = "word", state = "disabled")
        self.leettextfield.grid(column = 0, row = 6, columnspan = 4, rowspan = 3, sticky = "NEWS")

# The second scrollbar
        self.scrollbar2 = Tkinter.Scrollbar(self)
        self.scrollbar2.grid(column = 4, row = 6, rowspan = 3, sticky = "NS")

# Making the second scrollbar control the 1337 text field
        self.scrollbar2.config(command = self.leettextfield.yview)
        self.leettextfield.config(yscrollcommand = self.scrollbar2.set)

# The bottom-left padding
        self.blpad = Tkinter.Label(self, text = " ", anchor = "n", bg = "black")
        self.blpad.grid(column = 0, row = 9, columnspan = 3, sticky = "EW")

# The "Translate" button
        self.transbutton = Tkinter.Button(self, text = "Translate", fg = "black", bg = "green", relief = "raised", command = self.translate)
        self.transbutton.grid(column = 3, row = 9, sticky = "EW")

# The bottom-right padding
        self.brpad = Tkinter.Label(self, text = " ", anchor = "n", bg = "black")
        self.brpad.grid(column = 4, row = 9, sticky = "NEWS")

# Translating
    def translate(self):
        print
        print "Translating text..."
        self.leettextfield.config(state = "normal")
        self.leettextfield.delete(1.0, "end")
        self.leettextfield.config(state = "disabled")
        string = self.engtextfield.get(1.0, "end")
        string = string.replace("A", "4")
        string = string.replace("a", "@")
        string = string.replace("B", "8")
        string = string.replace("b", "b")
        string = string.replace("C", "[")
        string = string.replace("c", "<")
        string = string.replace("D", "|>")
        string = string.replace("d", "c|")
        string = string.replace("E", "3")
        string = string.replace("e", "3")
        string = string.replace("F", "|=")
        string = string.replace("f", "(=")
        string = string.replace("G", "6")
        string = string.replace("g", "6")
        string = string.replace("H", "#")
        string = string.replace("h", "#")
        string = string.replace("I", "|")
        string = string.replace("i", "!")
        string = string.replace("J", "_|")
        string = string.replace("j", "_)")
        string = string.replace("K", "|<")
        string = string.replace("k", "I<")
        string = string.replace("L", "|_")
        string = string.replace("l", "1")
        string = string.replace("M", "|\/|")
        string = string.replace("m", "|\/|")
        string = string.replace("N", "|\|")
        string = string.replace("n", "|\|")
        string = string.replace("O", "0")
        string = string.replace("o", "0")
        string = string.replace("P", "|*")
        string = string.replace("p", "|*")
        string = string.replace("Q", "O,")
        string = string.replace("q", "9")
        string = string.replace("R", "|2")
        string = string.replace("r", "|^")
        string = string.replace("S", "$")
        string = string.replace("s", "5")
        string = string.replace("T", "7")
        string = string.replace("t", "-|-")
        string = string.replace("U", "|_|")
        string = string.replace("u", "(_)")
        string = string.replace("V", "\/")
        string = string.replace("v", "\/")
        string = string.replace("W", "\/\/")
        string = string.replace("w", "uu")
        string = string.replace("X", "><")
        string = string.replace("x", "}{")
        string = string.replace("Y", "'|'")
        string = string.replace("y", "`/")
        string = string.replace("Z", "ZZ")
        string = string.replace("z", "2")
        self.leettextfield.config(state = "normal")
        self.leettextfield.insert("end", string)
        self.leettextfield.config(state = "disabled")
        print
        print "Translation complete."
        print

# Main
if __name__ == "__main__":
    app = eng_1337(None)
    app.title("Eng-1337 Translator version 2.0")
    app.maxsize(width = 600, height = 500)
    app.mainloop()
#NOTE: At the moment it does not translate back from 1337, I'll probably add this in for the next release;)