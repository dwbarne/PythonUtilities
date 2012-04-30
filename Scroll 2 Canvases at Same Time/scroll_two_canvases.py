from Tkinter import *

"""
from
http://www.faqts.com/knowledge_base/view.phtml/aid/5447/fid/264

Problem:

In Tkinter, can you connect a scrollbar to 2 objects (In my case I need
it to be on 2 canvases, or canvii, if you prefer).  The
canvases(canvaii) are next to each other horizontally, and I want them
to scroll down like one canvas.  I would just combine them, but I need
two so that the horizontal scroll will work correctly.

Solution:

Yes, you can. All you need to do is to set the scrollbar's command to
your own function that passes the arguments it's called with to the
xview or yview methods of both canvases. I'll append an example.
"""

class mainWin:
  def __init__(self,tkRoot):
    self.tkRoot=tkRoot
    self.createWidgets()
    return None

  def createWidgets(self):
    self.c1=Canvas(self.tkRoot,bg="blue",width="2i",height="2i", \
      scrollregion=(0, 0, "4i", "4i"))
    self.c1.pack(side=LEFT)
    self.c2=Canvas(self.tkRoot,bg="green",width="2i",height="2i", \
     scrollregion=(0, 0, "4i", "4i"))
    self.c2.pack(side=LEFT)
    self.sb=Scrollbar(orient="vertical")
    self.sb.pack(side=LEFT,fill=Y)
    self.sb['command']=self.scrollTwo
    self.c2['yscrollcommand']=self.sb.set

    self.c1.create_rectangle("0.5i", "0.5i", "1i", "1i", fill="black")
    self.c2.create_rectangle("0.5i", "0.5i", "1i", "1i", fill="yellow")

    return None

  def scrollTwo(self,*args):
    print args
    apply(self.c1.yview,args)
    apply(self.c2.yview,args)
    return None

def main():
  tkRoot=Tk()
  mainWin(tkRoot)
  tkRoot.mainloop()
  

if __name__=='__main__':
  main()