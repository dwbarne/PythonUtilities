# filename: stringsearch.py
# date: 031210
# 
# Purpose: search a string for a sub-string; count the matches

import fnmatch

def findit1(string2search, string2find):
    '''
    Purpose:
        finds any part of string2find (all combinations) in the sequence
          defined by string2search
        find a close match defined as only wrong at 1
          location and I what to record the location.
    '''
    icount=0
    for i in range(len(string2find)):
        match = '*' + string2find[0:i] + '?' + string2find[i+1:] + '*'
        print 'match =',match
        if fnmatch.fnmatch(string2search, match):
            icount += 1
            print 'Match found, icount =',icount
            
    return
            
def findit2(string2search, string2find):
    '''
    Purpose:
        finds all occurrences of "string2find" in "string2search"
    '''
    print '\n\nIn findit2...'
    print 'string2search = ',string2search
    print 'string2find =',string2find
    lenString2Find = len(string2find)
    print 'length of %s = %s' % (string2find, lenString2Find)
    icount = 0
    for i in range(len(string2search)):
        substring2search = string2search[i:i + lenString2Find]
        print '   substring2search =',substring2search
        if substring2search == string2find:
            icount += 1
            print '      Match found: icount =',icount
            
    print '\nTotal matches found in string:',icount
            
    return

# the following string contains 4 instances of '123'  and 2 instances of 'dog8'         
string2search = '123123478990708971dog899870389701270981230dog87123'

# define string to find in above string
# string2find = '123'
string2find = 'dog8'

# find it
findit1(string2search, string2find)

# find it
findit2(string2search, string2find)