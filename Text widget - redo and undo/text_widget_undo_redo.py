# from
#  http://mail.python.org/pipermail/python-list/2002-August/161510.html

from Tkinter import *
import string


#_DEBUG=None
_DEBUG=True


class SmartText(Text):
    def __init__(self, parent):
        Text.__init__(self, parent)
        
        self.redoList=[]
        self.undoList=[]
        
        
        self.bind("<Control-u>", self.undo)
        self.bind("<Control-r>", self.redo)
        self.bind("<Any-KeyPress>", self.recordUndo)
        
    def recordUndo(self, event):
        
        if _DEBUG: 
            print '  event.keycode = ',event.keycode
            print '  event.keysysm = ',event.keysym
            print '  event.keysym_num = ',event.keysym_num
            print ''
        
        
# first check the selection and clipboard
# if anything is selected then they may be about to delete 
# it
        text=event.widget
        try:
            selection=text.get("sel.first", "sel.last")
            sel_start = text.index("sel.first")
            sel_stop = text.index("sel.last")
        except TclError:
            selection=None           
             
# first get cursor position.... 
# now what are they about to do.....
# print event.keycode, event.keysym, event.keysym_num
       
        start = text.index("insert")
        stop = start

        whitespace=("space", "Return", "Tab", "Delete", "BackSpace")
        allkeys = string.letters + string.digits + string.punctuation
        if len(event.keysym)==1:            
            if event.keysym in allkeys:
                
                if selection:
                    self.undoList.append((sel_start, 
                        sel_stop, "delete", selection))
                    start=sel_start
                    stop=sel_stop
                
                self.undoList.append((start, stop, "insert", event.keysym))
                
                
        else:
# is it white space.....
            if event.keysym in whitespace:
                if selection:
                    self.undoList.append((sel_start, 
                        sel_stop, "delete", selection))
                    start=sel_start
                    stop=sel_stop
                if event.keysym=="Return":
                    key="\n"
                    self.undoList.append((start, stop, "insert", key))
                elif event.keysym=="Tab":
                    key="\t"
                    self.undoList.append((start, stop, "insert", key))
                elif event.keysym=="space":
                    key=" "
                    self.undoList.append((start, stop, "insert", key))
                elif event.keysym=="Delete":
                    if not selection:
                        key=text.get(start, start + "+ 1 char")
                        self.undoList.append((start, stop, "delete", key))
                elif event.keysym=="BackSpace":
                    if not selection:
                        key=text.get(start + "- 1 char", start )
                        self.undoList.append((start, stop, "delete", key))
                    
                
        
    def redo(self, event):
        if _DEBUG: print "redo called"
        try:
            last=self.redoList.pop()
        except IndexError:
            if _DEBUG: print "redoList empty"
            return
            
        if _DEBUG: print last
            
        text=event.widget
        start=last[0]
        stop=last[1]
        
        if last[2]=="delete":
            if start==stop:
                text.delete(start)
            else:
                text.delete(start, stop)
        elif last[2]=="insert":
            text.insert(start, last[3])
        self.undoList.append(last)
        return "break"
        
    def undo(self, event):
        if _DEBUG: print "undo called"
        try:
            last=self.undoList.pop()
        except IndexError:
            if _DEBUG: print "undoList empty"
            return
        text=event.widget
        
        start=last[0]
        stop=last[1]
        
        if last[2]=="insert": 
# if the text was inserted then delete it
            if start==stop:
                text.delete(start)
            else:
                text.delete(start, stop)
        elif last[2]=="delete": 
# however if it was deleted then insert it.
            text.insert(start, last[3])
        self.redoList.append(last)
        return "break"


if __name__=="__main__":
    root=Tk()
    st=SmartText(root)
    st.pack(fill='both', expand='yes')
    st.config(font="Helvetica 12")
    root.mainloop()
