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
		print computerName
		topLabel = Label (
			self,
			text=
				'SYSTEM DATA\n' +
				'-----------\n' +
				'Machine name: ' + computerName + '\n' +
				'User name: ' + userName + '\n'
				'OS: ' + operatingSystem + '\n'
				'Architecture: ' + processorArchitecture + '\n'
				'Processor: ' + processorIdentifier,
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
		
# Define top label		
#		self.topLabel = Label (
#			self, 
#			text='          You are currently running on XXX\n',
#			font=self.buttonFont
#			)
#			self.topLabel.grid(
#			row=rowx,
#			column=colx,
#			sticky='E')
# ??? causes code to hang
#		self.topLabel.pack()
		
#		rowx+=1
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
		
		self.askFilename = Button (
			self,
			text="Find executable, or just type it in",
			font=self.buttonFont,
			command=self.askfilename,
			)
		self.askFilename.grid (
			row=rowx,
			column=colx
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
				
#----------

#- - - main - - -
	
# instantiate Application class
runprog=Application()
runprog.master.title("PYEXEC: Sandia's job submission tool for clusters")
runprog.mainloop()
