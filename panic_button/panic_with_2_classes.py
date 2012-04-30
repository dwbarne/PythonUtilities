#!/usr/local/bin/python
from Tkinter import *
import tkFont

class Application1(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont=tkFont.Font(
            family="Helvetica",
            size=-10
            ) # use neg for pixels
        self.createWidgets()

    def createWidgets(self):
        self.panicButton = Button ( 
            self, 
            text="PANIC1!!",
            font=self.buttonFont, 
            command=self.panicHandler
            )
        self.panicButton.grid(row=0, column=0)

        self.panicLabel = Label ( 
            self,
            text="Press panic button when panicky.",
            font=self.buttonFont 
            )
        self.panicLabel.grid ( row=1, column=1)

        self.quitButton = Button ( 
            self, text="Quit",
            font=self.buttonFont, 
            bg="black", 
            fg="white",
            activebackground="cyan", 
            activeforeground="magenta",
            command=self.quit 
            )
        self.quitButton.grid(
            row=99, 
            column=0, 
            columnspan=99,
            sticky=E+W
            )

    def panicHandler(self):
        print "PANIC1 BUTTON PRESSED!! RUN!!!"
        print "" 
        
class Application2(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.buttonFont=tkFont.Font (
            family="Helvetica",
            size=-10
            ) # use neg for pixels
        self.createWidgets()    #NOTE that parentheses are used here, but not in the command statement below

    def createWidgets(self):
        self.panicButton = Button(
            self, text="PANIC2!!",
            font=self.buttonFont, 
            command=self.panicHandler
            )
        self.panicButton.grid(row=0, column=0)

        self.panicLabel = Label(
            self,
            text="Press panic button when panicky.",
            font=self.buttonFont )
        self.panicLabel.grid ( row=1, column=1)

        self.quitButton = Button(
            self, text="Quit",
            font=self.buttonFont, 
            bg="black", 
            fg="white",
            activebackground="cyan", 
            activeforeground="magenta",
            command=self.quit
            )
        self.quitButton.grid(
            row=99, 
            column=0, 
            columnspan=99,
            sticky=E+W
            )

    def panicHandler(self):
        print "PANIC2 BUTTON PRESSED!! RUN!!!"
        print "" 

#- - - - - -  main  - - - - -

app1=Application1()
app1.master.title("Panic1 Button Application")

app2=Application2()
app2.master.title("Panic2 Button Application")

app3=Application1()
app3.master.title("Panic1-again Button Application")

app1.mainloop()
#app2.mainloop()
#app3.mainloop()
	
				
