#!/usr/bin/python
# filename:
#   getFirstLine.py
#   get/print first line of text widget

from Tkinter import *

root = Tk()

root.title("test")

root.resizable(0, 0)

def test():
    data1 = t.get(1.0, "1.end")
    print 'len(2.0,2.end) =',len(data1),data1
    data2 = t.get(1.0, END)
    print 'len(2.0,END), data =',len(data2),data2
    print ' END index = ',t.index(END)
    print ' end index = ',t.index('2.end')
    print '++++++++++++'



b = Button(root, text="test", command=test)

b.grid(row=0,column=0,sticky=W)

d1 = Button(root, text='del-end+1',command=lambda: t.delete('2.0',str(eval(t.index('2.end')) + 0.1))) 
d1.grid(row=0,column=1,sticky=W)

d2 = Button(root, text='del-END',command=lambda: t.delete(
    str(eval(t.index(END))-1),END))
d2.grid(row=0,column=2,sticky=W)

q = Button(root, text='quit', command=sys.exit)
q.grid(row=0,column=3,sticky=E)

t = Text(root, width=40, height= 20, bg='white')
t.grid(row=1,column=0,columnspan=4,pady=2)

root.mainloop()