#!/usr/bin/python
# filename: yaml_dump_variable_is_dict.py

import yaml

# -------- example: dictionaries and yaml ----------

# 'dictionaries', which can contain lists and other dictionaries in Python, look like
var = [0.9876,{
    'key1':'value1',
    'key2':'value2',
    'lines':['line 1','line 2','line 3','last line', float('Nan'),float('inf')],
    'subdict':{'subdict_key1':'subdict_value1','subdict_key2':'subdict_value2'}
    }
    ]
print 'var =\n',var

# what happens when we write the data using YAML?

print '\nExample 1: LISTS AND YAML'
print '\nvar = \n\n', var
print '\n\nWRITING (using yaml.dump) ...'
print '\nyaml.dump(var) =\n\n', yaml.dump(var)

# write to file
filepath='T:/Python - Projects/Yaml loads and dumps/codes/tempFile_variable_is_dict'
file=open(filepath,'w')
file.write(yaml.dump(var))
file.close()

# read from file
contents=open(filepath,'r').read()
yy = yaml.load(contents)
print '\nyaml.load(var) = ', yy

