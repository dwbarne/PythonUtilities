from Tkinter import *

class Temp(Frame):
    def __init__(self,parent):
        Frame.__init__(self)
        self.frameParent = parent        
        self.createWidgets()
    
    def createWidgets(self):
    
        self.varFieldName1 = StringVar()
        self.varFieldName1.set('')
        self.entryFieldName1 = Entry(
            self.frameParent,
            bg='white',
            relief=SUNKEN,
            width=5,
            textvariable=self.varFieldName1
            )
        self.entryFieldName1.grid(
            row=0,
            column=0,
            padx=2,
            sticky=N,
            )
        
        self.varFieldName2 = StringVar()
        self.varFieldName2.set('')
        self.entryFieldName1 = Entry(
            self.frameParent,
            bg='white',
            relief=SUNKEN,
            width=25,
            textvariable=self.varFieldName2,
            )
        self.entryFieldName1.grid(
            row=0,
            column=1,
            padx=2,
            sticky=N,
            )
            
        self.buttonPrint1 = Button(
            text='Print 1',
            borderwidth=5,
            relief=RAISED,
            command=self.handlerPrint1,
            )
        self.buttonPrint1.grid(
            row=1,
            column=0,
            pady=5,
            padx=5,
            )
            
        self.buttonPrint2 = Button(
            text='Print 2',
            borderwidth=5,
            relief=RAISED,
            command=self.handlerPrint2,
            )
        self.buttonPrint2.grid(
            row=1,
            column=1,
            pady=5,
            padx=5,
            )
    def handlerPrint1(self):
        print '\n Entry 1 contains:', self.entryFieldName1.get()
        print '\n Entry 1 from textvariable:', self.varFieldName1.get()
        
    def handlerPrint2(self):
        print '\n Entry 2 contains:', self.entryFieldName1.get()
        print '\n Entry 2 from textvariable:', self.varFieldName2.get()
            
                    
#======== main ============
root=Tk()
app=Temp(root)
app.master.title('Two entries, same textvariable')
app.mainloop()
