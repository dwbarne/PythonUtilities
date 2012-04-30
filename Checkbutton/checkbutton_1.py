# checkbutton frame using python & Tkinter
#   date: 070808

# This file sets a variable to true or false, depending on whether the box is checked or not, respectively

from Tkinter import *
import tkFont
import string

class CheckButton_1(Frame):
    def __init__(self,rowx,coly,msg):
        Frame.__init__(self,master)
        self.rowx=rowx
        self.coly=coly
        self.msg=msg
        self.grid(
            rowspan=1,
            columnspan=1,
#            sticky=NSEW, 
            padx=10,
            pady=10,
            ipadx=10,
            ipady=10
            )
        self.createWidgets()
        
    def createWidgets(self):   
# define data font
        dataFont = tkFont.Font(
            family="Helvetica",
            size="10"
            )
            
        self.var = IntVar()
        
        c = Checkbutton(
            master, 
            text=self.msg,
            variable=self.var,
            command=self.checkButtonHandler,
            relief=RIDGE,
            justify=CENTER,
            borderwidth=5,
            font=dataFont,
            padx=10,
            pady=10,
            )
        c.grid(
            row=self.rowx, 
            column=self.coly,
            padx=20,
            pady=20,
            )

    def checkButtonHandler(self):
        import string
        self.doNotSend=self.var.get()
        if self.doNotSend:
            print "\nINFO: email will NOT be sent to your inbox"
        else:
            print "\nINFO: email will be sent to your inbox"
    
if __name__ == "__main__":
    master=Tk()
    master.title("Checkbutton test")
    row=0
    column=0
    msg='If checked, do NOT send me a copy of this email'
    check=CheckButton_1(row,column,msg)
    check.mainloop()
