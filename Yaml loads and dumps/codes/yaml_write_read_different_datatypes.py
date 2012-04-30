#!/usr/bin/python
# filename: yaml_write_read_different_datatypes.py

import yaml

# -------- example: values, lists, and dictionaries and yaml ----------

# 'dictionaries', which can contain values, lists, and other dictionaries in Python, look like
var = [
# values
    0.9876,
    1.2345,
# list    
    ['list_element1','list_element2','list_element3'],
# dictionaries with embedded list and dictionaries
    {
    'key0':'value0',
    'key1':'value1',
    'lines':['line 0','line 1','line 2','last line'],
    'subdict0':{'subdict0_key0':'subdict0_value0','subdict0_key1':'subdict0_value1'},
    'subdict1':{
      'subdict1_key0':{'subdict2_key0':'subdict2_value0','subdict2_key1':'subdict2_value1'},
      'subdict1_key1':'subdict1_value1',
      'subdict1_key2':'subdict1_value2'
               }  
    }
    ]
print 'var =\n',var

# what happens when we write the data using YAML?

print '\n\nWRITING var to file outFile.dat (using yaml.dump(var)) ...'
# write to file
filepath = 'T:/Python - Projects/Yaml loads and dumps/codes/outFile.dat'
file = open(filepath,'w')
file.write(yaml.dump(var))
file.close()

# read from file
print '\n\nREADING var from file outFile.dat, then load into yaml.load()'
fileContents = open(filepath,'r').read()
yl = yaml.load(fileContents)
print '\nyaml.load(var):\n', yl
print ''
print ' -- END --'

'''
File outFile.dat looks like:

- 0.98760000000000003
- 1.2344999999999999
- [list_element1, list_element2, list_element3]
- key0: value0
  key1: value1
  lines: [line 0, line 1, line 2, last line]
  subdict0: {subdict0_key0: subdict0_value0, subdict0_key1: subdict0_value1}
  subdict1:
    subdict1_key0: {subdict2_key0: subdict2_value0, subdict2_key1: subdict2_value1}
    subdict1_key1: subdict1_value1
    subdict1_key2: subdict1_value2
    
'''

