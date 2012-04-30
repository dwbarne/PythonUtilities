#!/usr/bin/env python
#================================================================

import sys
from Tkinter import *
import tkFont
from tkFileDialog import *

class Application(Frame):
    """Application to demonstrate reading into and writing from
        a text widget to a file.

    The user can edit the text in the text widget using ordinary
    keystrokes such as delete and arrow keys.

    Grid plan:
     0            1                2             3              4
    +------------+----------------+-------------+--------------+-------------+
  0 | .fileLabel | .fileNameEntry | .readButton | .writeButton | .quitButton |
    +------------+----------------+-------------+--------------+-------------+
  1 | .text                                                                  |
    +------------------------------------------------------------------------+
    """

    TEXT_WIDE  =  80
    TEXT_HIGH  =  8

    def __init__(self, master=None):
        """Constructor for the Application instance."""
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont = tkFont.Font ( family="Helvetica",
            size="40" )
        self.entryFont = tkFont.Font ( family="lucidatypewriter",
            size="18" )
        self.createWidgets()

    def createWidgets(self):
        rowx = colx = 0

        #--
        # Create a label for the file name entry widget.
        #--
        self.fileLabel = Label ( self, text="File:",
                                 font=self.buttonFont )
        self.fileLabel.grid ( row=rowx, column=colx )
        colx  +=  1

        #--
        # Create the text entry for the file name.
        #--
        self.fileNameVar = StringVar()
        self.fileNameEntry = Entry ( self,
            width=25, textvariable=self.fileNameVar,
            font=self.entryFont )
        self.fileNameEntry.grid ( row=rowx, column=colx )
        self.fileNameVar.set('<enter here>')
        colx  +=  1
        

        #--
        # Read and write buttons
        #--
        self.readButton  =  Button ( self, text="Read",
            font=self.buttonFont,
            command=self.readHandler )
        self.readButton.grid ( row=rowx, column=colx )
        colx  +=  1

        self.writeButton  =  Button ( self, text="Write",
            font=self.buttonFont, command=self.writeHandler )
        self.writeButton.grid ( row=rowx, column=colx )
        colx  +=  1

        self.quitButton = Button ( self, text="Quit",
            font=self.buttonFont,
            command=self.quit )
        self.quitButton.grid(row=rowx, column=colx)
        rowx  +=  1
        colx  =   0

        # get file button
        b1=Button(self,text="Find", command=self.getFile)
        b1.grid(row=1,column=0)

        #--
        # Row 2 contains the text widget.
        #--
        rowx+=1
        
        self.text  =  Text ( self, 
            width=self.TEXT_WIDE, height=self.TEXT_HIGH,            
            font=self.entryFont )
        self.text.grid ( row=rowx, column=colx, columnspan=99,
            sticky=E+W )
            
    def getFile(self):
        filenm=askopenfilename()
#        print " filenm = ",self.filenm
        self.fileNameVar.set(filenm)

    def readHandler ( self ):
        """Handler for the read button.

            Gets the file name from self.fileNameEntry and
            tries to open that file with read access.  If
            successful, it appends the contents of that file
            to self.text.
        """
        #--
        # Get the file name and try to open it.
        #--
        fileName  =  self.fileNameVar.get()
        print "*** Reading file '%s'" % fileName
        try:
            inFile  =  open ( fileName )
        except IOError, detail:
            print "*** Couldn't open '%s': %s" % (fileName, detail)
            sys.exit()

        #--
        # Get the contents of the file.
        #--
        contents  =  inFile.read()
        inFile.close()

        #--
        # Append the contents to self.text.  Position END (from
        # Tkinter) is after the end.
        #--
        self.text.insert ( END, contents )

    def writeHandler ( self ):
        """Handler for the write button.

            Gets the file name from self.fileNameEntry and
            tries to create a new file by that name, and then
            writes the contents of self.text to that file.
        """
        #--
        # Get the file name and try to open it.
        #--
        fileName  =  self.fileNameVar.get()
        print "*** Writing to file '%s'" % fileName
        try:
            outFile  =  open ( fileName, "w" )
        except IOError, detail:
            print "*** Couldn't open '%s': %s" % (fileName, detail)
            sys.exit()
        
        #--
        # Get the contents of the text widget.  Position "1.0"
        # is the beginning and END (from Tkinter) is after the
        # end.
        #--
        contents  =  self.text.get ( "1.0", END )

        #--
        # Append contents to the outFile.
        #--
        outFile.write ( contents )
        outFile.close()

#================================================================
# Main
#----------------------------------------------------------------

app = Application()
app.master.title("Sample application")
app.mainloop()