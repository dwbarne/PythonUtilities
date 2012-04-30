# from "Programming Python - 2nd Edition" by Mark Lutz, p. 328
#
# Example 7-20. PP2E\Gui\Tour\entry3.py

from Tkinter import *
from quitter import Quitter

field='Name'

def fetch(variable):
    print 
    for v1 in variable:
         print 'Input => %s' % v1.get()       #get from var
        
def makeform(root, fields):
    form=Frame(root)                                #make outer frame
    left=Frame(form)                                #make 2 columns
    rite=Frame(form)
    form.pack(fill=X)
    left.pack(side=LEFT)
    rite.pack(side=RIGHT, expand=YES, fill=X)       #grow horizontally
    
    variable=[]

    lab=Label(left, width=5, text=field)        #add to columns
    ent=Entry(rite)
    lab.pack(side=TOP)
    ent.pack(side=TOP, fill=X)                  #grow horizontallly
    var=StringVar()
    ent.config(textvariable=var)                #link field to var
    var.set('enter here')
    variable.append(var)
    return variable
    
if __name__ == '__main__':
    root=Tk()
    var=makeform(root, field)
    print " *** Here are the vars:"
    for var1 in var:
        print " var = ", var1.get()

    Button(
        root,
        text='Fetch',
        command=(lambda v=var: fetch(v))
        ).pack(side=LEFT)
    Quitter(root).pack(side=RIGHT)
    root.bind(
    '<Return>', 
    (lambda event, v=var: fetch(v))
    )
    root.mainloop()
    