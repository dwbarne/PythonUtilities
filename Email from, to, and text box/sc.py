# file sc.py
# 
# check & delete special characters

emailTo=['dwbarne@s/\?>.gov','dd*$(@ear//link`.net']

charList1=[';', '#', ',', '!', '$', '^', '&', '*', '(', ')', '+', '=', '{']
charList2=['}', '[', ']', '|', '\\', '/', ":", "?", '>', "<", "`", " "]
charList=charList1 + charList2
            
specialCharactersInEmailAddresses=0
        
#Debug
print "\nDebug: emailTo = ",emailTo
 
for index in range(len(emailTo)):
    specialCharacterCount=0
    for char in charList:
        specialCharacterCount=emailTo[index].count(char)
        if specialCharacterCount != 0:
            print "\n >> There are %s special characters( %s ) in %s\n" % (                specialCharacterCount,char,emailTo[index])
            specialCharactersInEmailAddresses+=specialCharacterCount
                
if specialCharactersInEmailAddresses != 0:    
    print "\n ERROR: A total of %s special characters were found in the email addresses." % specialCharactersInEmailAddresses
    print "\n        Please correct these before continuing...\n"
# we don't know how to handle special characters embedded in an email address, so just return and let user take care of problem
else:
    print "\n THERE ARE NO SPECIAL CHARACTERS!"