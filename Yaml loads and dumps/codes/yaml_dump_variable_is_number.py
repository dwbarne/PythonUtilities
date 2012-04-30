#!/usr/bin/python
# filename: yaml_dump_variable_is_number.py

import yaml

# -------- example: variables and yaml ----------

# 'Variables' in Python look like
var = 40.3388

# what happens when we write the data using YAML?

print '\nExample 1: VARIABLES AND YAML'

# what happens when we dump the data using YAML?
print '\n\nWRITING (yaml.dump) ...'
print '\nyaml.dump(var) =\n\n', yaml.dump(var)

print ''
print '=========='
print ''