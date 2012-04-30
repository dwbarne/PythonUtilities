# from "Python Standard Library," p. 21
#  Using the os Module to List the Files in a Directory

# File: os-example-5.py

# See also
# T:\Python - Projects\File list of current directory\file_list_os-example-5.py
# T:\Python - Projects\Files only - no directories\files_only_no_directories.py

import os
import Pmw
import Tkinter

#class Demo(Pmw.MegaWidget):
class Demo(Tkinter.Frame):
    def __init__(self,parent):
        parent.configure(background='white')
        Tkinter.Frame.__init__(self,parent)
 #       Pmw.MegaWidget.__init__(self,parent)
        
#   Create and pack widget to be configured.
#        self.target=Tkinter.Label(parent,
#            relief='ridge',
#            padx=20,
#            pady=20,
#            )
            
#        def getFileNames():
        self.filenames=[]
        for filename in os.listdir("."):
            print filename
            self.filenames.append(filename)
    
        print "filenames =",self.filenames
#            return filenames
    
#        self.filenames=getFileNames()
        print "external filenames = ",self.filenames

        self.dropdown=Pmw.ComboBox(parent,
            label_text="Dropdown box:",
            labelpos='wn',
#            selectioncommand=self.changeFile,
            scrolledlist_items=self.filenames,
#            dropdown=0
            )
        self.dropdown.grid(row=0,column=0)
#        self.dropdown.pack(side='left',fill='both',expand=1,padx=10,pady=10)
        entryInit=self.dropdown.selectitem(self.filenames[0])
        self.changeFile(entryInit)

    def changeFile(self,text):
        print " Text:", text
#        self.target.configure(text=text)
            

root=Pmw.initialise()
root.title('This is a Pmw Combobox')
            
app=Demo(root)
app.mainloop()
print "end"


    