##!/usr/bin/python

# Filename: argv_example.py

import sys  # retrieves command line arguments;
            #  do NOT use < or > to redirect input or output
            
# open output file
opsys = sys.platform[:3]    # first 3 characters
if opsys == 'win':
    fout = open('./temp.out','w')
else:
#    fout = open('/home/dwbarne/Mantevo_utilities/temp.out','w')
    fout = open('/tmp/tempDWB.out','w')
         
if len(sys.argv) == 1:
    fout.write('\nYou must include a filename on the command line!')
    fout.write('')
    sys.exit()

fout.write('\nsys.argv[0] = %s' % sys.argv[0])
len_sys = len(sys.argv) - 1
fout.write('You have %s other parameters:' % len_sys)
if len_sys > 0:
    for arg in sys.argv[1:]:
        fout.write('   arg = %s' % arg)
else:
    fout.write('\n -- END --')
    sys.exit()
    
'''
f = open(sys.argv[1])
fin = sys.stdin.read()
'''
contents = sys.stdin.read()
fout.write('\n----------')
fout.write('\nContents of file:\n%s' % contents)
fout.write('\n----------')
f.close()

# now parse contents

# Import the email modules we'll need
from email.parser import Parser
import email

#  If the e-mail headers are in a file, uncomment this line:
#headers = Parser().parse(open(messagefile, 'r'))

#  Or for parsing headers in a string, use:
'''
headers = Parser().parsestr('From: <user@example.com>\n'
        'To: <someone_else@example.com>\n'
        'Subject: Test message\n'
        '\n'
        'Body would go here\n')
'''
headers = Parser().parsestr(contents)

fout.write('headers.keys() = %s' % headers.keys())
fout.write('headers.values() = %s' % headers.values())

#  Now the header items can be accessed as a dictionary:
fout.write('\n\nHeaders:')
fout.write('  To: %s' % headers['to'])
fout.write('  From: %s' % headers['from'])
fout.write('  Subject: %s' % headers['subject'])
# get body of email
#print('\nBody:\n%s' % body)
'''
body = email.message_from_string(contents)
print('\n-------------')
print('\nBody:\n%s' % body)
print('-------------')


print ('keys in header: %s\n' % headers.keys())
    
print('\n\nAll headers:\n%s' % headers)
print('\nlen(headers) = %s' % len(headers))
'''

fout.write('\n--- END ---')



'''
>> Another approach

mb = mailbox.UnixMailbox(file('tmp/automated/Feedback', 'r'))
fout = file('Feedback.txt', 'w')
msg = mb.next()

while msg is not None:
    document = msg.fp.read()
    document = passthrough_filter(msg, document)
    msg = mb.next()


def passthrough_filter(msg, document):
    """This prints the 'from' address of the message and
    returns the document unchanged.
    """
    from_addr = msg.getaddr('From')[0]
    Sub = msg.get('Subject')
    ContentType = msg.get('Content-Type')
    ContentDisp = msg.get('Content-Disposition')
    print "From:",from_addr
    print "Subject:",Sub
    print "Attachment:",None
    print "Body:",document
    print '\n'
    return document

'''