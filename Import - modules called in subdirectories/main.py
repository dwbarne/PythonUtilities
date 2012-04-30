print " This is main module"

print '\nchanging module search path\n'
import sys

print '\n Before append, path =',sys.path

# make sure path includes that for module b
sys.path.append('.\\b')

print '\n  ... after append, path is:',sys.path

print '  ... import a'
import a
#string=a.sub_a()
#print " string =",string
print '  ... import b'
import b

print '   >> This is the end <<\n'

