#!/usr/bin/env python

# for gui:
from Tkinter import *

# for system calls, such as exit:
import sys

# for different fonts:
import tkFont

# for dates and such:
from time import *

# to get platform name:
import os

# Import other vital modules
# import	sys, string, math 

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
		rowx=2
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
			



#- - - main - - -
	
# instantiate Application class
runprog=Application()
runprog.master.title("SYSTEM INFO FOR CURRENT COMPUTER")
runprog.mainloop()
