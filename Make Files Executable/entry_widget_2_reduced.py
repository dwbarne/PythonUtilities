# from "Programming Python - 2nd Edition" by Mark Lutz, p. 328
#
# Example 7-20. PP2E\Gui\Tour\entry3.py

from Tkinter import *
from quitter import Quitter

fields='Name', 'Job', 'Pay'

def fetch(variables):
    print 
    for variable in variables:
        print 'Input => %s' % variable.get()        #get from var
        
def makeform(root, fields):
    form=Frame(root)                                #make outer frame
    left=Frame(form)                                #make 2 columns
    rite=Frame(form)
    form.pack(fill=X)
    left.pack(side=LEFT)
    rite.pack(side=RIGHT, expand=YES, fill=X)       #grow horizontally
    
    variables=[]
    for field in fields:
        lab=Label(left, width=5, text=field)        #add to columns
        ent=Entry(rite)
        lab.pack(side=TOP)
        ent.pack(side=TOP, fill=X)                  #grow horizontallly
        var=StringVar()
        ent.config(textvariable=var)                #link field to var
        var.set('enter here')
        variables.append(var)
    return variables
    
if __name__ == '__main__':
    root=Tk()
    vars=makeform(root, fields)
    print vars
    print " *** Here are the vars:"
    count=0
#    my_var1[]
    for var in vars:
        print var.get()
#        my_var1[count]=var.get()
        my_var2=var.get()
        count+=1
    print
#    print my_var1[0], my_var1[1], my_var1[2]
    print " my_var2 =",my_var2
    print " ***   end of vars ***"
    Button(
        root,
        text='Fetch',
        command=(lambda v=vars: fetch(v))
        ).pack(side=LEFT)
    Quitter(root).pack(side=RIGHT)
    root.bind(
    '<Return>', 
    (lambda event, v=vars: fetch(v))
    )
    root.mainloop()
    