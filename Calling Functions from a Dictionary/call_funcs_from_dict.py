# Call funcs from a dictionary
# 081409

# define functions
def func0(): print 'this is func0'

def func1(): print 'this is func1'

def func2(): print 'this is func2'

def func3(): print 'this is func3'

# define dictionary with function names
dictFuncs = {0:func0, 1:func1, 2:func2}

# define main function
def myFunc(inputList):
    for element in inputList:
        success = 0
        for key,value in dictFuncs.iteritems():
            if value == element:
                success = 1 
                dictFuncs[key]()
                break
        if not success:
            print 'no dictionary pair defined for',element

# call main method
myFunc([func2,func0,func1,func3])
