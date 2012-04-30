#!/usr/bin/env python

import os, pwd

uidNo=os.getuid()

pwdTuple=pwd.getpwuid ( uidNo)

(login, pwd, pw_uid, pw_gid, pw_gecos, pw_dir, pw_shell)=pwdTuple

print " "

print " Program login_info "

print " "

print " User name '%s' is '%s' " % (login, pw_gecos)

print " pwd is '%s' " % (pwd)

print " pw_uid is '%s' " % (pw_uid)

print " pw_gid is '%s' " % (pw_gid)

print " pw_dir is '%s' " % (pw_dir)

print " pw_shell is '%s' " % (pw_shell)

print " "

print " -- End -- "

print " "

