#!/usr/bin/python

import yaml

# -------- example 1. variables and yaml ----------

# 'Variables' in Python look like
#  var1 = 40.3388

# define some variables
var = """
var1: 40.3388
"""

# what happens when we read the data using YAML?

print '\nExample 1: VARIABLES AND YAML'
print '\nREADING (yaml.load) ...'
y1=yaml.load(var)
print '\nOriginal variable look like:\n\n',var
print '\nAfter loading, yaml.load(var) looks like:\n\n',y1
print '\nDatatype of loaded object:\n\n',type(y1)

# now what happens when we dump the data using YAML?

print '\n\nWRITING (yaml.dump) ...'
print '\nyaml.dump(var) =\n\n', yaml.dump(y1)

print ''
print '=========='
print ''

# -------- example 2. lists and yaml ----------

# A "list" in Python looks like this:
#  list = ['Hesperiidae','Papilionidae','Apatelodidae','Epiplemidae']

# define a list that has been written out by YAML
list1 = """
 - Hesperiidae
 - Papilionidae
 - Apatelodidae
 - Epiplemidae
"""

# what happens when we read the data using YAML?

print 'Example 2: LISTS AND YAML'
print '\nREADING (yaml.load) ...'
y2=yaml.load(list1)
print '\nOriginal file looks like:\n\n',list1
print '\nAfter loading, yaml.load(list) looks like:\n\n',y2
print '\nDatatype of loaded object:\n\n',type(y2)

# now what happens when we dump the data using YAML?

print '\n\nWRITING (yaml.dump) ...'
print '\nyaml.dump(file) =\n\n', yaml.dump(y2)

print ''
print '=========='
print ''

# ------ example 3. dictionaries and yaml ------------

# yaml a dictionary; each level of indentation 
#   implies a dictionary of a dictionary

# A dictionary {...} in a Python code looks like this, where
#   the datatype of quantities in brackets [..] is a list:
# dict = {'describe':'World War 2 fighter planes',
#          'howMany':3,
#          'mustang':['P-51','30,000','$10,000'],
#      'thunderbolt':['P-47','25,500','$9,500'],
#        'lightning':['P-38','26,600','%12,350']}

# instead of reading a separate file, keep everything internal
#  to code by using 'file1'

file1 = """
describe: 'World War 2 fighter planes'
howMany: 3
mustang:
    designation: 'P-51'
    maxAltitudeFt: '25000'
    cost: '10000'
thunderbolt:
  designation: "P-47"
  maxAltitudeFt: "30000"
  cost: "9500"
lightning:
  designation: "P-38"
  maxAltitudeFt: "28000"
  cost: "12350"
"""

# what happens when we read the data using YAML?

print 'Example 3: DICTIONARIES AND YAML'
print '\nREADING (yaml.load) ...'
y3 = yaml.load(file1)
print '\nOriginal file looks like:\n\n',file1
print '\nAfter loading, yaml.load(file) looks like:\n\n',y3
print '\nDatatype of loaded object:\n\n',type(y3)

# what happens when we dump the data using YAML?

print '\n\nWRITING (yaml.dump) ...'
print '\nAfter dump, yaml.dump(file) looks like:\n\n', yaml.dump(y3)

print ''
print ' --- END ---'

