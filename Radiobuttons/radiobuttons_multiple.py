from Tkinter import *

class Demo(Frame):
    def __init__(self,parent):
        Frame.__init__(self)
        self.frameParent=parent
        
        self.frame1=Frame(
            self.frameParent,
            )
        self.frame1.grid(
            row=0,
            column=0,
            )
            
        self.frame2=Frame(
            self.frameParent,
            )
        self.frame2.grid(
            row=0,
            column=1,
            )
            
        self.frame3 = Frame(
            self.frameParent,
            )
        self.frame3.grid(
            row=1,
            column=0,
            columnspan=99,
            )
        
        self.createWidgets()
        
    def createWidgets(self):

# one attribute to rule them all
#        self.varFieldName_Key = []
# iterate to list all fields
        irow=0
        for numField in range(1):
# column 'No.'
            icol=0
            
# label for button 1
            label1 = Label(
                self.frame1,
                text='Radiobutton 1: '
                )
            label1.grid(
                row=irow,
                column=icol,
                pady=5,
                )
                
            icol+=1
# radiobutton 1
#            self.varFieldName_Key.append(numField)
#            self.varFieldName_Key[numField] = IntVar
            self.varFieldName_Key = IntVar()
#            self.radiobuttonFieldName_Key.append('')
#            self.radiobuttonFieldName_Key[numField] = Radiobutton(
            self.radiobuttonFieldName_Key1 = Radiobutton(
                self.frame1,
                selectcolor='white',
#                variable=self.varFieldName_Key[numField],
                variable=self.varFieldName_Key,
#                value=numField+1,
                value=5,
                bg='tan',
                relief=FLAT,
                command=self.handler1,
                )
#            self.radiobuttonFieldName_Key[numField].grid(
            self.radiobuttonFieldName_Key1.grid(
                row=irow,
                column=icol,
                padx=2,
                pady=5
                )
                
            irow+=1
            icol=0
  
# label for button 2
            label2 = Label(
                self.frame2,
                text='Radiobutton 2:',
                )
            label2.grid(
                row=irow,
                column=icol,
                padx=2,
                pady=5,
                )
 
# radiobutton 2
            icol+=1
#            self.varFieldName_Key.append(numField)
#            self.varFieldName_Key[numField] = IntVar
#            self.radiobuttonFieldName_Key.append('')
#            self.radiobuttonFieldName_Key[numField] = Radiobutton(
            self.radiobuttonFieldName_Key2 = Radiobutton(
                self.frame2,
                selectcolor='white',
                variable=self.varFieldName_Key,
#                value=numField+2,
                value=10,
                bg='tan',
                relief=FLAT,
                command=self.handler1,
                )
#            self.radiobuttonFieldName_Key[numField].grid(
            self.radiobuttonFieldName_Key2.grid(
                row=irow,
                column=icol,
                padx=2,
                pady=5
                )
                
# increment row            
            irow+=1
            
        buttonQuit = Button(
            self.frame3,
            text='Quit',
            width=20,
            command=(lambda: self.frameParent.destroy()),
            )
        buttonQuit.grid(
            row=99,
            column=0,
            columnspan=3,
            pady=20,
            )
            


# ---- handlers go here

    def handler1(self):
        if self.varFieldName_Key.get() == 1:
            print '\n** Radiobutton1 is SET.'
        elif self.varFieldName_Key.get() == 2:
            print '\n** Radiobutton2 is set.'
        else:
            print '\n** Buttons are NOT set!'
            
        stateButton = self.varFieldName_Key.get()
        print '  state of self.varFieldName_Key.get():',stateButton
        
        print '  resetting button'
        
        if self.varFieldName_Key:
            self.varFieldName_Key.set(0)
            print ' >> Button has been cleared'
        else:
            self.varFieldName_Key.set(1)
            print ' >> Button has been set'
        stateButton = self.varFieldName_Key.get()
        print '  NEW state of self.varFieldName_Key.get():',stateButton        

# try test to see if this affects radiobuttons' assignments; it does not        
#        self.varFieldName_Key.set(3)
#        print '  altered state of self.varFieldName_Key:',self.varFieldName_Key.get()
# below is not allowed, no attribute 'get' for this Radiobutton instance
#        temp = self.radiobuttonFieldName_Key1.get()
#        print ' >>> temp = ',temp
        
        

   
   
    def handler2(self):
        if self.varFieldName_Key:
            print '\n Radiobutton2 is SET.'
        else:
            print '\n Radiobutton2 is NOT SET.'
            
        stateButton2 = self.varFieldName_Key.get()
        print 'state of button2:',stateButton2
   
   
   

root=Tk()    
app=Demo(root)
app.master.title('demo: radiobuttons')
app.mainloop()