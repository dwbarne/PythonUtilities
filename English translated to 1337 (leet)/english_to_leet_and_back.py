"""
Version 3.0!
http://uploader.polorix.net//files/123/Version%203%20interface.jpg

The text is a demonstration of the 1337 - English translator, which I've improved a bit. I also worked out how to stop symbols like "|\/|" being split up - I've now got the longer ones at the top and the shorter symbols at the bottom:D
"""

# Eng-1337 translator version 3.0

# Importing the Tkinter module
import Tkinter

#Don't doss with the DOS!
print "WARNING: Closing this window will terminate the application"
print

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
        self.grid_columnconfigure(2, weight = 2)
        self.grid_columnconfigure(3, weight = 2)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
        self.grid_rowconfigure(6, weight = 1)
        self.grid_rowconfigure(7, weight = 1)
        self.grid_rowconfigure(8, weight = 1)

# "English:" label
        self.eng_label = Tkinter.Label(self, text = "English:", anchor = "w", fg = "green", bg = "black")
        self.eng_label.grid(column = 0, row = 0, columnspan = 5, sticky = "EW")

# English text field
        self.engtextfield = Tkinter.Text(self, bd = 5, wrap = "word")
        self.engtextfield.grid(column = 0, row = 1, columnspan = 4, rowspan = 3, sticky = "NEWS")

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
        self.leettextfield = Tkinter.Text(self, bd = 5, wrap = "word")
        self.leettextfield.grid(column = 0, row = 6, columnspan = 4, rowspan = 3, sticky = "NEWS")

# The second scrollbar
        self.scrollbar2 = Tkinter.Scrollbar(self)
        self.scrollbar2.grid(column = 4, row = 6, rowspan = 3, sticky = "NS")

# Making the second scrollbar control the 1337 text field
        self.scrollbar2.config(command = self.leettextfield.yview)
        self.leettextfield.config(yscrollcommand = self.scrollbar2.set)

# The "Translate:" label
        self.blpad = Tkinter.Label(self, text = "Translate text:", anchor = "n", fg = "green", bg = "black")
        self.blpad.grid(column = 0, row = 9, columnspan = 2, sticky = "NEWS")

# The "English - 1337" button
        self.transbutton1 = Tkinter.Button(self, text = "English - 1337", fg = "black", bg = "green", relief = "raised", command = self.engleet)
        self.transbutton1.grid(column = 2, row = 9, sticky = "EW")

# The "1337 - English" button
        self.transbutton2 = Tkinter.Button(self, text = "1337 - English", fg = "black", bg = "green", relief = "raised", command = self.leeteng)
        self.transbutton2.grid(column = 3, row = 9, sticky = "EW")

# The bottom-right padding
        self.brpad = Tkinter.Label(self, text = " ", anchor = "n", bg = "black")
        self.brpad.grid(column = 4, row = 9, sticky = "NEWS")

# The copyright notice
        self.copyright = Tkinter.Label(self, text = "Copyright David Barker 2007", anchor = "e", fg = "green", bg = "black")
        self.copyright.grid(column = 0, row = 10, columnspan = 5, sticky = "EW")

# Translating English - 1337
    def engleet(self):
        print
        print "Translating English text..."
        self.leettextfield.delete(1.0, "end")
        string = self.engtextfield.get(1.0, "end")
        string = string.replace("A", "4 ")
        string = string.replace("a", "@ ")
        string = string.replace("B", "8 ")
        string = string.replace("b", "b ")
        string = string.replace("C", "[ ")
        string = string.replace("c", "[ ")
        string = string.replace("D", "|> ")
        string = string.replace("d", "c| ")
        string = string.replace("E", "3 ")
        string = string.replace("e", "3 ")
        string = string.replace("F", "|= ")
        string = string.replace("f", "(= ")
        string = string.replace("G", "6 ")
        string = string.replace("g", "9 ")
        string = string.replace("H", "# ")
        string = string.replace("h", "# ")
        string = string.replace("I", "| ")
        string = string.replace("i", "! ")
        string = string.replace("J", "_| ")
        string = string.replace("j", "_) ")
        string = string.replace("K", "|< ")
        string = string.replace("k", "I< ")
        string = string.replace("L", "|_ ")
        string = string.replace("l", "1 ")
        string = string.replace("M", "|\/| ")
        string = string.replace("m", "|\/| ")
        string = string.replace("N", "|\| ")
        string = string.replace("n", "|\| ")
        string = string.replace("O", "0 ")
        string = string.replace("o", "0 ")
        string = string.replace("P", "|* ")
        string = string.replace("p", "|* ")
        string = string.replace("Q", "O, ")
        string = string.replace("q", "O, ")
        string = string.replace("R", "|^ ")
        string = string.replace("r", "|^ ")
        string = string.replace("S", "$ ")
        string = string.replace("s", "5 ")
        string = string.replace("T", "7 ")
        string = string.replace("t", "-|- ")
        string = string.replace("U", "|_| ")
        string = string.replace("u", "(_) ")
        string = string.replace("V", "\/ ")
        string = string.replace("v", "\/ ")
        string = string.replace("W", "\/\/ ")
        string = string.replace("w", "uu ")
        string = string.replace("X", ">< ")
        string = string.replace("x", "}{ ")
        string = string.replace("Y", "'|' ")
        string = string.replace("y", "`/ ")
        string = string.replace("Z", "ZZ ")
        string = string.replace("z", "2 ")
        self.leettextfield.insert("end", string)
        print
        print "Translation complete."
        print
        
# Translating 1337 - Engligh
    def leeteng(self):
        print
        print "Translating 1337 text..."
        self.engtextfield.delete(1.0, "end")
        string = self.leettextfield.get(1.0, "end")
        string = string.replace("|2", "R")
        string = string.replace("|_|", "U")
        string = string.replace("(_)", "u")
        string = string.replace("|-|", "H")
        string = string.replace("|\/|", "M")
        string = string.replace("|\|", "N")
        string = string.replace("-|-", "t")
        string = string.replace("|_", "L")
        string = string.replace("4", "A")
        string = string.replace("@", "a")
        string = string.replace("8", "B")
        string = string.replace("b", "b")
        string = string.replace("[", "C")
        string = string.replace("|>", "D")
        string = string.replace("l>", "D")
        string = string.replace("c|", "d")
        string = string.replace("3", "E")
        string = string.replace("3", "e")
        string = string.replace("|=", "F")
        string = string.replace("(=", "f")
        string = string.replace("6", "G")
        string = string.replace("9", "g")
        string = string.replace("#", "H")
        string = string.replace("!", "i")
        string = string.replace("_|", "J")
        string = string.replace("_)", "j")
        string = string.replace("|<", "K")
        string = string.replace("I<", "k")
        string = string.replace("1", "l")
        string = string.replace("0", "O")
        string = string.replace("|*", "P")
        string = string.replace("O,", "Q,")
        string = string.replace("|^", "r")
        string = string.replace("$", "S")
        string = string.replace("5", "s")
        string = string.replace("7", "T")
        string = string.replace("\/", "V")
        string = string.replace("VV", "W")
        string = string.replace("uu", "w")
        string = string.replace("><", "X")
        string = string.replace("}{", "x")
        string = string.replace("'|'", "Y")
        string = string.replace("`/", "y")
        string = string.replace("ZZ", "Z")
        string = string.replace("2", "z")
        string = string.replace("<", "C")
        string = string.replace("(", "C")
        string = string.replace("+", "T")
        string = string.replace("|", "I")
        string = string.lower()
        string = string.capitalize()
        self.engtextfield.insert("end", string)
        print
        print "Translation complete."
        print

# Main
if __name__ == "__main__":
    app = eng_1337(None)
    app.title("Eng - 1337 Translator version 3.0")
    app.maxsize(width = 600, height = 500)
    app.mainloop()

# End of program
# Eng-1337 Translator is copyright David Barker 2007Also, I've added several more symbols to it (and tested it with some random garbled nonsense I found on Google), and it gets it right about 90% of the time - which is as much as I can be bothered trying to get at the moment;)
'''
I redid the bottom part of the UI as well, because it looked a bit rubbish before, and also so I could stick a copyright notice in (although seeing as it's .py you could probably remove it in seconds;)).
'''