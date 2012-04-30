import yaml

# yaml a dictionary; each level of indentation 
#   implies a dictionary of a dictionary

document1 = """
a: 1
b:
  c: 3
  d:
    e: "5: INFO: 100"
    f: 6
    f: 7
"""

#print yaml.dump(yaml.load(document))
y1 = yaml.load(document1)
print 'document1:\n',document1
print '\nyaml.load(document1) =',y1
print '\nyaml.dump(y1) =\n', yaml.dump(y1)
print '\ntype(y1) =',type(y1)

# now yaml a list

document2 = """
 - Hesperiidae
 - Papilionidae
 - Apatelodidae
 - Epiplemidae
"""
y2=yaml.load(document2)
print '\n\ndocument2:\n',document2
print '\nyaml.load(document2) =',y2
print '\nyaml.dump(y2) =\n', yaml.dump(y2)
print '\ntype(y2) =',type(y2)
