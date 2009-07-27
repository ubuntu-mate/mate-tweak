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
except Exception, detail:
	print detail
	sys.exit(1)


# i18n
gettext.install("messages", "/usr/lib/linuxmint/mintDesktop/locale")


class MintDesktop:
	"""MintDesktop - Makes the best out of your Gnome desktop..."""

	def __init__(self):
		
		self.gladefile = '/usr/lib/linuxmint/mintDesktop/mintDesktop.glade'
		self.wTree = gtk.glade.XML(self.gladefile, "main_window") 
		self.wTree.get_widget("main_window").connect("destroy", gtk.main_quit)
		self.wTree.get_widget("button_cancel").connect("clicked", gtk.main_quit)
		self.wTree.get_widget("button_ok").connect("clicked", self.applyChanges)

		# i18n
		self.wTree.get_widget("label3").set_text(_("Desktop Items"))
		self.wTree.get_widget("label5").set_text("Gnome Compositing")
		self.wTree.get_widget("checkbox_computer").set_label(_("Computer"))
		self.wTree.get_widget("checkbox_home").set_label(_("Home"))
		self.wTree.get_widget("checkbox_network").set_label(_("Network"))
		self.wTree.get_widget("checkbox_trash").set_label(_("Trash"))
		self.wTree.get_widget("checkbox_volumes").set_label(_("Mounted Volumes"))
		self.wTree.get_widget("checkbox_compositing").set_label("Gnome compositing")		
		
		# Get the current configuration
		confComputer = commands.getoutput("gconftool-2 --get /apps/nautilus/desktop/computer_icon_visible")
		if (confComputer == "true"):
			self.wTree.get_widget("checkbox_computer").set_active(1)
		confHome = commands.getoutput("gconftool-2 --get /apps/nautilus/desktop/home_icon_visible")
		if (confHome == "true"):
			self.wTree.get_widget("checkbox_home").set_active(1)
		confNetwork = commands.getoutput("gconftool-2 --get /apps/nautilus/desktop/network_icon_visible")
		if (confNetwork == "true"):
			self.wTree.get_widget("checkbox_network").set_active(1)
		confTrash = commands.getoutput("gconftool-2 --get /apps/nautilus/desktop/trash_icon_visible")
		if (confTrash == "true"):
			self.wTree.get_widget("checkbox_trash").set_active(1)
		confVolumes = commands.getoutput("gconftool-2 --get /apps/nautilus/desktop/volumes_visible")
		if (confVolumes == "true"):
			self.wTree.get_widget("checkbox_volumes").set_active(1)
		confCompositing = commands.getoutput("gconftool-2 --get /apps/metacity/general/compositing_manager")
		if (confCompositing == "true"):
			self.wTree.get_widget("checkbox_compositing").set_active(1)
					

	def applyChanges(self, widget): 
		computer_selected = self.wTree.get_widget("checkbox_computer").get_active()
		if (computer_selected == True):
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/computer_icon_visible true")
		else:
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/computer_icon_visible false")
		
		home_selected = self.wTree.get_widget("checkbox_home").get_active()
		if (home_selected == True):
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/home_icon_visible true")
		else:
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/home_icon_visible false")
		
		network_selected = self.wTree.get_widget("checkbox_network").get_active()
		if (network_selected == True):
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/network_icon_visible true")
		else:
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/network_icon_visible false")
		
		trash_selected = self.wTree.get_widget("checkbox_trash").get_active()
		if (trash_selected == True):
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/trash_icon_visible true")
		else:
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/trash_icon_visible false")
				
		volumes_selected = self.wTree.get_widget("checkbox_volumes").get_active()
		if (volumes_selected == True):
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/volumes_visible true")
		else:
			os.system("gconftool-2 --type bool --set /apps/nautilus/desktop/volumes_visible false")		
				
		compositing_selected = self.wTree.get_widget("checkbox_compositing").get_active()
		if (compositing_selected == True):
			os.system("gconftool-2 --type bool --set /apps/metacity/general/compositing_manager true")
		else:
			os.system("gconftool-2 --type bool --set /apps/metacity/general/compositing_manager false")
		
		gtk.main_quit()		
		sys.exit(0)	
			
if __name__ == "__main__":
	MintDesktop()
	gtk.main()
