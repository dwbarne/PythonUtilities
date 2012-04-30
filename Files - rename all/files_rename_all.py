# list of files only, not directories, for 
#  purposes of renaming all files

# Ref:
# "Python Phrasebook," p. 80ff

import os
import time
import sys

#cwd="c:\documents and settings\dwbarne"
cwd=os.getcwd()
os.chdir(cwd)

# get list of files
files=os.listdir('.')

def dump(file_tuple):
    mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime = file_tuple
    print " -size:", size, "bytes"
    print " -owner:", uid,gid
    print " -created:", time.ctime(ctime)
    print " -last accessed:", time.ctime(atime)
    print " -last modified:", time.ctime(mtime)
    print " -mode:", oct(mode)
    print " -inode/dev:", ino, dev
   
# get stats for each file

filelist=[]
basename=[]
extension=[]
filenameExtension = []
for file in files:
# for directories
#    if os.path.isdir(file):
# for files
    if os.path.isfile(file):
        file_tuple=os.stat(file)
        print "Stats for file:",file
        dump(file_tuple)
        filelist.append(file)
        basename.append(os.path.basename(file))
        extension.append(os.path.splitext(file))
        print
print
print '-'*50
print 
icount=0       
# print list of files
print " *** List of files:"
for file in filelist:
    icount+=1
    filename_main, filename_ext = extension[icount-1]
    filenameExtension.append(filename_ext)
#    print "%s. %s, basename = %s, extension = %s" % (icount,file,basename[icount-1],filename_ext)
    print "%s. %s, basename = %s, extension = %s" % (icount,file,filename_main,filename_ext)
    
print
print
print " *** Sorted basenames:"
basename.sort()
for number,name in enumerate(basename):
    print number+1, name
    
print
print
dictFilenameExtensions = {}
print " *** Sorted extensions:"
filenameExtension.sort()
for number,ext in enumerate(filenameExtension):
    print number+1, ext
    dictFilenameExtensions[ext] = None
    
print
print
print " *** Unique extensions:"
icount = 0
for ext,value in dictFilenameExtensions.iteritems():
    icount += 1
    print icount, ext
    
# add the following extension to all files
print
print
answer = raw_input("Hit 'y' to add 'temp' to end of filenames: ",)
if answer <> 'y':
    print
    print ' --- END ---'
    sys.exit()
print " *** New filenames"
extAdd = '.temp'
for file in filelist:
    filenameNew = file + extAdd
    os.rename(file,filenameNew)
# get list of files, now with new names
files=os.listdir('.')
for number,file in enumerate(files):
    print number+1,file
print
        
print " -- END --"

