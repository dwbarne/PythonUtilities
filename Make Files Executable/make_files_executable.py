# website:
#  http://www.jorendorff.com/articles/python/path/
#
# filename: make_files_executable.py

######################
# to chmod one file
######################

ppath=os.getcwd()	# get present path

# get filename
from tkFileDialog import askopenfilename
filenm=askopenfilename
print filenm
ppath=os.getcwd()
filenm1=os.path.join(ppath, filenm)  # not necessary, but informational
os.chmod(filenm1,0755)		# can also use just filenm
# to run python program:
os.system('python '+filenm1)


############################################
# to chmod many files in a directory,
#  with either python or unix path known
############################################

# with os.path known in python
#DIR = '/usr/home/guido/bin'

for f in os.listdir(DIR):
    if f.endswith('.py'):
        path = os.path.join(DIR, f)
        os.chmod(path, 0755)  # Assume it's a file

# with path known in unix
d = path('/usr/home/guido/bin')
for f in d.files('*.py'):
    f.chmod(0755)
	