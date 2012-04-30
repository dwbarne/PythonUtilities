# read (key, value) pairs from dictionaries within dictionaries
# April 22, 2010
import yaml
from tkMessageBox import *      # dialogs such as askokcancel, showinfo, showerror, etc.
import tkFileDialog             # for askopenfilename
import sys                      # for sys.exit()
import os                       # check for file

# Globals
DEBUG = 0                       # set to 0 to supress detailed print statements

class ParseYamlFile():
    def __init__(self,inputObject):
        
        print '\n os.path.isfile(inputObject) =',os.path.isfile(inputFileName)
# if file, open; if not, assume inputObject is a yaml.dump() object of some kind to be read directly by yaml.load()
        if os.path.isfile(inputObject):      
# open the file as one big string
            try:
                inputYamlLoad = open(inputObject,'r').read()
            except:
                stringReadFileError = (
                    'Cannot open file "%s"\n\n' +
                    'Some reasons might be:\n' +
                    '  - contents of file are corrupted\n' +
                    '  - you may not have proper permissions set\n' +
                    '  - contents of file are not readable\n\n' +
                    'As a result, this option will not be executed.'
                    )
                print stringReadFileError
                showinf(
                    'Error: cannot open file',
                    stringReadFileError
                    )
                return
        else:
            inputYamlLoad = inputObject
            
# load into YAML    
#print yaml.dump(yaml.load(inputFile)
        try:
            objectYaml = yaml.load(inputYamlLoad)
        except:
            stringYamlLoadError = (
                'Content does not appear to be in\n' + 
                'typical YAML format.\n\n' +
                'Select different content and try again.'
                )
            print stringYamlLoadError
            showinfo(
                'Error: not YAML format',
                stringYamlLoadError
                )
            return
            
        if DEBUG:
            print 'object contents: inputYamlLoad =\n',inputYamlLoad
            print '\nyaml.load(inputYamlLoad) =',objectYaml

        d1 = objectYaml
        
        if DEBUG:
            print
            print ' **** dict_within_dict ****'
            print
            print 'd1 =\n',d1
            print 'len(d1) =',len(d1)
            print 
            print 'yaml.dump(d1) =\n',yaml.dump(d1)
            print
            
        try:
            dump = yaml.dump(d1)
        except:
            stringYamlDumpError = (
                'Content cannot be output in\n' + 
                'typical YAML format.\n\n' +
                'Select different content and try again.'
                )
            print stringYamlLoadError
            showinfo(
                'Error: not YAML format',
                stringYamlLoadError
                )
            return
        
        if DEBUG:
            print 'type(dump) =',type(dump)
            print
            print 'len(dump) =',len(dump)
            print
            print 'dump =\n',dump
            print

            for (k,v) in d1.iteritems():
                print 'key, value = %s : %s' % (k,v)
                try:
                    print '   len(value) =',len(v)
                except:
                    print '   len(value) = 0'
    
            print 
            print '----- keys, values, lens -----'
            print

            print 'd1.keys()[0] =',d1.keys()[0]
            print 'd1.values()[0] =',d1.values()[0]
            try:
                len0 = len(d1.values()[0])
                print 'len(d1.values()[0]) =',len0
#    if (len(d1.values()[0])) >= 1:
                print 'len(d1.values()[0].values()[0] =',len(d1.values()[0].values()[0])
            except:
                print 'len(d1.values()[0]) = 0'
#            if (len(d1.values()[0])) >= 1:
#                print 'len(d1.values()[0].values()[0]) =',len(d1.values()[0].values()[0])
            print '------------------------------------'

            print 'd1.keys()[1] =',d1.keys()[1]
            print 'd1.values()[1] =',d1.values()[1]
            try:
                len1 = len(d1.values()[1])
                print 'len(d1.values()[1]) =',len1
            except:
                print 'len(d1.values()[1]) = 0'
            print '------------------------------------'
    
            print 'd1.keys()[2] =',d1.keys()[2]
            print 'd1.values()[2] =',d1.values()[2]
            try:
                len2 = len(d1.values()[2])
                print 'len(d1.values()[2]) =',len2
            except:
                print 'len(d1.values()[2]) = 0'
            print '------------------------------------'
        
            print
            print ' creating list of items in d1'
            print
            
        l1=d1.items()
        
        if DEBUG:
            print 'l1 =\n',l1
            print
            print 'len(l1) =',len(l1)
            print
        
# empty lists
        listAllItems = []
        listTemp = []
# initialize counter
        icount=1
        flagSlice = 0
# 3-level extractor for (key,value) dictionary pairs, meaning it can handle
#    dictionaries within dictionaries within dictionaries
#    Final entry will be a list of lists, not a list of tuples which is what *.items() produces
# ... this is the heart of this module
        for item in l1:
            if DEBUG:
                print '%s. item = %s' % (icount,item)
            if type(item[1]) == dict:
                string1 = item[0]
                l2=item[1].items()
                if DEBUG:
                    print '  l2 =',l2
                for subItem_1 in l2:
                    if DEBUG:
                        print '%sa.    subItem_1 = %s' % (icount, subItem_1)
                    if type(subItem_1[1]) == dict:
                        string2 = subItem_1[0]
                        l3=subItem_1[1].items()
                        if DEBUG:
                            print '  l3 =',l3
                        for subItem_2 in l3:
                            if DEBUG:
                                print '%sb.         subItem_2 = %s' % (icount, subItem_2) 
#                            listAllItems.append(subItem_2 + ',' + type(subItem_2[1]))
                            listTemp = [((string1 + '_' + string2 + '_' + subItem_2[0]).replace(' ','-')).lower()]
                            if len(listTemp) > 64:
                                print
                                print 'BEFORE: listTemp =',listTemp
                                listTemp = listTemp[:64]
                                print 'AFTER: listTemp =',listTemp
                                print
                                flagSlice = 1
                            listTemp.append(subItem_2[1])
                            mySqlType = self.typeIt(subItem_2[1])
                            listTemp.append(mySqlType)
                            listAllItems.append(listTemp)
                            listTemp = []
#                        break
                        continue
                    else:
#                        listAllItems.append(subItem_1 + ',' + type(subItem_1[1]))
                        listTemp = [((string1 + '_' + subItem_1[0]).replace(' ','-')).lower()]
                        if len(listTemp) > 64:
                            print
                            print 'BEFORE: listTemp =',listTemp
                            listTemp = listTemp[:64]
                            print 'AFTER: listTemp =',listTemp
                            print
                            flagSlice = 1
                        listTemp.append(subItem_1[1])
                        mySqlDataType = self.typeIt(subItem_1[1])
                        listTemp.append(mySqlDataType)
                        listAllItems.append(listTemp)
                        listTemp = []
                        continue
            else:
                listTemp = [((item[0]).replace(' ','-')).lower()]
                if len(listTemp) > 64:
                    print
                    print 'BEFORE: listTemp =',listTemp
                    listTemp = listTemp[:64]
                    print 'AFTER: listTemp =',listTemp
                    print
                    flagSlice = 1
                listTemp.append(item[1])
                mySqlDataType = self.typeIt(item[1])
                listTemp.append(mySqlDataType)
                listAllItems.append(listTemp)
                listTemp = []
                
            icount += 1
            

# sort alphabetically
        listAllItems.sort()
        if DEBUG:
            print
            print ' final item list:'
            print
            print 'listAllItems =\n',listAllItems
            print
            print 'len(listAllItems) =',len(listAllItems)
        print
        print 'Alphabetized printout of list:'
        icount = 1
        for item in listAllItems:
            print '%s. %s' % (icount, item)
            icount += 1
        print
        if flagSlice:
            stringSlice = (
                'FYI: At least one of the column names has been\n' +
                'shortened to 64 characters, as this is the maximum\n' +
                'name length allowed by MySQL'
                )
            print stringSlice
            print
            showinfo(
                'INFO: at least one name shortened',
                stringSlice
                )
                
        print '\n**** yaml data preparation finished ****'
        
    def typeIt(self, var):
        '''
        Purpose:
            determine type of the variable and assign a string that can be understood by MySQL
        '''
        if type(var) == int:
            return 'INTEGER(10)'
        elif type(var) == str:
            return 'CHAR(200)'
        elif type(var) == float:
            return 'FLOAT'
        elif type(var) == bool:
            return 'BOOL'
        else:
            stringTypeError = (
                (
                'The datatype of the variable,\n\n%s\n\n' +
                'has not been found in the current list of options.\n\n' +
                'Modify this module (extract.py) to provide for this datatype.\n\n'
                )
                % (type(var))
                )
            print stringTypeError
            showinfo(
                'Error: datatype not found',
                stringTypeError
                )
            return
            
                
            
    
if __name__ == '__main__':
# created from yaml.load command
    outputYaml={'one':1, 'two':2, 'three':{'sons':{'son1':'travis', 'son2':'trevor', 'son3':'taylor'}}}
# or can load from a file
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
#    app = ParseYamlFile(outputYaml)
    app = ParseYamlFile(inputFileName)