# checkbutton frame using python & Tkinter

from Tkinter import *
import string

class CheckButton_1(Frame):
    def __init__(self,msg):
        Frame.__init__(self,master)
        self.grid(
            )
            
        self.createWidgets()
        
    def createWidgets(self):             
        self.var = IntVar()       
        c = Checkbutton(
            master, 
            text='Check if yes',
            variable=self.var,
            command=self.handlerCheckButton,
            )
        c.grid(
            )
            
    def handlerCheckButton(self):
        self.doNotSend=self.var.get()
        if self.doNotSend:
            print "\nChecked"
        else:
            print "\nNot checked"
            
if __name__ == "__main__":
    master=Tk()
    master.title("Checkbutton test")
    msg='If checked, do NOT send me a copy of this email'
    check=CheckButton_1(msg)
    check.mainloop()
