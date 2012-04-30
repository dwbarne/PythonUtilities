#! user/bin/python

# Name: finger
# Author: Keith Jones
# web site:
#   http://www.justlinux.com/forum/showthread.php?t=47711

# A simple example illustrating the use of sockets in python:
# This program uses the python socket interface emulate the
# typical UNIX 'finger' command.

# Usage: finger [[usr@]host]
#   usr - username to finger
#   host - host to finger
#   If no argument is given, use localhost as default

# The process is as follows:
# 1) Connect to well-known finger port (port 79) of desired host
# 2) Send the finger information (either a specific username or a '\n'
# 3) Recieve any information sent and print it out

import socket   # necessary for socket stuff (duh, (c :)
import sys      # necessary to handle command-line arguments

who = ''        # default username to finger 

# First we parse the command line, to determine who to finger
if  len(sys.argv) > 2 or len(sys.argv) == 0:
    print "Usage: %s who@where" % sys.argv[0]
    exit
elif len(sys.argv) == 1:
    where = 'localhost'     # default host
else:
    arg = sys.argv[1]
    '''
    try:
        atpos = arg.index('@');
        who = arg[:atpos]
        where = arg[atpos + 1:]
    except ValueError, verr:
        where = arg
    '''
    try:
        who,where = string.split(arg,'@')
    except ValueError:
        where = arg

# This is all we need to send to the server, so give it a trailing newline
who += '\n'

try:
    # Create a new socket, AF_INET means we want to specify the address & port
    # as a tuple, SOCK_STREAM seems to mean TCP, as opposed to UDP (SOCK_DGRAM)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the host, since we're using AF_INET, we want to specify the
    # address as a pair: the IP address and the port.
    # -It's important to note that this must be passed as a pair (a single
    # argument) to the function; older versions of python allowed you to
    # pass it as two arguments, but that was unintentional and has been fixed.
    # -Notice we translate the name into an IP address. If given an address,
    # gethostbyname will return that, so don't worry.
    
    sock.connect((socket.gethostbyname(where), 79))
    
    # or
    # sock.connect((where, 79)) 
    # is also permissable since Python socket functions also
    # accept domains or ip addresses
    

    # Send the appropriate message to the server, for 'finger' it's very simple
    
    sock.send(who)

    # Wait for the server to reply, and print out the reply. To keep it simple
    # we don't accept more than 1024 characters in the reply string.
    
    print sock.recv(1024)

except socket.error, serr:
    # Alert the user if there was any problem running
    # the finger client. This is rather convenient,
    # since it will tell the user about any error that
    # occurred running 'finger', such as 'unknown
    # host', 'connection refused', etc.
                           
    print "Error: ", serr   