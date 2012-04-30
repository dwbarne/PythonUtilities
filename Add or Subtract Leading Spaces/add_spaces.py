# filename: add_leading_spaces.py
# date of creation:
#     Oct 9, 2008

# purpose:
#   to add a specified number of spaces in
#   front of designated lines; these occur when
#   python code from one program is copied to
#   a module, for example, where the defs start in
#   column 1.

import os                   # to get current directory, etc.
import string               # filenames are strings, dude
from tkFileDialog import *  # for 'askopenfilename()', etc
import sys                  # for sys.exit()
from tkMessageBox import *  # askokcancel, showinfo, showerror, etc.

def say_goodbye():
    print '\nYou have elected to end this session.'
    print 'Program terminated\n\n'
    sys.exit()

currentDirectory = os.getcwd()

print '\n ** Welcome to "add_leading_spaces.py"'
print '\nThis program adds a user-specified amount'
print '   of leading spaces to each line of a code.'
print
print ' "Starting line" and "Ending line" are line numbers'
print '   as shown in any text editor.'
    
# define dictionary of options for askopenfilename(); open only python extensions initially
options = {}
options = {
    'defaultextension' : '',
    'filetypes' : [('All files','.*')],
#    'initialdir' : currentDirectory,
    'initialfile' : '',
#    'parent' : root,
    'title' : 'Open any text file...'
    }      
        
# get filename
#        dirname, filename = os.path.split(askopenfilename(**options))
inputFile = askopenfilename(**options)

file=open(inputFile,'rU').readlines()

print '\nInput file:',inputFile
lenFile=len(file)
print '\nInput file has %s lines.' % len(file)

lineStart=int(raw_input('\nStarting line: '))
lineEnd=int(raw_input('Ending line: '))
numSpaces=int(raw_input('Number of leading white spaces to add: '))

if lineStart > lineEnd:
    print '\nWARNING - "Ending line" cannot be less than "Starting line" '
    print '\n   Starting line =',lineStart
    print '   Ending line =',lineEnd

    print '     Check your input and start over.\n'
    sys.exit()
    
if lineStart > lenFile or lineEnd > lenFile:
    print '\nWARNING - Starting or Ending line numbers out of range'
    print '   Max line number:',lenFile
    print '   Starting line:',lineStart
    print '   Ending line:',lineEnd
    print '     Check your input and start over.\n'
    sys.exit()
    

ans = askokcancel(
    'start and end line numbers ok?',
    'File = ' + inputFile + '\n' +
    '\nStarting line = ' + str(lineStart) + '\n' + 
    'Ending line = ' + str(lineEnd) + '\n' + 
    'Leading white spaces to add per line = ' + str(numSpaces) + '\n\n' +
    'Is this ok?'
    )
    
if ans:
    diff = lineEnd - lineStart + 1
    print
    for i in range(diff):
        lineNumber=lineStart+i
        line = file[lineNumber-1]
        print '\nBefore change ...'
        print '%s. %s' % (lineNumber,line)
        if line[0] <> '#':
            lineNew=' '*numSpaces + line
            print ' After change ...'
            print '%s. %s' % (lineNumber,lineNew)
            file[lineNumber-1]=lineNew
        else:
            print ' Comment - no change'
        
# check if ok to write file back out to disk
    ans=askokcancel(
        'Write file...',
        'OK to write file out to disk?'
        )
        
    if ans:
        options={'title' : 'Save a file...'}
        outputFile=asksaveasfilename(**options)
        fileOut=open(outputFile,'w')
        fileOut.writelines(file)
        print '\nOutput file:',outputFile
        print '   successfully written!\n'
        print ' Program ended\n'
                
    else:
        say_goodbye()
    
else:
    say_goodbye()

