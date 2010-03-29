#!/usr/bin/env python

try:
	import os
	import commands
	import sys
	import string
	import pygtk
	pygtk.require("2.0")
	import gtk
	import gtk.glade
	import gettext
	import gconf
except Exception, detail:
	print detail
	sys.exit(1)


# i18n
# TODO: Badly need to fix this - overuse of "The" etc.
gettext.install("mintdesktop", "/usr/share/linuxmint/locale")

# i18n for menu item
menuName = _("Desktop Settings")
menuGenericName = _("Gnome Gonfiguration Tool")
menuComment = _("Fine-tune Gnome settings")

class MintDesktop:	

	"""MintDesktop - Makes the best out of your Gnome desktop..."""

	# Set a string in gconf
	def set_string(self, key, value):
		client = gconf.client_get_default()
		client.set_string(key, value)
				
	# Get a string from gconf
	def get_string(self, key):
		client = gconf.client_get_default()
		return client.get_string(key)

	# Set a boolean in gconf according to the value of the passed gtk.CheckButton
	def set_bool(self, key, value):
		client = gconf.client_get_default()
		client.set_bool(key, value.get_active())

	# Get a boolean from gconf
	def get_bool(self, key):
		client = gconf.client_get_default()
		return client.get_bool(key)


	def __init__(self):
		
		self.gladefile = '/usr/lib/linuxmint/mintDesktop/mintDesktop.glade'

		self.wTree = gtk.glade.XML(self.gladefile, "main_window") 

		self.wTree.get_widget("main_window").connect("destroy", gtk.main_quit)
		self.wTree.get_widget("button_cancel").connect("clicked", gtk.main_quit)
		self.wTree.get_widget("combo_wmlayout").append_text(_("Traditional style"))
		self.wTree.get_widget("combo_wmlayout").append_text(_("Mac style"))
		self.wTree.get_widget("combo_wmlayout").append_text(_("Ubuntu style"))

		# i18n
		self.wTree.get_widget("main_window").set_title(_("Desktop Settings"))
		self.wTree.get_widget("label3").set_text(_("Desktop Items"))
		self.wTree.get_widget("label5").set_text(_("Window Manager"))
		self.wTree.get_widget("label_layouts").set_text(_("Window buttons layout:"))
		self.wTree.get_widget("checkbox_computer").set_label(_("Computer"))
		self.wTree.get_widget("checkbox_home").set_label(_("Home"))
		self.wTree.get_widget("checkbox_network").set_label(_("Network"))
		self.wTree.get_widget("checkbox_trash").set_label(_("Trash"))
		self.wTree.get_widget("checkbox_volumes").set_label(_("Mounted Volumes"))
		self.wTree.get_widget("checkbox_compositing").set_label(_("Gnome compositing"))

		# tell gconf we want to be notified when these change
		client = gconf.client_get_default()
		client.add_dir("/apps/nautilus/desktop", gconf.CLIENT_PRELOAD_NONE)
		client.add_dir("/apps/metacity/general", gconf.CLIENT_PRELOAD_NONE)

		# initialise the checkboxes		
		self.init_checkbox("/apps/nautilus/desktop/computer_icon_visible", "checkbox_computer")
		self.init_checkbox("/apps/nautilus/desktop/home_icon_visible", "checkbox_home")
		self.init_checkbox("/apps/nautilus/desktop/network_icon_visible", "checkbox_network")
		self.init_checkbox("/apps/nautilus/desktop/trash_icon_visible", "checkbox_trash")
		self.init_checkbox("/apps/nautilus/desktop/volumes_visible", "checkbox_volumes")
		self.init_checkbox("/apps/metacity/general/compositing_manager", "checkbox_compositing")

		# slightly more complicated. find the window manager button layout in use..
		confLayout = self.get_string("/apps/metacity/general/button_layout")
		if (":minimize,maximize,close" in confLayout):
			self.wTree.get_widget("combo_wmlayout").set_active(0)
		elif ("close,minimize,maximize:" in confLayout):
			self.wTree.get_widget("combo_wmlayout").set_active(1)
		elif ("maximize,minimize,close:" in confLayout):
			self.wTree.get_widget("combo_wmlayout").set_active(2)

		#else
			# TODO: Add checking for custom layouts here, store the layout etc.

		self.wTree.get_widget("combo_wmlayout").connect("changed", self.applyWMChanges)


	''' Initialise the CheckButton with a gconf value, then bind it with the gconf system '''
	def init_checkbox(self, key, name):
		widget = self.wTree.get_widget(name)
		conf = self.get_bool(key)
		widget.set_active(conf)
		widget.connect("clicked", lambda x: self.set_bool(key, x))
		self.add_notify(key, widget)

	''' adds a notify system... '''
	def add_notify(self, key, widget):
		client = gconf.client_get_default()
		notify_id = client.notify_add(key, self.key_changed_callback, widget)
		widget.set_data('notify_id', notify_id)
		widget.set_data('client', client)
		widget.connect("destroy", self.destroy_callback)


	''' destroy the associated notifications '''
	def destroy_callback (self, widget):
		client = widget.get_data ('client')
    		notify_id = widget.get_data ('notify_id')

		if notify_id:
			client.notify_remove (notify_id)

	''' Callback for gconf. update our internal values '''
	def key_changed_callback (self, client, cnxn_id, entry, widget):
		# deal with all boolean (checkboxes)
		if (type(widget) == gtk.CheckButton):
			if(entry.value.type == gconf.VALUE_BOOL):
				value = entry.value.get_bool()
				if(widget):
					widget.set_active(value)

	''' Update the window manager button layout '''
	def applyWMChanges(self, widget): 
		wmindex = self.wTree.get_widget("combo_wmlayout").get_active()
		if (wmindex == 0):
			self.set_string("/apps/metacity/general/button_layout", "menu:minimize,maximize,close")
		elif (wmindex == 1):
			self.set_string("/apps/metacity/general/button_layout", "close,minimize,maximize:")
		elif (wmindex == 2):
			self.set_string("/apps/metacity/general/button_layout", "maximize,minimize,close:")
			
if __name__ == "__main__":
	MintDesktop()
	gtk.main()
