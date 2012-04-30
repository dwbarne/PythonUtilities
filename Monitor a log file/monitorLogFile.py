#!/usr/bin/python

# Purpose:
#   Monitor a log file specified by user

"""
[output]
Enter the log file to be monitored: /var/log/messages
May  6 16:00:01 opteron cron[24679]: (root) CMD (rm -f 
/var/spool/cron/lastrun/cron.hourly)
May  6 16:00:01 opteron run-crons[24685]: (root) CMD 
(/etc/cron.hourly/moodle)
"""

"Python program similar to tail -f"
import os
import sys
import commands
import time

sec_to_wait = 60
fname = raw_input('Enter the log file to be monitored: ')

def usage():
    """Explains the program to the user"""
	print \
        "You will need to be root to monitor most log files."

def check_whoami():
    """Check if Root"""
    if commands.getoutput('whoami') != 'root':
        sys.exit('\nYou will need to be Root!\n')


def tail_it(fname, bufsize, linesep):
    """
    update if monitored file time changes
    """
    old_time = os.stat(fname).st_mtime
    while True:
        new_time = os.stat(fname).st_mtime
        if new_time > old_time:

            updated = get_tail(fname, 8, bufsize, linesep)
            for i in updated:
                print i
            old_time = new_time
        time.sleep(sec_to_wait)
     
def print_log_end(fname, bufsize, linesep):
    for i in get_tail(fname, 8, bufsize, linesep):
        print i

def get_tail(fname, numlines, bufsize, linesep):
    f = open(fname, 'r')
    f.seek(-bufsize, os.SEEK_END)    # goto one buffsize away from end
    result =  f.read().split(linesep)[-numlines:]
    f.close()
    return result

if __name__ == "__main__":
    print_log_end(fname, bufsize=8192, linesep=os.linesep)
    check_whoami()
    tail_it(fname, bufsize=8192, linesep=os.linesep)
