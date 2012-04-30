#!/usr/bin/python
# filename: yaml_dump_variable_is_list.py

import yaml

# -------- example: lists and yaml ----------

# 'lists' in Python look like
var = ['line 1','line 2','line 3','last line']

# what happens when we write the data using YAML?

print '\nExample 1: LISTS AND YAML'

# what happens when we dump the data using YAML?
print '\n\nWRITING (yaml.dump) ...'
print '\nyaml.dump(var) =\n\n', yaml.dump(var)

print ''
print '=========='
print ''