# define a name:callback demos table

from tkFileDialog	import askopenfilename
from tkColorChooser	import askcolor
from tkMessageBox	import askquestion, showerror
from tkSimpleDialog	import askfloat

demos={
	'Open File': 	askopenfilename,
	'Color':	askcolor,
	'Query':	lambda: askquestion('Warning', 'You typed "rm *" \nConfirm?'),
	'Error': 	lambda: showerror('Error!', "He's dead, Jim"),
	'Input': 	lambda: askfloat('Entry', 'Enter credit card number')

}


