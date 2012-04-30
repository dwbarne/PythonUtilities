# filename: read_csv_file.py
# Author: Shai Vaingast, from book "Beginning Python Visualization"
# Revised by: Daniel Barnette
# date: April 2009

import csv
import MySQLdb
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *  # askokcancel, showinfo, showerror, etc.

# def to handle csv files
def read_csv_file(filename):
    """
    Reads a CSV file and returns it as a list of rows
    """
    data = []
    for row in csv.reader(open(filename)):
         data.append(row)
    print '\nData read in by csv.reader():\n', data
    return data

# send data to database
def send_to_MySQL(stringUser, stringPW, stringHost, numPort, data):
    """
    Connects to database; sends data to the open database; 
    then closes the database
    """
    
# check if connected to a MySQL server
#    self.checkMySQLConnection()
#    if self.connectionFlag == 0: return    
    print ('User: %s   Type: %s' % (stringUser,type(stringUser)))
#    print ('PW: %s   Type: %s' % (stringPW,type(stringPW)))
    print ('Host: %s   Type: %s' % (stringHost,type(stringHost)))
    print ('Port: %s   Type: %s' % (numPort,type(numPort)))
    
# try to connect; if cannot, print error, show window with error, and return    
    try:
        myDbConnection = MySQLdb.connect(
#            user='root',
#            passwd='d',
#            host='localhost',
#            port=3306
            user=stringUser,
            passwd=stringPW,
            host=stringHost,
            port=numPort
            )
    except:
 #       self.MySQL_Output(
        print (
#            1,
            '  Could not connect to database\n' +
            '  Invalid username, password, server or port.\n' +
            '  Could also be due to a simple timeout.\n' +
            '  Check input and try again.'
            )
        showinfo(
            'ERROR',
            'Could not connect - possible invalid username,\n' +
            '  password, server, or port.\n' +
            'Could also be due to a simple timeout.\n' +
            'Check input and try again.'
            )
        return
        
# if we get here, connection is successful
    print ('\nConnected to MySQL database\n')
            
# connect
    myHandler = myDbConnection.cursor()
#        self.checkbuttonStatusDbNotConnected.configure(state='normal')
#        self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
#        self.checkbuttonStatusDbConnected.configure(state='disabled') 

    print
    i=0
    for line in data:
        i+=1
        print i,line
    print

# insert csv data into database table
    i=0
    for line in data:
        i+=1
        print('\nWorking on line # %d' % i)
        try:
            command = "INSERT INTO ctvaugh_cth_performance_on_rs.different_os_versions \
                VALUES(%i,%f,%f,%f,'%s')" % \
                (int(line[0]),float(line[1]),float(line[2]),float(line[3]),line[4] )
        except:
            print ' >> Error: invalid data'
            
        print '  command =',command       
        print
        
        try:
            myHandler.execute(command)
        except:
            print ' >>Error: not able to insert data into database.'

# commit INSERTs
    myDbConnection.commit()
 
    
# get filename
def askOpenFilename(root):
    """
    Purpose:
      open a file and print first 5 lines
    
    Author:
      dwbarne
    
    Date:
      Mon, 04-06-2009
    
    Called by:
      main
    """

    print '\n** In askOpenFilename'
    import os
    currentDirectory = os.getcwd()

# define dictionary of options
    options = {}
    options = {
        'defaultextension' : '.csv',
        'filetypes' : [('csv','.csv'),('All files','.*')],
        'initialdir' : currentDirectory,
        'parent' : root,
        'title' : 'Read file'
        }

# get full pathname
    filename = askopenfilename(**options)
    dirname, filenameShort = os.path.split(filename)

# open the file and store contents in myfileContents
    myfileContents = open(filename,'r').readlines()
    
# print myfileContents
    print (
        '\nentire file contents:\n %s \n' % myfileContents
        )
        
    print (
        "There are %s lines in file %s \n" % (len(myfileContents),filename)
        )

# print first 5 lines of the file
    print('First five lines of file %s:' % filenameShort)
    lineCountMax = 5
    lineCount = 1
    for eachLine in myfileContents:
        print('%d %s' % (lineCount,eachLine))
        lineCount += 1
        if lineCount == lineCountMax: break
        
    return filename
        
# ===== main =====
root=Tk()
fn=askOpenFilename(root)
final_output = read_csv_file(fn)
print ('\nfinal_output:\n%s' % final_output)
print ('\nfinal_output[0]:\n%s' % final_output[0])
print('\nfinal_output[1]:\n%s' % final_output[1])
print('\nfinal_output[1][4]:\n%s' % final_output[1][4])
# send to database
answer = askyesno(
    'Send to database?',
    'Do you wish to send data to database?'
    )
if answer:
    send_to_MySQL('root', 'd', 'localhost', 3306, final_output)


