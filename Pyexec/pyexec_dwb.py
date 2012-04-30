#!/usr/bin/env python

# for gui:
from Tkinter import *
# for askfilename:
from tkFileDialog import *
# for system calls, such as exit:
import sys
# for different fonts:
import tkFont
# for dates and such:
from time import *
# get canned std dialog:
from tkMessageBox import askokcancel
# to get platform name:
import os

# Import other vital modules
import	sys, string, math 

#----------

class Application(Frame):
#	""" Application for running jobs on various clusters and supercomputers
#		at Sandia Labs.
#	"""

#
	def __init__(self, master=None, parent=None):
		Frame.__init__(self, parent)
		self.grid()

# initialize row and column to place buttons		
		rowx=colx=0
		
# does not work:
# self.pack()

# get system info
		computerName=os.environ['COMPUTERNAME']
		userName=os.environ['USERNAME']
		sessionName=os.environ['SESSIONNAME']
		operatingSystem=os.environ['OS']
		processorArchitecture=os.environ['PROCESSOR_ARCHITECTURE']
		processorIdentifier=os.environ['PROCESSOR_IDENTIFIER']
		currentDirectory=os.getcwd()

# define data font
		self.dataFont = tkFont.Font (
			family="Arial",
			size="10"
			)
		
# define button font
		self.buttonFont = tkFont.Font ( 
			family="Helvetica",
			size="12" 
			)

# define entry font			
		self.entryFont = tkFont.Font ( 
#			family="lucidatypewriter",
			family="arial",
			size="12" 
			)
			
# define top label
		print "\n Running on ",computerName,"\n"
		topLabel = Label (
			self,
			text=
				'SYSTEM DATA\n' +
				'-----------\n' +
				'Machine name: ' + computerName + '\n' +
				'User name: ' + userName + '\n'
				'OS: ' + operatingSystem + '\n'
				'Architecture: ' + processorArchitecture + '\n'
				'Processor: ' + processorIdentifier + '\n'
				'Directory: ' + currentDirectory  ,
			font=self.dataFont,
			foreground="blue",
			background="white",
			borderwidth=5,
			justify=CENTER,
			relief=RIDGE
			)
		topLabel.grid(
			sticky='N',
			row=rowx,
			column=colx
			)
			
# create the buttons
		self.createWidgets()
		
#----------
			
	def createWidgets(self):

#initialize row and column markers for buttons and entry boxes	
		rowx=1
		colx=0
		

# quit button
		self.quitButton = Button (
			self, 
			text="Quit", 
			font=self.buttonFont, 
			command=self.quit 
			)
		self.quitButton.grid (
			row=rowx, 
			column=colx,
			sticky='N'+'W'
			)
			
		rowx += 1
		
#		self.askFilename = Button (

		self.askFilename = Button (
			self,
			text="Click here to find executable, or type it in below:",
			font=self.buttonFont,
			command=self.askfilename,
			)
		self.askFilename.grid (
			row=rowx,
			column=colx
			)
			
		
		rowx += 1
		
		self.filenm=StringVar()
		self.Filename = Entry (
			self,
#			textvariable=self.filenm
			textvariable=self.filenm
		)
		print "\n\n self.filenm = ",self.filenm
		
		self.Filename.grid (
			row=rowx,
			column=colx
		)
		self.Filename.bind ( 
			"<KeyPress-Return>", 
			self.returnEvent1 
		)		
			
			        #-- 1 --
        # [ self              :=  self with a new Label to label the
        #                         computer name field
        #   self._entryLabel  :=  that widget ]
#		self._entryLabel  =  Label ( 
#			self, 
#			text="Enter a computer's hostname:" 
#			)
#		self._entryLabel.grid ( 
#			row=4, 
#			sticky=W 
#			)
			
#-- 2 --
# [ self  :=  self with a new ComputerNamePicker set up so that
#             any valid computer name selection tells
#             self._colorA to pick that computer ]
		self._computerNamePicker  =  ComputerNamePicker ( 
			self, 
#			self._nameHandler 
		)
		self._computerNamePicker.grid ( 
			row=10, 
			column=0,
			padx="0.1i", 
			pady="0.1i" 
		)

			
			# ASKFILENAME widget
	#-- 5 --
	# [ self := self with a new fileName added
	#
		self._fileName	=  FileName ()
		self._fileName.grid (
			row=5,
			column=0,
			sticky=W
			)

	def quit(self):
		ans=askokcancel('Verify exit', "Really quit?")
		if ans: 
			print "\n >> PYEXEC exiting << \n\n"
			Frame.quit(self)
# print here: time()
#			sys.exit()
		
# get filename using local window manager
	def askfilename(self):				
		self.filenm = askopenfilename()
		
# - - -   _ n a m e H a n d l e r   - - -

	def _nameHandler ( self, color ):
		self._colorAdjuster.set ( color )
		
		# RETURN key handler
	def returnEvent1 ( self, event ):
		"""
		Handler for the Return key inside self.readout.
		"""
		try:
			self.filenm.set()
		except ValueError, detail:
			print "\n================================"
			print "\nThat's not a string!\n\n", detail
	
#----------

#================================================================

class FileName(Frame):

	"""
	Choose an executable file from the local directories
	"""
        #-- 1 --
        # [ master  :=  master with a new, empty Frame
        #   self    :=  that frame ]
	def __init__ (self):
#	        Frame.__init__ ( self, master )
		Frame.__init__ ( self )
#		self._createWidgets()

# - - createWidgets --
#	def _createWidgets(self):

#        	self.b1=Button(self, text="Get a file name", command=self.get)
		self.b1=Button(
			self, 
			text="Get a file name", 
			command=lambda: askopenfilename() 
		)
		self.b1.grid(
			row=2,
			column=2
		)
	def get(self):
		self.filenm = askopenfilename()

#================================================================

class ComputerNamePicker ( Frame ):
	""" 
	A widget for picking computers by name.  Contains:
          - A text entry field for typing an arbitrary computer name.
          - A scrollable listbox containing known computer names. 
        Exports:
            ComputerNamePicker ( master, callback )
                [ if (master is a widget) and (callback is a function) ->
                    master  :=  master with our widgets inside it
                                in a frame, so that on any event
                                that selects a valid computer, we call
                                  callback ( c )
                                where c is a Computer object representing the
                                computer picked ]

        Widget hierarchy [and grid coordinates]:
            ._entryLabel:  Label for color name entry field [0,0]
            ._entry:  Color name entry field [1,0]
            ._pickLabel:  Label for the color pick list [2,0]
            ._pickList:  A ColorPickList object [3,0]
        State and invariants:
            ._callback:  The callback function to be called when
                the user picks a valid computer
            ._entryVar:  a StringVar linked to the computer name
                entry field
	"""

#--
# Manifest constants
#--
	NAME_WIDTH = 20     # Width of a name in characters


# - - -   _ _ i n i t _ _   - - -

	def __init__ ( self, master ):    #, callback):
        #-- 1 --
        # [ master  :=  master with a new, empty Frame
        #   self    :=  that frame ]
		Frame.__init__ ( self, master )

        #-- 2 --
#		self._callback  =  callback
		self._entryVar  =  StringVar()

        #-- 3 --
        # [ self  :=  self with all widgets created and gridded ]
		self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

	def _createWidgets ( self ):
		""" 
			[ self  :=  self with all widgets created and gridded
		"""

        #-- 1 --
        # [ self              :=  self with a new Label to label the
        #                         computer name field
        #   self._entryLabel  :=  that widget ]
		self._entryLabel  =  Label ( 
			self, 
			text="Enter a computer's hostname:" 
		)
		self._entryLabel.grid ( 
			row=0, 
			sticky=W 
		)

        #-- 2 --
        # [ self         :=  self with a new Entry, with Enter bound to
        #                    a routine that will call self._callback
        #                    when a valid color is entered
        #   self._entry  :=  that widget ]
		self._entry   =  Entry ( 
			self, 
			relief=SUNKEN,
			width=self.NAME_WIDTH,
			textvariable=self._entryVar 
		)
		self._entry.grid ( 
			row=1, 
			sticky=W 
		)
		self._entry.bind ( 
			"<Key-Return>", 
			self._entryHandler 
		)

        #-- 3 --
        # [ self             :=  self with a new Label to label the color
        #                        pick list
        #   self._pickLabel  :=  that widget ]
		self._pickLabel  =  Label ( 
			self,
			text="Or double-click on a computer name:" 
		)
		self._pickLabel.grid ( 
			row=2, 
			sticky=W 
		)

        #-- 4 --
        # [ self            :=  self with a new ColorPickList widget,
        #                       with its callback set up to call self._callback
        #                       when a color is picked
        #   self._pickList  :=  that widget ]
		self._pickList  =  ComputerPickList ( 
			self,
			callback=self._pickListHandler 
		)
		self._pickList.grid ( 
			row=3, 
			sticky=W 
		)


# - - -   _ e n t r y H a n d l e r   - - -

	def _entryHandler ( self, event ):
		""" 
	[ if event is an event in self._entry ->
                if self._entryVar is a valid color name ->
                    call self._callback ( a Color representing that name )
                else ->
                    pop up a dialog box to tell the user self._entryVar
                    is not valid ]
		"""
		self._setByName ( 
			self._entryVar.get() 
		)


# - - -   _ s e t B y N a m e   - - -

	def _setByName ( self, computerName ):
		""" 
			[ if computerName is a string ->
                if computerName is a valid computer name in self's window ->
                  call self._callback ( a computer representing that name )
                  return 1
                else ->
                  pop up a dialog box to tell the user (computerName)
                    is not valid
                  return 0 ]
		"""

        #-- 1 --
        # [ if computerName is a valid X color name in self's window ->
        #     rgb  :=  a tuple ( r, g, b ) representing that color,
        #              where each value is an integer in [0,65535]
        #   else ->
        #     pop up a dialog box to tell the user (computerName)
        #       is not valid
        #     return 0 ]
		try:
			rgb = Misc.winfo_rgb ( 
				self, 
				computerName 
			)
		except:
			d = Dialog ( 
				self, 
				title="Message", 
				bitmap="info",
				text="Computer `" + computerName + "' is not defined.",
# First button is the default
				default=0,   
# Only one button: OK 
				strings=("OK",) 
			) 
		return 0

        #-- 2 --
        # [ if rgb is a tuple ( r, g, b ) representing a color in the RGB
        #   model, where each value is an integer in [0,65535] ->
        #     call self._callback ( c ) where c is a Color object
        #       representing rgb ]
		self._callback ( Color 
			( 
				( 
					self._scale16 ( rgb[0] ),
					self._scale16 ( rgb[1] ),
					self._scale16 ( rgb[2] ) 
				) 
			) 
		)


# - - -   _ s c a l e 1 6   - - -

	def _scale16 ( self, color16 ):
		""" 
			Takes an integer color value in the range [0,65535]
			and normalizes it to a float in [0.0, 1.0].
        """
		return float ( color16 ) / 65535.0


# - - -   _ p i c k L i s t H a n d l e r   - - -

	def _pickListHandler ( self, color ):
		""" 
			[ if color is a Color object ->
			call self._callback ( a Color representing computerName ) ]
		"""
		self._callback ( color )


#================================================================

class ComputerPickList ( Frame ):
	""" 
		A widget for selecting standard X window colors.
        A frame containing a Listbox with color names and an
        associated vertical Scrollbar.

        Exports:
            ColorPickList ( master, callback )
                [ if (master is a widget) and (callback is a function) ->
                    master  :=  master with our widgets in a frame, so that
                                on any event that selects a valid color,
                                we call
                                  callback ( c )
                                where c is a Color object representing
                                that color ]

        Widget hierarchy [and grid coordinates]:
            ._names:  The Listbox containing the color names [0,0]
            ._scroll:  The Scrollbar for scrolling the listbox [0,1]
        State and invariants:
            ._callback:  The callback function
            ._colors:  A list of Color objects such that ._colors[i]
                       represents the color from the (i)th name in ._names
	"""

    #--
    # Manifest constants
    #--
# Computer-names file
#    COMPUTER_NAMES_FILE = "/home/dwbarne/Disk12/Python_projects/Pyexec/computer_names.txt"
#	COMPUTER_NAMES_FILE = "d:/Python_projects/Pyexec/computer_names.txt"
	if os.environ['OS'] == 'Windows_NT':
		COMPUTER_NAMES_FILE = os.getcwd() + "\computer_names.txt"
	else:
		COMPUTER_NAMES_FILE = os.getcwd() + "/computer_names.txt"
		
	print ("Computer_names_file location: " + COMPUTER_NAMES_FILE)


# Width of the Listbox in characters
	NAME_WIDTH = 20 
# Number of lines in the Listbox
	NAME_LINES = 10


# - - -   _ _ i n i t _ _   - - -

	def __init__ ( self, master, callback ):
        #-- 1 --
        # [ master  :=  master with a new Frame
        #   self    :=  that Frame ]
		Frame.__init__ ( self, master )

        #-- 2 --
		self._callback  =  callback

        #-- 3 --
        # [ self  :=  self with all widgets created and gridded ]
		self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

	def _createWidgets ( self ):
		""" 
			[ self  :=  self with all widgets created and gridded ]
		"""

        #-- 1 --
        # [ self          :=  self with a new Scrollbar
        #   self._scroll  :=  that Scrollbar ]
		self._scroll  =  Scrollbar ( 
			self, 
			orient=VERTICAL 
		)
		self._scroll.grid ( 
			row=0, 
			column=1, 
			sticky=N+E+S 
		)

        #-- 2 --
        # [ self         :=  self with a new Listbox, scrolled by
        #                    self._scroll, with single-click events on the
        #                    (i)th name bound to a method that calls
        #                    self._callback(c) where c is self._colors(i) 
        #   self._names  :=  that Listbox ]
		self._names  =  Listbox ( 
			self, 
			width=self.NAME_WIDTH,
			height=self.NAME_LINES, 
			relief=SUNKEN,
			borderwidth=2, 
			exportselection=0,
			yscrollcommand=self._scroll.set 
		)
		self._names.grid ( 
			row=0, 
			column=0, 
			sticky=N+W+S 
		)
		self._names.bind ( 
			"<Double-Button-1>", 
			self._pickHandler 
		)
		self._scroll["command"] = self._names.yview

        #-- 3 --
        # [ self._names   :=  self._names with all color names from 
        #                     self.COLOR_NAMES_FILE inserted in the order
        #                     they occur in the file, except for names with
        #                     embedded blanks
        #   self._colors  :=  a list of Color objects representing those
        #                     names in the same order ]
		self._readComputerNames ( )


# - - -   _ p i c k H a n d l e r   - - -

	def _pickHandler ( self, event ):
		""" 
			[ if event is an event in self._names ->
                call self._callback(c) where c is the self._colors(i)
                  and i is the index of the selected name ]
		"""
# An Index tuple
#		current = self._names.curselection()  
		print " >> I am in __pickHandler "
		print computerList
		lineno = int(self._names.curselection()[0])
		current=computerList[lineno]
		print " >>> Current = ",current
# Ignore when empty
		if  len(current) > 0:  
			i   =  string.atoi ( current[0] )
			self._callback ( self._colors[i] )


# - - -   _ r e a d C o m p u t e r N a m e s   - - -

	def _readComputerNames ( self ):
		""" 
		[ if self.COMPUTER_NAMES_FILE names a readable file in which
              "!" is the comment character and lines have the format
              "r g b name" where r, g, and b are red, green and blue
              values in [0,255] and the name may have embedded blanks ->
                self._names   :=  self._names with all color names from 
                                  self.COLOR_NAMES_FILE inserted in the order
                                  they occur in the file, except for names with
                                  embedded blanks
                self._colors  :=  a list of Color objects representing those
                                  names in the same order ]
		"""

        #-- 1 --
		self._computers  =  []
		computerList = []

        #-- 2 --
        # [ if self.COMPUTER_NAMES_FILE can be opened for reading ->
        #     computerFile  :=  that file so opened
        #   else ->
        #     stdout  ||:=  message about unavailable file
        #     return ]
		try:
			computerFile = open ( self.COMPUTER_NAMES_FILE )
			print ("  \nOpened computer-names file: " + 
				self.COMPUTER_NAMES_FILE + 
				"\n\n"
			)
		except:
			print ( 
				"\n\n" +
				"*** Can't open the standard computer-names file: " +
				self.COMPUTER_NAMES_FILE + 
				" \n\n" 
			)
#			return
			sys.exit()
			
        #-- 3 --
        # [ colorList  :=  a list of the lines from colorFile ]
		global computerList
		computerList  =  computerFile.readlines()
		for line in computerList:
			print "computerList is " + line
		computerFile.close()

        #-- 4 --
        # [ self._colors  ||:=  a Color object representing each line from
        #                       colorList that doesn't start with "!",
        #                       where the format of the line is "r g b name",
        #                       ignoring names with embedded blanks, and
        #                       the (r,g,b) values are in [0,255] ]
		for line in computerList:
            #-- 4 body --
            # [ if line starts with "!" or doesn't have 4 fields -> I
            #   else ->
            #     self._colors  ||:=  a Color whose (r,g,b) values are
            #                         taken from the first three fields
            #                         of line, integers in [0,255]
            #     self._names   ||:=  the fourth field from line ]
			if line[0] != "!":  # Ignore comment lines

                #-- 4.1 --
                # [ fields  :=  a list of the whitespace-delimited fields
                #               from line ]
				fields = string.split ( line )      

                #-- 4.2 --
                # [ if fields has 4 elements ->
                #     self._colors  ||:=  a Color whose (r,g,b) values are
                #                         taken from fields[0:2], integers
                #                         in [0,255]
                #     self._names   ||:=  fields[3]
                #   else -> I ]
#				if len(fields) == 4:
                #if len(fields) == 1:
				self._computers.append ( self._rgbScale ( fields ) )
				self._names.insert ( 
						END, 
						fields[0] 
					)


# - - -   _ r g b S c a l e   - - -

	def _rgbScale ( self, fields ):
		"""
			[ if fields is a sequence of at least three strings
              representing integers in [0,255] ->
                return a Color object using fields[0:2] as the RGB
                  values
		"""
		return fields[0]
#		return Color ( 
#			( 
#				string.atof ( fields[0] ) / 255.0,
#				string.atof ( fields[1] ) / 255.0,
#				string.atof ( fields[2] ) / 255.0 
#			) 
#		)

		#================================================================

class ColorAdjuster ( Frame ):
	""" A widget that allows the user to select a color model,
        and displays and allows the user to adjust a color.

        Exports:
            ColorAdjuster ( master, callback )
                [ if (master is a widget) and (callback is a function) ->
                    master  :=  master with a new ColorAdjuster widget,
                                set up so that any color change due to
                                explicit .set() or user events calls
                                  callback(c)
                                where c is a Color widget representing the
                                new color ]
            .set ( color ):
                [ if (color is a Color object) ->
                    display (color) in self's sliders
                    call self's callback with (color) ]
            .get ( ):
                [ returns a Color object representing self's current color ]

        Widget hierarchy [and grid coordinates]:
            ._radioLabel:  Label for radiobuttons [0,0]
            ._radioFrame:  Frame for radiobuttons [1,0]
                ._radios:  A list of radiobuttons, one per color model
            ._slidersLabel:  Label for the NumProcs widget [2,0]
            ._sliders:  A NumProcs widget [3,0]

        State and invariants:
            ._callback:  Our callback function
            ._models:  A list of ColorModel objects such that
                       self._radios[i] selects self._models[i]
            ._modelx:  An IntVar linked to self._radios
            ._radios: A list of radiobuttons, one per color model
	"""

	def __init__ ( self, master, callback ):
        #-- 1 --
        # [ master  :=  master with a new Frame inserted
        #   self    :=  that Frame ]
		Frame.__init__ ( self, master )

        #-- 2 --
        # [ self._callback  :=  callback
        #   self._models    :=  a list of one or more ColorModel objects
        #   self._modelx    :=  an IntVar set to 0 ]
		self._callback  =  callback
		self._models    =  []
		self._models.append ( HSV_Model ( ) )
		self._models.append ( RGB_Model ( ) )
		self._models.append ( CMY_Model ( ) )
		self._modelx   =  IntVar ( )
		self._modelx.set ( 0 )

        #-- 3 --
        # [ self  :=  self with all widgets created and gridded ]
		self._createWidgets ( )


# - - -   _ c r e a t e W i d g e t s   - - -

	def _createWidgets ( self ):
		""" 
			[ self  :=  self with all widgets created and gridded ]
		"""

        #-- 1 --
        # [ self          :=  self with one or more new Radiobutton widgets,
        #                     one per element of self._models, such that the
        #                     Nth radiobutton sets self._modelx to N and has
        #                     a label derived from self._models[N], and each
        #                     radiobutton tells self._sliders when the
        #                     color model changes
        #   self._radios  :=  a list of those Radiobuttons in the same order ]
		self._radioLabel  =  Label ( 
			self, 
			text="Select job submission type :" 
		)
		self._radioLabel.grid ( 
			row=0, 
			sticky=W 
		)

		self._radioFrame  =  Frame ( 
			self, 
			relief=RIDGE, 
			borderwidth=4 
		)
		self._radioFrame.grid ( 
			row=1, 
			sticky=W, 
			padx="0.1i", 
			pady="0.1i" 
		)

		self._radios = []
		for i in xrange(len(self._models)):
			self._radios.append ( self._addRadioButton ( i ) )

        #-- 2 --
        # [ self                :=  self with a new Label to label the
        #                           NumProcs widget 
        #   self._slidersLabel  :=  that new Label ]
		self._slidersLabel = Label ( 
			self,
			text="Drag these sliders to change\nthe number of processors:\n" 
		)
		self._slidersLabel.grid ( 
			row=2, 
			sticky=W 
		)

        #-- 3 --
        # [ self           :=  self with a new NumProcs widget,
        #                      with its callback set to self._callback(),
        #                      and its color model the (self._modelx)th
        #                      element of self._models
        #   self._sliders  :=  that new widget ]
		self._sliders  =  NumProcs ( 
			self,
			self._models[self._modelx.get()],
			self._sliderChanged 
		)
		self._sliders.grid ( 
			row=3, 
			sticky=E+W 
		)


# - - -   _ s l i d e r C h a n g e d   - - -

	def _sliderChanged ( self, color ):
		self._callback ( color )


# - - -   _ a d d R a d i o B u t t o n   - - -

	def _addRadioButton ( self, n ):        
		"""
			[ if n is in range(len(self._models)) ->
              self  :=  self with a new Radiobutton widget
                        that sets self._modelx to (n) and has a label
                        derived from self._models[n], and set up to
                        tell self._sliders when the model changes
              return that new widget ]
		"""

        #-- 1 --
		model  =  self._models[n]

        #-- 2 --
        # [ text  :=  model.name + " (" + s1 + "-" + s2 + "-" + s3 + ")"
        #             where si is the (i)th slider name of model ]
		text   =  model.name() + " ("
		for i in xrange(3):
			if  i != 0:
				text = text + "-"
			text = text + model.sliderLabel(i)
		text  =  text + ")"

        #-- 3 --
        # [ self  :=  self with a new Radiobutton with variable=self._modelx,
        #             value=i, and text=text
        #   rb    :=  that new Radiobutton ]
		rb  =  Radiobutton ( 
			self._radioFrame, 
			variable=self._modelx, 
			value=n,
			text=text, 
			command=self._modelChanged, 
			anchor=W 
		)
		rb.grid ( 
			row=n, 
			sticky=W 
		)
		return rb


# - - -   _ m o d e l C h a n g e d - - -

	def _modelChanged ( self ):
		newModel  =  self._models [ self._modelx.get() ]
		self._sliders.setColorModel ( newModel )


# - - -   s e t   - - -

	def set ( self, color ):
		self._sliders.set ( color )
		self._callback ( color )


# - - -   g e t   - - -

	def get ( self ):
		return self._sliders.get()




#- - - main - - -
	
# instantiate Application class
runprog=Application()
runprog.master.title("PYEXEC: Sandia's job submission tool for clusters")
runprog.mainloop()
