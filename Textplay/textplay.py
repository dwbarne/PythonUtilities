#!/usr/local/bin/python
from Tkinter import *
import tkFont
import Image                # Python Imaging Library
import ImageTk              # PIL <-> Tkinter adapter


BACKGROUND  =  "#fff4e0"      # Standard background color
ACTIVE_FG   =  "#664400"      # Standard active foreground color
ACTIVE_BG   =  "#ffbb18"      # Standard active background color
TROUGH      =  "#997744"      # Standard trough color
TEXT_WIDE   =  50
TEXT_HIGH   =  10

def showOptions ( w, what ):
    """Shows all the options for a widget `w' with annotation string `what'
    """
    print "@@@ options for %s:" % what
    id = w.winfo_id()
    path = w.winfo_pathname(id)
    print ( "@@@   name=<%s> .winfo_name=<%s> .winfo_pathname=<%s>" %
            (str(w), w.winfo_name(), path) )
    print "@@@ nametowidget(path)=", w.nametowidget(path)
#### #--This commented-out part shows the 5- and 2-tuples, but all
#### #--the user probably cares about is the value.
####    D = w.config()
####    keyList = D.keys()
####    keyList.sort()
####    for key in keyList:
####        print "@@@   [%s]: <%s>" % (key, D[key])     
    print "@@@   ",
    for optName in w.keys():
        print "%s=<%s>" % (optName, `w.cget(optName)`),
    print


class Test(Frame):
    ###################################################################
    ###### Event callbacks for THE CANVAS (not the stuff drawn on it)
    ###################################################################
    def mouseDown(self, event):
        # remember where the mouse went down
        self.lastx = event.x
        self.lasty = event.y

    def mouseMove(self, event):
        # whatever the mouse is over gets tagged as CURRENT for free by tk.
        self.draw.move(CURRENT, event.x - self.lastx, event.y - self.lasty)
        self.lastx = event.x
        self.lasty = event.y

    ###################################################################
    ###### Event callbacks for canvas ITEMS (stuff drawn on the canvas)
    ###################################################################
    def mouseEnter(self, event):
        # the CURRENT tag is applied to the object the cursor is over.
        # this happens automatically.
        self.draw.itemconfig(CURRENT, fill="red")
         
    def mouseLeave(self, event):
        # the CURRENT tag is applied to the object the cursor is over.
        # this happens automatically.
        self.draw.itemconfig(CURRENT, fill="blue")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
####        self["bg"]  =  BACKGROUND
####        self.master.option_add("*background", BACKGROUND)
####        self.master.option_add("*activeforeground", ACTIVE_FG)
####        self.master.option_add("*activebackground", ACTIVE_BG)
####        self.master.option_add("*troughcolor", TROUGH)
        self.imageList = []    # Kluge for images; see labelplay.py
        self.__createWidgets()
        print "@@@ app.children.keys()=", self.children.keys()
        print "@@@ app.bindtags()=", self.bindtags()
        showOptions(self.winfo_toplevel(), "ROOT")

#--
# This next one is really cool: it arranges for self.__extraHandler
# to be called when any button is clicked, in addition to its
# existing bindings.
#--
####        self.bind_class("Button", "<Button-1>", self.__extraHandler, "+")

    def __createWidgets(self):
        self.giantFont = tkFont.Font(family="times", size=72)
        self.bigFont = tkFont.Font(family="helvetica", size=20)
        self.tt14Font = tkFont.Font(family="lucidatypewriter",
            size=14)
        self.tt18Font = tkFont.Font(family="lucidatypewriter",
            size=18)
        self.helv20Font = tkFont.Font(family="helvetica",
            size=20)

        self.fruitImage = Image.open ( "apple.jpg" )
        self.fruitTk    = ImageTk.PhotoImage ( self.fruitImage )
        self.imageList.append ( self.fruitTk )  # Kluge, see labelplay.py
        self.top  =  self.winfo_toplevel()
        print "@@@ self.winfo_toplevel()=", self.top
        print "@@@   Type of that is ", type(self.top)
        self.top.title("BOOGA BOOGA")

#================================================================
        self.top = Toplevel (
            width="7i", height="2i",
            relief=SUNKEN,
            bd="0.25i",
            class_="prune",
            bg="PapayaWhip" )
        self.top.lift()

        self.t = Text ( self,
####            relief=GROOVE,
####            padx=100, pady=20,
####            spacing1=10,
####            spacing2=10,
            tabs=("1i", "2i", CENTER, "3i", RIGHT, "4i", NUMERIC),
            insertofftime=50,
####            insertontime=250,
            insertbackground="magenta",
            insertborderwidth=5,
            insertwidth=20,
            wrap=NONE,
            selectbackground="NavajoWhite",
            selectforeground="turquoise3",
            selectborderwidth=1,
            fg="MidnightBlue",
            bg="azure3",
            bd=20,
            font=self.tt18Font,
            height=TEXT_HIGH, width=TEXT_WIDE )
        self.t.grid ( row=0, column=0, padx=10, pady=10,
            sticky=NW )

        #--
        # Add scrollbars
        #--
        self.scrollY = Scrollbar ( self, orient=VERTICAL,
            command=self.t.yview )
        self.scrollY.grid ( row=0, column=1, sticky=N+S )

        self.scrollX = Scrollbar ( self, orient=HORIZONTAL,
            command=self.t.xview )
        self.scrollX.grid ( row=1, column=0, sticky=E+W )

        self.t["xscrollcommand"]  =  self.scrollX.set
        self.t["yscrollcommand"]  =  self.scrollY.set

        #--
        # Stick some text in
        #--
        self.t.insert(END, "The quick brown fox jumps over the lazy dog.\n" )
        self.t.insert(END, "0         1         2         3\n" )
        self.t.insert(END, "0....5....0....5....0....5....0\n" )
        self.t.insert(END, "abcdefghijklmnopqrstuvwxyz\n" )

        #--
        # Change line 4 to giant font
        #--
        self.t.tag_add("giant", "4.0", "4.9")
        self.t.tag_config("giant",
            background="orchid",
            fgstipple="gray50",
            bgstipple="gray12",
            font=self.giantFont)

        #--
        # See how insertion at a mark works
        #--
        self.t.mark_set("pre-d", "4.3")
        self.t.mark_gravity("pre-d", LEFT)
        self.t.insert("pre-d", "xxx")
        print "Mark pre-d =", self.t.index("pre-d")
        self.t.insert("pre-d", "zzzz")
        print "Gravity of pre-d is ", self.t.mark_gravity("pre-d")
        print "Mark names:", self.t.mark_names()

        #--
        # Embed an image
        #--
        self.t.image_create("pre-d",
            align=BASELINE,
            padx=5, pady=5,
            name="appil",
            image=self.fruitTk )
        D = self.t.image_configure("appil")
        print "@@@ appil options:"
        keyList = D.keys()
        keyList.sort()
        for key in keyList:
            print "[%s]=<%s>" % (key, D[key])

        #--
        # Embed a button using the `window=' option
        #--
        self.t.insert("5.0", "lag")
        self.t.tag_add("giant", "5.0", "5.end")

        self.panicButton = Button ( self,
            text="PANIC",
            font=self.bigFont,
            command=self.__panicHandler )
        self.t.window_create ( "5.1",
            align=BOTTOM,
            window=self.panicButton )
        showOptions(self.panicButton, "panic-button") #@@@

        #--
        # Embed a button using the `create=' callback
        #--
        self.t.window_create ( "5.3",
####            align=BASELINE,
            stretch=1,
            padx=30,
            create=self.__dreamBuilder )

        #--
        # Play with various methods
        #--
####        self.t["font"]=self.tt14Font

        #--
        # Tag a region and change its font and color
        #--
        self.t.tag_add("tag1", "4.7", "4.end")
        self.t.tag_config("tag1",
            overstrike=1,
            foreground="coral",
            font=self.helv20Font)

        #--
        # Try out string search (straight string and regexp)
        #--
        matchLen = IntVar()
        match = self.t.search ( "xx", "1.0", count=matchLen )
        if  match:
            print ( "Found xx at %s, length %d" %
                     ( match, matchLen.get() ) )
        else:
            print "Didn't find xx."

        match = self.t.search ( "[a-z][a-z][a-z][a-z]*", "4.0",
            regexp=1,
            count=matchLen )
        if match:
            print ( "Found 4+ alphas at %s, length %d" %
                     ( match, matchLen.get() ) )
        else:
            print "Didn't find 4+ alphas."

        #--
        # These features do not seem to work
        #--
        print "pre-d bbox is", self.t.bbox("pre-d")
        print "pre-d as an index is", self.t.index("pre-d")
        print "Apple bbox is", self.t.bbox(self.t.index("pre-d"))
        print "1.0 is", self.t.bbox("1.0")        
        print "4.0 bbox is", self.t.bbox("4.0")

        print "Here come the .dlineinfos:"
        for i in range(1, 5):
            linex = "%d.0" % i
            print "[%s] = %s" % (linex, self.t.dlineinfo(linex))

        #--
        # Pack all the buttons L-to-R in a frame on the bottom
        #--
        self.buttonFrame = Frame ( self )
        self.buttonFrame.grid ( row=3, column=0,
            pady=10,
            sticky=W,
            columnspan=99 )

        #--
        # Add a button to pull the selection out and display it in
        # a label
        #--
        self.selectVar = StringVar()
        self.selectLabel = Label ( self,
            font=self.tt14Font,
            justify=LEFT,
            anchor=NW,
            relief=GROOVE,
            height=TEXT_HIGH,
            width=TEXT_WIDE,
            textvariable=self.selectVar )
        self.selectLabel.grid ( row=2, column=0, 
            sticky=W,
            padx=10, pady=10 )
        showOptions(self, ".selectLabel")   # @@@
        print "@@@ .selectLabel.bindtags()=", self.selectLabel.bindtags()

        #--
        # Venerable QUIT button
        #--
        colx  =  0
        self.QUIT = Button ( self.buttonFrame,
            foreground="red",  
            font=self.bigFont,
            activeforeground=ACTIVE_FG,
            activebackground=ACTIVE_BG,
            command=self.quit,
            text="Quit" )
        self.QUIT.grid ( row=0, column=colx, padx=5 )
        colx  =  colx + 1

        #--
        # Button to copy selection to self.selectLabel
        #--
        self.selectButton = Button ( self.buttonFrame,
            font=self.bigFont,
            command=self.__selHandler,
            text="Show selected text" )
        self.selectButton.grid ( row=0, column=colx, padx=5 )
        colx  =  colx + 1

        #--
        # Buttons to `see' top and bottom
        #--
        self.seeTopButton = Button ( self.buttonFrame,
            font=self.bigFont,
            command=self.__seeTopHandler,
            text="See top" )
        self.seeTopButton.grid ( row=0, column=colx, padx=5 )
        colx  =  colx + 1

        self.seeBotButton = Button ( self.buttonFrame,
            font=self.bigFont,
            command=self.__seeBotHandler,
            text="See bottom" )
        self.seeBotButton.grid ( row=0, column=colx, padx=5 )
        colx  =  colx + 1

        #--
        # Button to lower self.top
        #--
        self.lowerTopButton = Button ( self.buttonFrame,
            font=self.bigFont,
            command=self.__lowerTop,
            text="Lower\nTop" )
        self.lowerTopButton.grid ( row=0, column=colx, padx=5 )
        colx  =  colx + 1

        #--
        # Button to lower self.window_toplevel()
        #--
        self.lowerSelfButton = Button ( self.buttonFrame,
            font=self.bigFont,
            command=self.__lowerSelf,
            text="Lower\nSelf" )
        self.lowerSelfButton.grid ( row=0, column=colx, padx=5 )
        colx  =  colx + 1

    def __lowerTop(self):
        self.top.lower()

    def __lowerSelf(self):
        self.winfo_toplevel().lower()
#--
# This next variant is weird. Sometimes it raises self only just
# above self.top, sometimes it raises it all the way.
#--
####        self.winfo_toplevel().tkraise(aboveThis=self.top)

    def __selHandler(self):
        """If there is a selection, show it in self.selectLabel
        """
        try:
            text = self.t.get(SEL_FIRST, SEL_LAST)
            self.selectVar.set(text)
        except TclError:
            pass

    def __panicHandler(self):
        self.panicButton.flash()
        print "@@@ PANIC @@@"

    def __seeTopHandler(self):
        self.t.see("1.0")

    def __seeBotHandler(self):
        self.t.see(END)

    def __dreamBuilder(self):
        """Dynamic creation of an embedded checkbutton.
        """
        result = Checkbutton ( self.t,
            selectcolor="DarkOrchid",
            activeforeground="DarkOrchid",
            activebackground="LavenderBlush2",
            fg="IndianRed",
            bg="wheat",
            relief=GROOVE, bd=2,
            font=self.bigFont,
            padx=5,
            text="Dream on" )
        return result

    def __extraHandler(self, event):
        print "@@@ EXTRA HANDLER!!!"


# - - - - -   M a i n   - - - - -

test = Test()
test.mainloop()
