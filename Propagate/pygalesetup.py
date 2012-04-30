#
# $Id: pygalesetup.py,v 1.3 2001/08/14 22:22:34 tlau Exp $
#
import Tkinter
import tkFileDialog, tkMessageBox
import os, sys
import shutil
import socket
import string
from pygale import pygale, gale_env, userinfo, version, ROOT

PYGALE_CONF = 'pygale.conf'
def get_start_dir():
	start_dir = os.path.dirname(sys.argv[0])
	orig_dir = os.getcwd()
	if start_dir:
		os.chdir(start_dir)
	start_dir = os.getcwd()
	os.chdir(orig_dir)
	return start_dir

def make_path(path_name):
	current_path = path_name
	unmade_dirs = []
	while current_path and not os.path.exists(current_path):
		unmade_dirs.insert(0, current_path)
		current_path = os.path.dirname(current_path)
	for dir_name in unmade_dirs:
		os.mkdir(dir_name)
		

class WizardDialog(Tkinter.Frame):
	def __init__(self, master, frame_list):
		Tkinter.Frame.__init__(self, master)
		self.master = master
		self.current_frame = 0
		self.finished = 0
		self.abort = 0
		self.vars = {}
		self.grid(row = 0, column = 0, sticky = 'nswe')
		self.frame_area = Tkinter.Frame(self, width = 320, height = 184)
		self.frame_area.grid(row = 0, column = 0, sticky = 'wens', pad = 10)
		self.frame_area.grid_propagate(0)
		self.frame_area.grid_columnconfigure(0, weight = 1)
		self.frame_area.grid_rowconfigure(0, weight = 1)
		self.frame_list = []
		for frame in frame_list:
			frame_instance = frame(self.frame_area, self, self.vars)
			self.frame_list.append(frame_instance)
		self.separator = Tkinter.Frame(self, width = 320, height = 2, borderwidth = 1, relief = 'sunken')
		self.separator.grid_propagate(0)
		self.separator.grid(row = 1, column = 0, pad = 10)
		self.button_area = Tkinter.Frame(self, width = 280, height = 50)
		self.button_area.grid_propagate(0)
		self.button_area.grid(row = 2, column = 0, sticky = 'we', pad = 10)
		self.button_area.grid_columnconfigure(0, weight = 1)
		self.button_area.grid_rowconfigure(0, weight = 1)
		self.next_button = Tkinter.Button(self.button_area, 
						  command = self.next, 
						  default = 'active',
						  text = 'Next', width = 10)
		self.next_button.grid(row = 0, col = 1, sticky = 'e')
		self.prev_button = Tkinter.Button(self.button_area, 
						  command = self.prev,
						  text = 'Prev', width = 10)
		self.prev_button.grid(row = 0, col = 0, sticky = 'e')
		self.cancel_button = Tkinter.Button(self.button_area,
						    command = self.cancel,
						    text = 'Cancel', width = 10)
		self.cancel_button.grid(row = 0, col = 4, sticky = 'e')
		self.button_area.grid_columnconfigure(3, minsize = 10)
		self.display_frame(0)


	def set_next_to_finish(self):
		self.next_button.configure(text = 'Finish', 
					   command = self.finish)

	def set_next_to_next(self):
		self.next_button.configure(text = 'Next', command = self.next)


	def disable_prev(self):
		self.prev_button.configure(state = 'disabled')

	
	def enable_prev(self):
		self.prev_button.configure(state = 'normal')


	def disable_next(self):
		self.next_button.configure(state = 'disabled')


	def enable_next(self):
		self.next_button.configure(state = 'normal')


	def display_frame(self, index):
		if index == len(self.frame_list) - 1:
			self.set_next_to_finish()
		else:
			self.set_next_to_next()
		if index == 0:
			self.disable_prev()
		else:
			self.enable_prev()
		self.master.title(self.frame_list[index].title)
		self.frame_list[index].display()


	def undisplay_frame(self, index):
		self.frame_list[index].undisplay()


	def next(self):
		current_frame = self.frame_list[self.current_frame]
		if hasattr(current_frame, 'next'):
			current_frame.next()
		if self.abort:
			self.destroy()
		else:
			self.undisplay_frame(self.current_frame)
			self.current_frame = self.current_frame + 1
			self.display_frame(self.current_frame)


	def prev(self):
		self.undisplay_frame(self.current_frame)
		self.current_frame = self.current_frame - 1
		self.display_frame(self.current_frame)

	
	def finish(self):
		current_frame = self.frame_list[self.current_frame]
		if hasattr(current_frame, 'next'):
			current_frame.next()
		self.finished = 1
		self.destroy()


	def cancel(self):
		self.destroy()

	def add_screen_after(self, after_frame, new_frame_class):
		index = self.frame_list.index(after_frame)
		if self.frame_list[index+1].__class__ == new_frame_class:
			return
		new_frame = new_frame_class(self.frame_area, self,
			after_frame.vars)
		self.frame_list.insert(index + 1, new_frame)

	def del_screen_after(self, after_frame):
		index = self.frame_list.index(after_frame)
		if (index + 1) >= len(self.frame_list):
			# out of bounds error
			return
		del self.frame_list[index+1]
	
	def next_screen_is(self, curframe, next_class):
		index = self.frame_list.index(curframe)
		if (index + 1) >= len(self.frame_list):
			# out of bounds error
			return 0
		return self.frame_list[index+1].__class__ == next_class

# ----------------------------------------------------------------------
# Wizard configuration screens

class GetPygaleDir(Tkinter.Frame):
	def __init__(self, master, wizard, vars):
		Tkinter.Frame.__init__(self, master)
		self.wizard = wizard
		self.vars = vars
		self.title = 'PyGale configuration'
		self.galedir = gale_env.get('PYGALE_DIR',
			os.path.join(userinfo.home_dir, '.gale'))
		if not os.path.exists(self.galedir):
			create_str = "\n\nThis directory does not exist.  I'll " +\
				     'create it for you.\n'
		else:
			create_str = '\n\nGood!  This directory already exists.\n'
		
		conffile = os.path.join(self.galedir, PYGALE_CONF)
		if os.path.exists(conffile):
			create_str = create_str + "I'll read the settings from " +\
				'your existing conf file.\n'
			gale_env.load_file(conffile)

		self.label = Tkinter.Label(self, wraplength=310, anchor='nw',
			justify='left', text=
			'PyGale configuration, version %s\n\n' % version.VERSION +
			'By default, this configuration will be stored in the ' +
			'.gale directory in your home directory.  Optionally, you ' +
			'can set the environment variable PYGALE_DIR to a directory ' +
			'where the configuration file will be stored.\n\n' +
			'Your Gale directory is: ' + self.galedir +
			create_str
			)
	
	def display(self):
		self.grid(row = 0, column = 0, sticky = 'wens')
		self.label.grid(row = 0, column = 0, sticky = 'news')
	
	def undisplay(self):
		self.grid_forget()
		self.label.grid_forget()
	
	def next(self):
		try:
			make_path(self.galedir)
		except OSError, e:
			m = tkMessageBox.showerror(
				title='Cannot create directory',
				parent=self,
				message='Unable to create directory ' +
					self.galedir + ':\n' + e[1] + '\n\n' +
					'Aborting configuration...')
			self.wizard.abort = 1	
		gale_env.set('PYGALE_DIR', self.galedir)

		
class GetGaleSysDir(Tkinter.Frame):
	def __init__(self, master, wizard, vars):
		Tkinter.Frame.__init__(self, master)
		self.wizard = wizard
		self.vars = vars
		self.gale_sys_dir = Tkinter.StringVar()
		self.title = 'PyGale configuration'

		self.gale_sys_dir.set(gale_env.get('GALE_SYS_DIR',
			'/usr/local/etc/gale'))
		self.label = Tkinter.Label(self, wraplength = 310, anchor = 'nw',
			justify = 'left', text = "Gale system directory\n\nThis directory contains the public key cache and other Gale-specific data.  It can and should be shared between Gale users on the same machine or network.  If you have an existing Gale installation, enter its path here.  Otherwise, I will create this directory for you.")
		self.entry = Tkinter.Entry(self, textvariable = self.gale_sys_dir)

	def display(self):
		self.grid(row = 0, column = 0, sticky = 'wens')
		self.label.grid(row = 0, column = 0, sticky = 'news')
		self.entry.grid(row = 1, column = 0, sticky = 'nwe')

	def undisplay(self):
		self.grid_forget()
		self.label.grid_forget()
		self.entry.grid_forget()

	def next(self):
		abspath = os.path.abspath(self.gale_sys_dir.get())
		gale_env.set('GALE_SYS_DIR', abspath)

class GetGaleDomain(Tkinter.Frame):
	def __init__(self, master, wizard, vars):
		Tkinter.Frame.__init__(self, master)
		self.wizard = wizard
		self.vars = vars
		self.title = 'Enter Gale Domain'
		self.gale_domain = Tkinter.StringVar()
		domain = gale_env.get('GALE_DOMAIN', None)
		if domain is None:
			domain = socket.gethostbyaddr(socket.gethostname())[0]
		self.gale_domain.set(domain)
		self.grid_propagate(0)
		self.grid_rowconfigure(0, weight = 1)
		self.grid_rowconfigure(1, weight = 1)
		self.grid_columnconfigure(0, weight = 1)
		self.label = Tkinter.Label(self, wraplength = 310, anchor = 'nw', justify = 'left', text = "Gale domain\n\nEnter your Gale domain here (for example, gale.org).  If you don't know what this is, contact your local Gale administrator.  This domain will be appended to all non-qualified locations, and it determines which Gale server you will connect to.")
		self.entry = Tkinter.Entry(self, textvariable = self.gale_domain)


	def display(self):
		self.grid(row = 0, column = 0, sticky = 'wens')
		self.label.grid(row = 0, column = 0, sticky = 'we', 
				columnspan = 2)
		self.entry.grid(row = 1, column = 0, sticky = 'nwe')


	def undisplay(self):
		self.grid_forget()
		self.label.grid_forget()
		self.entry.grid_forget()


	def next(self):
		gale_env.set('GALE_DOMAIN', self.gale_domain.get())


class GetGaleUser(Tkinter.Frame):
	def __init__(self, master, wizard, vars):
		Tkinter.Frame.__init__(self, master)
		self.wizard = wizard
		self.vars = vars
		self.title = 'Enter User ID'
		self.gale_user = Tkinter.StringVar()
		user = pygale.gale_user()
		self.gale_user.set(user)
		self.grid_propagate(0)
		self.grid_rowconfigure(0, weight = 1)
		self.grid_rowconfigure(1, weight = 1)
		self.grid_columnconfigure(0, weight = 1)
		self.label = Tkinter.Label(self, wraplength = 310, anchor = 'nw', justify = 'left', text = "Gale user id\n\nEnter your Gale id.  This id identifies you to other Gale users.  You must have a valid public/private key pair for this id.")
		self.entry = Tkinter.Entry(self, textvariable = self.gale_user)


	def display(self):
		self.grid(row = 0, column = 0, sticky = 'wens')
		self.label.grid(row = 0, column = 0, sticky = 'we', 
				columnspan = 2)
		self.entry.grid(row = 1, column = 0, sticky = 'nwe')


	def undisplay(self):
		self.grid_forget()
		self.label.grid_forget()
		self.entry.grid_forget()


	def next(self):
		sig_name = self.gale_user.get()
		gale_env.set('GALE_ID', sig_name)
		gale_dir = gale_env.get('GALE_DIR',
			os.path.join(userinfo.home_dir, '.gale'))
		privkey = os.path.join(gale_dir, 'auth', 'private', sig_name)
		privkey_gpri = os.path.join(gale_dir, 'auth', 'private',
			sig_name + '.gpri')
		self.vars['sig_name'] = sig_name
		if os.path.exists(privkey_gpri):
			file_exists = 1
			sigfile = privkey_gpri
		elif os.path.exists(privkey):
			file_exists = 1
			sigfile = privkey
		else:
			file_exists = 0
			sigfile = None
		next_is_sigscreen = self.wizard.next_screen_is(self, FindSignature)
		if not file_exists and not next_is_sigscreen:
			self.wizard.add_screen_after(self, FindSignature)
		elif not file_exists and next_is_sigscreen:
			pass
		elif file_exists and not next_is_sigscreen:
			pass
		elif file_exists and next_is_sigscreen:
			self.wizard.del_screen_after(self)

		if file_exists:
			self.vars['sig_file_name'] = sigfile			

class FindSignature(Tkinter.Frame):
	def __init__(self, master, wizard, vars):
		Tkinter.Frame.__init__(self, master)
		self.vars = vars
		self.title = 'Find Signature'
		self.sig_file_name = Tkinter.StringVar()
		sig_name = self.vars['sig_name']

		gale_dir = gale_env.get('GALE_DIR',
			os.path.join(userinfo.home_dir, '.gale'))
		sig_file = os.path.join(gale_dir, 'auth', 'private', sig_name)
		sig_file_gpri = sig_file + '.gpri'
		if os.path.exists(sig_file_gpri):
			self.sig_file_name.set(sig_file_gpri)
		elif os.path.exists(sig_file):
			self.sig_file_name.set(sig_file)
		self.grid_propagate(0)
		self.grid_rowconfigure(0, weight = 1)
		self.grid_rowconfigure(1, weight = 1)
		self.grid_columnconfigure(0, weight = 1)
		self.grid_columnconfigure(1, weight = 0)
		self.label = Tkinter.Label(self, wraplength = 310, anchor = 'nw', justify = 'left', text = "The Gale id you have specified requires a private key file.  I was unable to find it at either '%s' or '%s'.  Enter the location of your private key file." % (sig_file_gpri, sig_file))
		self.browse_button = Tkinter.Button(self, command = self.browse, text= 'Browse', width = 10)
		self.entry = Tkinter.Entry(self, textvariable = self.sig_file_name)


	def display(self):
		self.grid(row = 0, column = 0, sticky = 'wens')
		self.label.grid(row = 0, column = 0, sticky = 'we', 
				columnspan = 2)
		self.entry.grid(row = 1, column = 0, sticky = 'nwe')
		self.browse_button.grid(row = 1, column = 1, sticky = 'nw', pad = 5)


	def undisplay(self):
		self.grid_forget()
		self.label.grid_forget()
		self.entry.grid_forget()
		self.browse_button.grid_forget()


	def browse(self):
		result = tkFileDialog.askopenfilename()
		result = os.path.normpath(result)
		self.entry.delete(0, Tkinter.END)
		self.entry.insert(Tkinter.END, result)


	def next(self):
		self.vars['sig_file_name'] = self.sig_file_name.get()

class EnterUser(Tkinter.Frame):
	def __init__(self, master, wizard, vars):
		Tkinter.Frame.__init__(self, master)
		self.title = 'Select User Name'
		self.vars = vars
		self.user_name = Tkinter.StringVar()
		# Use (in order) GALE_NAME or our username
		fullname = gale_env.get('GALE_NAME', userinfo.user_name)
		self.user_name.set(fullname)
		self.grid_propagate(0)
		self.grid_rowconfigure(0, weight = 1)
		self.grid_rowconfigure(1, weight = 1)
		self.grid_columnconfigure(0, weight = 1)
		self.user_label = Tkinter.Label(self, wraplength = 310, anchor = 'nw', justify = 'left', text = "Enter your user name.  This is a free form string that accompanies every puff.  People generally use their full name (e.g. Joe Smith).")
		self.user_entry = Tkinter.Entry(self, textvariable = self.user_name)	


	def display(self):
		self.grid(row = 0, column = 0, sticky = 'wens')
		self.user_label.grid(row = 0, column = 0, sticky = 'we')
		self.user_entry.grid(row = 1, column = 0, sticky = 'nwe')


	def undisplay(self):
		self.grid_forget()
		self.user_label.grid_forget()
		self.user_entry.grid_forget()


	def next(self):
		gale_env.set('GALE_NAME', self.user_name.get())

# Check for existing conf file, and if it doesn't exist, run the
# configurator
def check():
	pygaledir = gale_env.get('PYGALE_DIR',
		os.path.join(userinfo.home_dir, '.gale'))
	conf_file = os.path.join(pygaledir, PYGALE_CONF)
	if os.path.exists(conf_file):
		gale_env.load_file(conf_file)
		if gale_env.get('PYGALE_VERSION', '1.0') >= version.VERSION:
			return
	run_gui_setup()

def run_gui_setup():
	print get_gale_sys_env()
	root = Tkinter.Tk()
	if sys.platform == 'win32':
		wizard = WizardDialog(root, [GetPygaleDir, GetGaleDomain,
			GetGaleUser, EnterUser])
	else:
		wizard = WizardDialog(root, [GetPygaleDir, GetGaleSysDir,
			GetGaleDomain, GetGaleUser, EnterUser])
	wizard.wait_window(wizard)
	if not wizard.finished:
		sys.exit(0)

	write_settings()

	# Copy private key file
	user, domain = string.split(os.path.basename(
		wizard.vars['sig_name']),'@', 1)
	gale_dir = gale_env.get('GALE_DIR',
		os.path.join(userinfo.home_dir, '.gale'))
	private_dir = os.path.join(gale_dir, 'auth', 'private')
	target_file = os.path.join(private_dir,
		os.path.basename(wizard.vars['sig_file_name']))
	if not os.path.exists(target_file):
		shutil.copy(wizard.vars['sig_file_name'], target_file)
	else:
		print 'Not overwriting existing private key:', target_file
	
	# Quit
	root.destroy()
		
def conditional_mkdir(dir_name, perms = None):
	parent = os.path.dirname(dir_name)
	if parent and not os.path.exists(parent):
		conditional_mkdir(parent)
	if not os.path.exists(dir_name):
		print 'Creating directory', dir_name
		try:
			os.mkdir(dir_name)
		except Exception, e:
			print 'Unable to create directory %s: %s' % (dir_name, e)
			sys.exit(-1)
		if perms is not None:
			os.chmod(dir_name, perms)

def get_gale_sys_env():	
	pygaledir = gale_env.get('PYGALE_DIR',
		os.path.join(userinfo.home_dir, '.gale'))
	fname = os.path.join(pygaledir, PYGALE_CONF)
	if os.path.exists(fname):
		gale_env.load_file(fname)
		result = 'Reading PyGale settings from ' + fname
	else:
		# Assume some reasonable defaults
		try:
			gale_env.set('GALE_SYS_DIR', os.path.join(string.strip(
				os.popen('gale-config --prefix', 'r').read()),
				'etc', 'gale'))
		except:			
			# Can't find gale-config; Gale probably isn't installed
			if sys.platform == 'win32':
				gale_env.set('GALE_SYS_DIR', get_start_dir())
			else:
				gale_env.set('GALE_SYS_DIR', '/usr/local/etc/gale')
		conffile = os.path.join(gale_env.get('GALE_SYS_DIR'), 'conf')
		if os.path.exists(conffile):
			confvars = gale_env.parse_sys_conf(conffile)
			result = 'Reading Gale settings from ' + conffile
		else:
			confvars = {}
			result = 'No existing Gale configuration found'
		if confvars.has_key('GALE_DOMAIN'):
			gale_env.set('GALE_DOMAIN', confvars['GALE_DOMAIN'])
		
	return result

def write_settings():
	GALE_SYS_DIR = gale_env.get('GALE_SYS_DIR')
	conditional_mkdir(GALE_SYS_DIR, 0755)
	conditional_mkdir(os.path.join(GALE_SYS_DIR, 'auth'), 0755)
	conditional_mkdir(os.path.join(GALE_SYS_DIR, 'auth', 'cache'), 0777)
	conditional_mkdir(os.path.join(GALE_SYS_DIR, 'auth', 'local'), 01777)
	conditional_mkdir(os.path.join(GALE_SYS_DIR, 'auth', 'private'), 0755)
	conditional_mkdir(os.path.join(GALE_SYS_DIR, 'auth', 'trusted'), 0755)
	root_key_path = os.path.join(GALE_SYS_DIR, 'auth', 'trusted', 'ROOT')
	if not os.path.exists(root_key_path):
		try:
			f = open(root_key_path, 'wb')
			f.write(ROOT.rootkey)
			f.close()
			os.chmod(root_key_path, 0644)
		except:
			print '#' * 50
			print 'Trouble installing the ROOT key in its proper location.'
			print 'WARNING!  Puffs will not be verified!'
			print '#' * 50
	galedir = gale_env.get('GALE_DIR',
		os.path.join(userinfo.home_dir, '.gale'))
	conditional_mkdir(galedir)
	conditional_mkdir(os.path.join(galedir, 'auth'))
	conditional_mkdir(os.path.join(galedir, 'auth', 'local'))
	conditional_mkdir(os.path.join(galedir, 'auth', 'private'))
	conditional_mkdir(os.path.join(galedir, 'auth', 'trusted'))
	pygaledir = gale_env.get('PYGALE_DIR',
		os.path.join(userinfo.home_dir, '.gale'))
	fname =  os.path.join(pygaledir, PYGALE_CONF)
	f = open(fname, 'w')
	f.write('PYGALE_VERSION %s\n' % version.VERSION)
	f.write('GALE_SYS_DIR %s\n' % gale_env.get('GALE_SYS_DIR'))
	f.write('GALE_ID %s\n' % gale_env.get('GALE_ID'))
	f.write('GALE_DOMAIN %s\n' % gale_env.get('GALE_DOMAIN'))
	f.write('GALE_NAME %s\n' % gale_env.get('GALE_NAME'))
	f.close()
	
	print 'Run pygale-config to modify this configuration at any point.'

# Change this to run_gui_setup() when that works
config = run_gui_setup

if __name__ == '__main__':
	run_gui_setup()
