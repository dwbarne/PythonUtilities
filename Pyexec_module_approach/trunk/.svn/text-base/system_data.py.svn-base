# class System_Data
# purpose: to write user-specified system data to the current Tkinter window
#author: Daniel Barnette, Sandia Labs, Albuquerque, NM 87185

# for gui:
from Tkinter import *
# for different fonts:
import tkFont
# to get platform name:
import os

class System_Data(Frame):
#	""" Application for running jobs on various clusters and supercomputers
#		at Sandia Labs.
#	"""

#
#	def __init__(self, master=None, parent=None):
	def __init__(self, master=None):
#		Frame.__init__(self, parent)
		Frame.__init__(self, master)
####		self.grid(row=rowx,col=colx)

# initialize row and column to place buttons		

		
# does not work:
# self.pack()
		print " This is class System_Data"
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

#			 define top label
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
			sticky='N'

			)

		print "NOW LEAVING CLASS SYSTEM_DATA...\n"
		
if __name__=='__main__': 
	System_Data(0,0).mainloop()
