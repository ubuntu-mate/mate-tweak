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
menuName = _("Desktop Configuration Tool")
menuGenericName = _("Gnome Settings")
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

	# Change pages
	def side_view_nav(self, param):
		path = param.get_selected_items()
		if (len(path) > 0):
			selection = path[0][0]			
			self.get_widget("notebook1").set_current_page(selection)

	''' Create the UI '''
	def __init__(self):
		# load our glade ui file in
		self.gladefile = '/usr/lib/linuxmint/mintDesktop/mintDesktop.glade'
		self.wTree = gtk.glade.XML(self.gladefile, "main_window") 
		self.get_widget("main_window").connect("destroy", gtk.main_quit)

		# say hi to gconf
		client = gconf.client_get_default()
		client.add_dir("/apps/nautilus/desktop", gconf.CLIENT_PRELOAD_NONE)
		client.add_dir("/apps/metacity/general", gconf.CLIENT_PRELOAD_NONE)
		client.add_dir("/desktop/gnome/interface", gconf.CLIENT_PRELOAD_NONE)
		client.add_dir("/apps/nautilus/preferences", gconf.CLIENT_PRELOAD_NONE)

		# get the icon theme.
		theme = gtk.icon_theme_get_default()
		img = theme.load_icon("user-desktop", 36, 0)
		# create the backing store for the side nav-view. very perty.
		self.store = gtk.ListStore(str, gtk.gdk.Pixbuf)
		self.store.append(["Desktop", img])
		img = theme.load_icon("gnome-windows", 36, 0)
		self.store.append(["Window Manager", img])
		img = theme.load_icon("preferences-desktop", 36, 0)
		self.store.append(["Interface", img])
		img = theme.load_icon("preferences-desktop-wallpaper", 36, 0)

		# set up the side view - navigation.
      		self.get_widget("side_view").set_text_column(0)
        	self.get_widget("side_view").set_pixbuf_column(1)
		self.get_widget("side_view").set_model(self.store)
		self.get_widget("side_view").select_path((0,))
		self.get_widget("side_view").connect("selection_changed", self.side_view_nav )

		# set up larger components.
		self.get_widget("main_window").set_title("Desktop Configuration")
		self.get_widget("main_window").connect("destroy", gtk.main_quit)
		self.get_widget("button_cancel").connect("clicked", gtk.main_quit)

		# i18n
		self.get_widget("label3").set_text(_("Desktop Items"))
		self.get_widget("label5").set_text("Window Manager Tweaks")
		self.get_widget("checkbox_computer").set_label(_("Computer"))
		self.get_widget("checkbox_home").set_label(_("Home"))
		self.get_widget("checkbox_network").set_label(_("Network"))
		self.get_widget("checkbox_trash").set_label(_("Trash"))
		self.get_widget("checkbox_volumes").set_label(_("Mounted Volumes"))
		self.get_widget("checkbox_compositing").set_label("Gnome compositing")		

		# Desktop page
		self.init_checkbox("/apps/nautilus/desktop/computer_icon_visible", "checkbox_computer")
		self.init_checkbox("/apps/nautilus/desktop/home_icon_visible", "checkbox_home")
		self.init_checkbox("/apps/nautilus/desktop/network_icon_visible", "checkbox_network")
		self.init_checkbox("/apps/nautilus/desktop/trash_icon_visible", "checkbox_trash")
		self.init_checkbox("/apps/nautilus/desktop/volumes_visible", "checkbox_volumes")

		# Window Manager page
		self.init_checkbox("/apps/metacity/general/reduced_resources", "checkbutton_resources")
		self.init_checkbox("/apps/metacity/general/compositing_manager", "checkbox_compositing")
		self.init_checkbox("/apps/metacity/general/titlebar_uses_system_font", "checkbutton_titlebar")

		# interface page
		self.init_checkbox("/desktop/gnome/interface/menus_have_icons", "checkbutton_menuicon")
		self.init_checkbox("/desktop/gnome/interface/menus_have_tearoff", "checkbutton_menu_tearoff")
		self.init_checkbox("/desktop/gnome/interface/menubar_detachable","checkbutton_menubarmove")
		self.init_checkbox("/desktop/gnome/interface/toolbar_detachable", "checkbutton_toolbar_detach")
		self.init_checkbox("/desktop/gnome/interface/show_input_method_menu","checkbutton_im_menu")
		self.init_checkbox("/desktop/gnome/interface/show_unicode_menu", "checkbutton_unicode")
		self.init_checkbox("/desktop/gnome/interface/buttons_have_icons", "checkbutton_button_icons")
		self.init_checkbox("/desktop/gnome/interface/enable_animations", "checkbutton_animations")

		iconSizes = gtk.ListStore(str, str)
		iconSizes.append(["Small", "small-toolbar"])
		iconSizes.append(["Large", "large-toolbar"])
		self.get_widget("combobox_icon_size").set_model(iconSizes)
		self.init_combobox("/desktop/gnome/interface/toolbar_icons_size", "combobox_icon_size")

		# Metacity button layouts..
		layouts = gtk.ListStore(str, str)
		layouts.append(["Left", "minimize,maximize,close:menu"])
		layouts.append(["Left (Inverted)", "close,minimize,maximize:menu"])
		layouts.append(["Right", "menu:minimize,maximize,close"])
		self.get_widget("combo_wmlayout").set_model(layouts)
		self.init_combobox("/apps/metacity/general/button_layout", "combo_wmlayout")

		# toolbar icon styles
		iconStyles = gtk.ListStore(str, str)
		iconStyles.append(["Text below items", "both"])
		iconStyles.append(["Text beside items", "both-horiz"])
		iconStyles.append(["Icons only", "icons"])
		iconStyles.append(["Text only", "text"])
		self.get_widget("combobox_toolicons").set_model(iconStyles)
		self.init_combobox("/desktop/gnome/interface/toolbar_style", "combobox_toolicons")

		# demo stuff (for the interface tab)
		self.get_widget("toolbar1").add(gtk.ToolButton(gtk.STOCK_NEW))
		self.get_widget("toolbar1").add(gtk.ToolButton(gtk.STOCK_OPEN))
		self.get_widget("toolbar1").add(gtk.ToolButton(gtk.STOCK_SAVE))
		self.get_widget("toolbar1").show_all()

		self.get_widget("main_window").show()

	''' Saves typing self.get_widget all the time.... '''
	def get_widget(self, which):
		return self.wTree.get_widget(which)


	''' Initialise the CheckButton with a gconf value, then bind it with the gconf system '''
	def init_checkbox(self, key, name):
		widget = self.get_widget(name)
		conf = self.get_bool(key)
		widget.set_active(conf)
		widget.connect("clicked", lambda x: self.set_bool(key, x))
		self.add_notify(key, widget)

	''' Bind the ComboBox to gconf and assign the action '''
	def init_combobox(self, key, name):
		widget = self.get_widget(name)
		conf = self.get_string(key)
		index = 0
		for row in widget.get_model():
			if(conf == row[1]):
				widget.set_active(index)
				break
			index = index +1
		widget.connect("changed", lambda x: self.combo_fallback(key, x))
	
	''' Fallback for all combo boxes '''	
	def combo_fallback(self, key, widget):
		act = widget.get_active()
		value = widget.get_model()[act]
		self.set_string(key, value[1])

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
		# combobox, multiple targets..
		elif( type(widget) == gtk.ComboBox ):
			# Sanity check, if its crap ignore it.
			if(entry.value.type == gconf.VALUE_STRING):
				if(not widget and not value):
					return
			# the string in question :)
			value = entry.value.get_string()
			for row in widget.get_model():
				if(value == row[1]):
					widget.set_active(index)
					break
				index = index +1
if __name__ == "__main__":
	MintDesktop()
	gtk.main()

