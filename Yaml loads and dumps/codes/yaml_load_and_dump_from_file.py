import yaml
import tkFileDialog
from tkMessageBox import *  # askokcancel, showinfo, showerror, etc

# define dictionary of options for askopenfilename()
options = {}
options = {
    'defaultextension' : '.yaml',
    'filetypes' : [('YAML files','.yaml'),('All files','*')],
    'initialdir' : '.',
    'initialfile' : '',
#    'parent' : '',
    'title' : 'Read and Write YAML file'
    } 
# get input filename first    
inputFileName = tkFileDialog.askopenfilename(**options)
if inputFileName == '':
    print '   No filename chosen!'
    showinfo(
    '\nNo filename chosen...',
    'You must enter a filename.\n\n'
    )
    sys.exit()
# open the file as one big string
inputFile = open(inputFileName,'r').read()
# load into YAML    
#print yaml.dump(yaml.load(inputFile)
try:
    y1 = yaml.load(inputFile)
except:
    stringYamlLoadError = (
        'Data in column %s does not appear to be in\n' + 
        'typical YAML format.\n\n' +
        'Choose another column and try again.'
        )
    print stringYamlLoadError
    showinfo(
        'Error: not YAML format',
        stringYamlLoadError
        )
    sys.exit()
print 'file contents:\n',inputFile
print '\nyaml.load(inputFile) =',y1
print '\nyaml.dump(y1) =\n', yaml.dump(y1)
print '\ntype(y1) =',type(y1)
print
print '\ny1.keys() =\n',y1.keys()


