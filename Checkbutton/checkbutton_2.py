# Example 7-22. PP2E\GUI\Tour\demoCheck.py
#  from book, "Programming Python"

from Tkinter import *
import sys

class Demo(Frame):
    def __init__(self,parent=None, **args):
        Frame.__init__(self,parent,args)
        self.pack()
        self.tools()
        Label(self, text='Check demos').pack()
        self.vars=[]
        demos={
            'Error': 'print 1',
            'Input': 'print 2',
            'Open': 'print 3',
            'Query': 'print 4',
            'Color': 'print 5'
            }
        
        for key in demos.keys():
            var=IntVar()
            Checkbutton(self,
                text=key,
                variable=var,
                command=demos[key]
                ).pack(side=LEFT)
            self.vars.append(var)
    def report(self):
        for var in self.vars:
            print var.get(),
        print '\nself.vars =',self.vars
        print
    def tools(self):
        frm=Frame(self)
        frm.pack(side=RIGHT)
        Button(frm,text='State',command=self.report).pack(fill=X)
        Button(frm,text='Quit',command=(lambda: sys.exit())).pack(fill=X)
        
if __name__ == '__main__': 
    Demo().mainloop()