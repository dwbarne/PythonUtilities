#! usr\\bin\\env python
from Tkinter import *

# from
# http://webmail.earthlink.net/wam/msg.jsp?msgid=32517&x=-815335918
# June 3, 2009


def myfiles (n='',m=''):
    import os
    mf=[os.path.join(x,i)for x,y,z in os.walk(n) for i in z if
i.endswith(m)]

    return mf

def fshow():
    tclear()
    x=entry1.get()

    try:
       value1,value2=x.split(',')
       mf=myfiles(value1,value2)

       text.insert(END,('Total files in %s are %d\n'%
        (entry1.get(),len(mf)))+ mystring(mf))
    except:
        mf=myfiles(x)
        text.insert(END,('Total files in %s are %d\n'%
            (entry1.get(),len(mf)))+ mystring(mf))

def atime(x):

    import time
    import os
    atime=time.strftime("%c",time.localtime(os.path.getatime(x)))
    return atime

def mtime(x):
    import time
    import os
    mtime=time.strftime("%c",time.localtime(os.path.getmtime(x)))
    return mtime

def ctime(x):
    import time
    import os
    ctime=time.strftime("%c",time.localtime(os.path.getctime(x)))
    return ctime
def mystring(x):
    q=''
    for n,m in  enumerate(x,start=1):
        o=str(n)+'.'+str(m)
        q+=(o+'\n')
    return q+'\n'

def info():
    tclear()
    import glob,os
    mf=''
    md=''
    mfl,mdl=[],[]
    mdd=glob.glob(entry1.get()+os.sep+'*')
    for x in mdd:
        if os.path.isfile(x)==True:
            mfl.append(x)
        else:mdl.append(x)

        mf+=mystring(mfl)
        md+=mystring(mdl)
        mf=("Total files in %s are %d \n\n"%(entry1.get(),len(mfl)))+mf
        md=('Total directories in %s are %d\n\n'%(entry1.get(),len(mdl)))+md
        mf+='\n\n'
        text.insert(END,mf+md)
        
def destroy():
    root.destroy()
    
def eclear():
    entry1.delete(0,END)
    entry2.delete(0,END)
    entry3.delete(0,END)
    entry4.delete(0,END)
def tclear():
    text.delete(1.0,END)
    
def ashow():
    x=entry1.get()
    try:
        n,m=x.split(',')
        value=atime(n)
    except:value=atime(x)
    entry2.insert(0,value)
    
def mshow():
    x=entry1.get()
    try:
        n,m=x.split(',')
        value=mtime(n)
    except:value=mtime(x)
    entry3.insert(0,value)
    
def cshow():
    x=entry1.get()
    try:
        n,m=x.split(',')
        value=ctime(n)
    except:value=ctime(x)
    entry4.insert(0,value)

root = Tk()

frame1=Frame(root,relief='sunken',border=1)
frame1.pack(side='top',expand="true")

frame2=Frame(root,relief='sunken',border=1)
frame2.pack(side='top',expand="true")

frame3=Frame(root,relief='sunken',border=1)
frame3.pack(side='top',expand="true")

frame4=Frame(root,relief='sunken',border=1,)
frame4.pack(side='top',expand="true")

frame5=Frame(root,relief='sunken',border=1)
frame5.pack(side='top',expand="true")

label5=Label(frame1,text="Enter file path to get information about the file\
or enter directory(or directory,fileextension) to get files init ",border=1)
label5.pack(side='top',fill='both')

b1=Button(frame2,text='quit',command=destroy,border=1)
b1.pack(side='left',padx=5,pady=5)

b2=Button(frame2,text='clear',command=eclear,border=1)
b2.pack(side='left',padx=5,pady=5)

b3=Button(frame2,text='accessed',command=ashow,border=1)
b3.pack(side='left',padx=5,pady=5)

b4=Button(frame2,text='modified',command=mshow,border=1)
b4.pack(side='left',padx=5,pady=5)

b5=Button(frame2,text='created',command=cshow,border=1)
b5.pack(side='left',padx=5,pady=5)

b5=Button(frame2,text='files',command=fshow,border=1)
b5.pack(side='left',padx=5,pady=5)

b6=Button(frame2,text='deltxt',command=tclear,border=1)
b6.pack(side='left',padx=5,pady=5)

b7=Button(frame2,text='files+dirs',command=info,border=1)
b7.pack(side='left',padx=5,pady=5)

label4=Label(frame3,text="Enter full path",border=1)
label4.pack(side='left',fill='both')

entry1=Entry(frame3,relief='sunken',border=1)
entry1.pack(side='left',fill='both')

lable1=Label(frame3,text='access time',border=1)
lable1.pack(side='left',fill='both')

entry2=Entry(frame3,relief='sunken',border=1)
entry2.pack(side='left',fill='both')

lable2=Label(frame3,text='modifide time',border=1)
lable2.pack(side='left',fill='both')

entry3=Entry(frame3,relief='sunken',border=1)
entry3.pack(side='left',fill='both')

lable3=Label(frame3,text='created time',border=1)
lable3.pack(side='left',fill='both')

entry4=Entry(frame3,relief='sunken',border=1)
entry4.pack(side='left',fill='both')

text=Text(frame4,relief='sunken',border=1,width=130,height=40,padx=5,pady=5)
text.pack(side='top')
text.xview(SCROLL,30,UNITS)
text.yview(SCROLL,30,UNITS)

root.title("info of file")

root.mainloop()
