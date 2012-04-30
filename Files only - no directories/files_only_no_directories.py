# list of files only, not directories

# Ref:
# "Python Phrasebook," p. 80ff

import os
import time

cwd="c:\documents and settings\dwbarne"
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
#    print "%s. %s, basename = %s, extension = %s" % (icount,file,basename[icount-1],filename_ext)
    print "%s. %s, basename = %s, extension = %s" % (icount,file,filename_main,filename_ext)
    
print " -- END --"

