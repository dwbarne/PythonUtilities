# Listbox widget with scrollbars
from Tkinter import *
import tkFont

class Listbox_widget(Frame):
    def __init__(self,master=None,parent=None):
        Frame.__init__(self,parent)
        self.grid(rowspan=12,columnspan=12,sticky=N+S+E+W, padx=10,pady=10,ipadx=10,ipady=10)
        self.createWidget()
         
    def createWidget(self):
        self.yScroll=Scrollbar(self,orient=VERTICAL)
        self.yScroll.grid(row=0, column=1,sticky=N+S)
        
        self.xScroll = Scrollbar(self,orient=HORIZONTAL)
        self.xScroll.grid(row=1,column=0,sticky=E+W)
        
        self.listbox=Listbox(self,
            xscrollcommand=self.xScroll.set,
            yscrollcommand=self.yScroll.set)
        self.listbox.grid(row=0,column=0,sticky=N+S+E+W)
        self.xScroll["command"]=self.listbox.xview
        self.yScroll["command"]=self.listbox.yview
        
app=Listbox_widget()
app.mainloop()