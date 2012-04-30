#! /usr/bin/python
# Home directory for this file:
#  T:\Python - Projects\Files - find and list\find_file.py
#
# a copy is also located in the C:\ directory

import sys, os   # imports all the functions in the os module (operating system functions)
cwd = os.getcwd()   # gets the current working directory and places it in the variable cwd
print "Enter file to search for: "
file2find = str(raw_input("__> "))
print(' -- file2find = %s' % file2find)
if file2find=="":
    sys.exit()
dirFiles = open( "filelist.txt","w")  # creates the file filelist.txt ready for writing using the variable dirFiles

# the walk function returns the current directory in root, the directories in dirs
# and the files in root in files. By using the for loop it traverses every folder
# from the starting folder.
c=0  #Count the files found!
for root, dirs, files in os.walk(cwd):
#    dirFiles.write(root + "\n")   # writes to dirFiles.txt the current directory name
    i=0   #file count for directory to save directory path if found!
    for theFiles in files:      # will iterate all the files in the current directory
        if file2find in theFiles:
            i+=1
            c+=1
            if i==1:
                dirFiles.write('\n' + root + '\n')   # writes to dirFiles.txt the current directory name
            dirFiles.write( "___________ " + theFiles + "\n") # writes the filename to dirlist.txt. 
dirFiles.close() # Cleanly saves and closes the file dirlist.txt
# Note: the "\n" in the write lines adds the newline character so that the next write starts on a newline
