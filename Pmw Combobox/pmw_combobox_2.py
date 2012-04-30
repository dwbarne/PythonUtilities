import os
import Pmw
import Tkinter

class Demo(Pmw.MegaWidget):
    def __init__(self, parent):
        parent.configure(background = 'white')
        Pmw.MegaWidget.__init__(self,parent)

        # Create and pack the widget to be configured.
        self.target = Tkinter.Label(parent,
#                relief = 'sunken',
                relief = 'raised',
                padx = 20,
                pady = 20,
        )
        self.target.pack(fill = 'x', padx = 8, pady = 8)

        # Create and pack the simple ComboBox.
        words = ('Monti', 'Python', 'ik', 'den', 'Holie', 'Grailen', '(Bok)')
        simple = Pmw.ComboBox(parent,
                label_text = 'Simple ComboBox:',
                labelpos = 'nw',
                selectioncommand = self.changeText,
                scrolledlist_items = words,
#                dropdown = 0,
        )
        simple.pack(side = 'left', fill = 'both',
                expand = 1, padx = 8, pady = 8)

        # Display the first text.
        first = words[0]
        simple.selectitem(first)
        self.changeText(first)

        # Create and pack the dropdown ComboBox.
        colours = ('red','cornsilk1', 'snow1', 'seashell1', 'antiquewhite1',
                'bisque1', 'peachpuff1', 'navajowhite1', 'lemonchiffon1',
                'ivory1', 'honeydew1', 'lavenderblush1', 'mistyrose1')
        dropdown = Pmw.ComboBox(parent,
                label_text = 'Dropdown ComboBox:',
                labelpos = 'nw',
                selectioncommand = self.changeColour,
                scrolledlist_items = colours,
        )
        dropdown.pack(side = 'left', anchor = 'n',
                fill = 'x', expand = 1, padx = 8, pady = 8)

        # Display the first colour.
        first = colours[0]
        dropdown.selectitem(first)
        self.changeColour(first)

    def changeColour(self, colour):
        print 'Colour: ' + colour
        self.target.configure(background = colour)

    def changeText(self, text):
        print 'Text: ' + text
        self.target.configure(text = text)
        
# # # # # # # # # # # # # # #
root=Pmw.initialise()
root.title('This is a Pmw ComboBox!')

app=Demo(root)
#app.Title('This is Pmw Combobox!')  # won't work with this
app.mainloop() 