# checkbutton frame using python & Tkinter
#   date: 070808

# This file sets a variable to true or false, depending on whether the box is checked or not, respectively

from Tkinter import *
import tkFont
import string

#root=Tk()

class CheckButton_1(Frame):
#class CheckButton_1(Frame):
#    def __init__(self,rowx,coly,msg,fontsize,parent=None):
    def __init__(self,rowx,coly,msg,fontsize):
#        Frame.__init__(self,parent)
        Frame.__init__(self)
        self.rowx=rowx
        self.coly=coly
        self.msg=msg
        self.fontsize=fontsize
        self.grid()
#        self.grid(
#            row=0,
#            column=4,
#            rowspan=1,
#            columnspan=2,
##            sticky=NSEW, 
#            padx=2,
#            pady=2,
#            ipadx=1,
#            ipady=1
#            )
        self.createWidgets()
        
    def createWidgets(self):   
# define data font
        dataFont = tkFont.Font(
            family="Helvetica",
            size=self.fontsize
            )
            
        self.var = IntVar()
        
        c = Checkbutton(
            self, 
            text=self.msg,
            variable=self.var,
            command=self.checkButtonHandler,
            relief=RIDGE,
            justify=CENTER,
            borderwidth=5,
            font=dataFont,
            padx=5,
            pady=5,
            )
        c.grid(
#            row=self.rowx, 
#            column=self.coly,
            row=0,
            column=0,
            padx=5,
            pady=5,
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
