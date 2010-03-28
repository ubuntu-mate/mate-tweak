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
		self.wTree.get_widget("checkbox_computer").connect("clicked", lambda x: self.set_bool("/apps/nautilus/desktop/computer_icon_visible", x))
		self.wTree.get_widget("checkbox_home").connect("clicked", lambda x: self.set_bool("/apps/nautilus/desktop/home_icon_visible", x))
		self.wTree.get_widget("checkbox_network").connect("clicked", lambda x: self.set_bool("/apps/nautilus/desktop/network_icon_visible", x))
		self.wTree.get_widget("checkbox_trash").connect("clicked", lambda x: self.set_bool("/apps/nautilus/desktop/trash_icon_visible", x))
		self.wTree.get_widget("checkbox_volumes").connect("clicked", lambda x: self.set_bool("/apps/nautilus/desktop/volumes_visible", x))
		self.wTree.get_widget("checkbox_compositing").connect("clicked", lambda x: self.set_bool("/apps/metacity/general/compositing_manager", x))

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

		# Get the current configuration
		confComputer = self.get_bool("/apps/nautilus/desktop/computer_icon_visible")
		if (confComputer):
			self.wTree.get_widget("checkbox_computer").set_active(1)
		confHome = self.get_bool("/apps/nautilus/desktop/home_icon_visible")
		
		if (confHome):
			self.wTree.get_widget("checkbox_home").set_active(1)
		confNetwork = self.get_bool("/apps/nautilus/desktop/network_icon_visible")
		
		if (confNetwork):
			self.wTree.get_widget("checkbox_network").set_active(1)
		confTrash = self.get_bool("/apps/nautilus/desktop/trash_icon_visible")
		
		if (confTrash):
			self.wTree.get_widget("checkbox_trash").set_active(1)
		confVolumes = self.get_bool("/apps/nautilus/desktop/volumes_visible")
		
		if (confVolumes):
			self.wTree.get_widget("checkbox_volumes").set_active(1)
		confCompositing = self.get_bool("/apps/metacity/general/compositing_manager")
		
		if (confCompositing):
			self.wTree.get_widget("checkbox_compositing").set_active(1)

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
