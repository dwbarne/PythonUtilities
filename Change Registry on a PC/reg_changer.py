#
# Setup the desktop or laptop registry to allow us to double click on python   scripts
# Run this from a DOS window by cd'ing to the directory and typing
#    python reg_changer.py
#
from _winreg import *
import sys

print "Setting up registry to allow\ndouble clicking of Python files to work"

#
# Create the registry entries for ".py" and ".pyc"  extensions
#
for Name in (".py", ".pyc"):
   Key = CreateKey(HKEY_CLASSES_ROOT, Name)
   SetValue(Key, None, REG_SZ, "Python.File")
   CloseKey(Key)

#
# Create   HKEY_CLASSES_ROOT\Python.File\Shell\Open\Command = "\Program Files\Python\Lib\Python.exe" "%1"
#
Key = CreateKey(HKEY_CLASSES_ROOT, "Python.File")
for Name in ("Shell","Open","Command"):
  New_Key= CreateKey(Key, Name)
  CloseKey(Key)
  Key = New_Key
SetValue(Key, None, REG_SZ, '"' + sys.executable + '" "%1"')
CloseKey(Key)