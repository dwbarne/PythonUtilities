# module_spawnprogram.py
# run a python program from this script
# runs on windows or *nix

import os                   # to get current directory, etc.
import string               # filenames are strings
from tkFileDialog import *  # for 'askopenfilename()', etc
from Tkinter import *       # to inherit from Frame
import sys                  # for sys.exit()

_DEBUG=False

# define globals
if os.name in ("nt", "dos"):
    exefile = ".exe"
    envWindows=1
    print '\n >> Environment: Windows\n'
else:
    envWindows=0
    exefile = ""
    print '\n >> Environment: *nix\n'
    
    
    
class Spawn(Frame):
    def __init__(self,parent):
        print '\n** class Spawn'
        Frame.__init__(self)
        self.frameParent=parent
        
        currentDirectory = os.getcwd().split('\\').pop()
        
        if _DEBUG:
            currentDirectoryFullPath = os.getcwd()
            print '\n ** Current directory (full path):\n' + '"' + \
                currentDirectoryFullPath + '"' 
        
# define dictionary of options
        options = {}
        options = {
            'defaultextension' : '.py',
            'filetypes' : [('python','.py'),('All files','.*')],
            'initialdir' : currentDirectory,
            'initialfile' : '',
            'parent' : self.frameParent ,
            'title' : 'Open a Python file only'
            }      
        
# get filename
#        dirname, filename = os.path.split(askopenfilename(**options))
        filename = str(askopenfilename(**options))
        
        if _DEBUG:
            print '\n    File opened:',filename
            
# if Windows, put double-quotes around filename so that it can be executed properly by spawn
        if envWindows:
            filename='"' + filename + '"'
        self.spawn("python", filename)
        print "\n....goodbye\n"
        

    def spawn(self, program, *args):    #*args is a tuple
    
        if _DEBUG:
            print '\n filename to run: %s\n' % args
        
        try:
# check if the os module provides a shortcut
            return os.spawnvp(program, (program,) + filename)
            
        except AttributeError:
            pass
# darn; it doesn't
        try:
            spawnv = os.spawnv
            
        except AttributeError:
# assume it's unix
            pid = os.fork()
            if not pid:
                os.execvp(program, (program,) + args)
            return os.wait()[0]
# must be windows
        else:
        
# got spawnv but no spawnp: go look for an executable
# ... construct a list of path names
            paths=string.split(os.environ["PATH"], os.pathsep)
# ... include current directory up front, just in case executable exists there
            paths.insert(0,'.')
# ... determine number of path names            
            length_paths=len(paths)
# ... use counter to see when at end
            icount=0
            
            for path in paths:
                icount+=1
                print '\n %s/%s. path = %s' % (icount,length_paths,path)
                print ' executable =',(program + exefile)
                file = os.path.join(path, program) + exefile
                print ' - checking whether executable exists in this path...'
                
                try:
# ... (file,) is a one-item tuple; the comma MUST be there!
                    spawnv(os.P_WAIT, file, (file,) + args )
                    return
                except os.error:
                    if icount == length_paths:
                        raise IOError, (
                            '\n>> ERROR: cannot find executable!\n' + 
                            '     executable: ' + program + exefile + '\n' + 
                            '     filename: ' + argsModified + '\n'
                            )
                        sys.exit()
                    else:
                        print ' No; try next path in list.\n'



if __name__ == '__main__':
    root=Tk()
    app=Spawn(root)

    
