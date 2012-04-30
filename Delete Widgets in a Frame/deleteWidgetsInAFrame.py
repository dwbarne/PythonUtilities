# filename: deleteWidgetsInAFrame.py
# purpose: delete widgets from a frame
# date: 021109
from Tkinter import *

class App:
    def __init__(self, parent):
        self.parent = parent
        self.parent.geometry("500x350")

        self.list_of_widgets = []

#----------------------------Contstants for Buttons------------

        button_padx = "2m"
        button_pady = "1m"

#--------------------------end constants-----------------------

        self.baseContainer = Frame(self.parent)
        self.baseContainer.pack(side=TOP, fill = BOTH, expand=NO)

#the Top Frame with all the buttons
        self.topContainer = Frame(self.baseContainer)
        self.topContainer.pack(side=TOP, expand=YES, ipadx=5,
        ipady=5, fill = X, anchor=N)

#the frame with the main things the user will use
        self.mainContainer = Frame(self.baseContainer)
        self.mainContainer.pack(side=TOP,
            ipadx = 5,
            ipady = 5,
            anchor=CENTER,
            expand=YES,
            fill=BOTH
            )

#---------------------Top Buttons-----------------------------

        self.defineButton = Button(
            self.topContainer,
            padx=button_padx,
            pady=button_pady
            )
        self.defineButton.configure(
            text="Word List",
            command=self.define_Frame
            )
        self.defineButton.pack(side=LEFT)

#--------------------------------------------------------------
    def define_Frame(self):
# destroy all the child widgets of the Frame
        for widget in self.list_of_widgets:
            widget.destroy()
            
        self.list_of_widgets = []

        myMessage="Please type in all the words that you would like to define"
        xxx = Label(self.mainContainer, text=myMessage,
            justify=LEFT)
        xxx.pack(side=TOP, anchor=N)
        self.list_of_widgets.append(xxx)

 #The LEFT Frame that comes up when you hit define
        self.defineContainer1 = Frame(self.mainContainer)
        self.defineContainer1.pack(side=LEFT, ipadx = 5,
            ipady = 5, expand=YES, fill=BOTH)
        self.list_of_widgets.append(self.defineContainer1)

 #The RIGHT Frame that comes up when you hit define
        self.defineContainer2 = Frame(self.mainContainer)
        self.defineContainer2.pack(side=LEFT, ipadx=5,
            ipady=5, expand=YES, fill=BOTH)
        self.list_of_widgets.append(self.defineContainer2)

 #This frame is where the define button goes
        self.defineButtonF = Frame(self.baseContainer)
        self.defineButtonF.pack(side=TOP,
            anchor=S,
            ipady=5,
            ipadx=5,
            fill=BOTH,
            expand=NO)
        self.list_of_widgets.append(self.defineButtonF)

#---------------Contstants for Buttons------------

        self.button_padx = "2m"
        self.button_pady = "1m"

#-----------------end constants-----------------------




#----------STUFF FOR DEFINE FRAME-------------------------

        self.e1 = Entry(self.defineContainer1)
        self.e1.pack(fill=X)

        self.e2 = Entry(self.defineContainer1)
        self.e2.pack(fill=X)

        self.e3 = Entry(self.defineContainer1)
        self.e3.pack(fill=X)

        self.e4 = Entry(self.defineContainer1)
        self.e4.pack(fill=X)

        self.e5 = Entry(self.defineContainer1)
        self.e5.pack(fill=X)

        self.e6 = Entry(self.defineContainer1)
        self.e6.pack(fill=X)

        self.e7 = Entry(self.defineContainer1)
        self.e7.pack(fill=X)

        self.e8 = Entry(self.defineContainer2)
        self.e8.pack(fill=X)

        self.e9 = Entry(self.defineContainer2)
        self.e9.pack(fill=X)

        self.e10 = Entry(self.defineContainer2)
        self.e10.pack(fill=X)

        self.e11 = Entry(self.defineContainer2)
        self.e11.pack(fill=X)

        self.e12 = Entry(self.defineContainer2)
        self.e12.pack(fill=X)

        self.e13 = Entry(self.defineContainer2)
        self.e13.pack(fill=X)

        self.e14 = Entry(self.defineContainer2,)
        self.e14.pack(fill=X)

#------Define Button Stuff-------------------------

#Define it button
        self.defineIt= Button(self.defineButtonF,
            command=self.DefineClick)
        self.defineIt.configure(text="Define!")
        self.defineIt.bind("<Return>", 
            self.DefineClickE)
        self.defineIt.pack(side=TOP,
            anchor=N,
            padx=self.button_padx,
            pady=self.button_pady,)
            
    def DefineClickE(self, event):
        print "Define was hit with Enter"
        self.DefineClick()
        
    def DefineClick(self):
        print "Define was activated."

#-------end define Button Stuff----------------------
 
root = Tk()
app = App(root)
root.mainloop() 
