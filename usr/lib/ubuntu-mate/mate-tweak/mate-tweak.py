#!/usr/bin/env python2

import gi
 
from gi.repository import Gtk, GdkPixbuf, Gdk, GObject
from gi.repository import Gio

try:
    import os
    import commands
    import sys
    import string
    import gettext
except Exception, detail:
    print detail
    sys.exit(1)


# i18n
# TODO: Badly need to fix this - overuse of "The" etc.
gettext.install("mate-tweak", "/usr/share/ubuntu-mate/locale")

class SidePage:
    def __init__(self, notebook_index, name, icon):
        self.notebook_index = notebook_index
        self.name = name
        self.icon = icon

class MateTweak:

    def set_string(self, schema, key, value):
        settings = Gio.Settings.new(schema)
        settings.set_string(key, value)

    def get_string(self, schema, key):
        settings = Gio.Settings.new(schema)
        return settings.get_string(key)

    def set_bool(self, schema, key, value):
        settings = Gio.Settings.new(schema)
        settings.set_boolean(key, value.get_active())
    
    def get_bool(self, schema, key):
        settings = Gio.Settings.new(schema)
        return settings.get_boolean(key)
    
    def init_checkbox(self, schema, key, name):
        source = Gio.SettingsSchemaSource.get_default()
        if source.lookup(schema, True) != None:
            widget = self.builder.get_object(name)
            value = self.get_bool(schema, key)
            widget.set_active(value)
            widget.connect("clicked", lambda x: self.set_bool(schema, key, x))       

    def init_combobox(self, schema, key, name):
        source = Gio.SettingsSchemaSource.get_default()
        if source.lookup(schema, True) != None:
            widget = self.builder.get_object(name)
            conf = self.get_string(schema, key)
            index = 0
            for row in widget.get_model():
                if(conf == row[1]):
                    widget.set_active(index)
                    break
                index = index +1
            widget.connect("changed", lambda x: self.combo_fallback(schema, key, x))

    def combo_fallback(self, schema, key, widget):
        act = widget.get_active()
        value = widget.get_model()[act]
        self.set_string(schema, key, value[1])

    # Change pages
    def side_view_nav(self, param):
        treePaths = param.get_selected_items()
        if (len(treePaths) > 0):
            treePath = treePaths[0]
            index = int("%s" % treePath) #Hack to turn treePath into an int
            target = self.sidePages[index].notebook_index
            self.builder.get_object("notebook1").set_current_page(target)

    ''' Create the UI '''
    def __init__(self):
        # load our glade ui file in
        self.builder = Gtk.Builder()
        self.builder.add_from_file('/usr/lib/ubuntu-mate/mate-tweak/mate-tweak.ui')
        self.window = self.builder.get_object( "main_window" )
               
        self.builder.get_object("main_window").connect("destroy", Gtk.main_quit)
                      
        side_desktop_options = SidePage(0, _("Desktop"), "user-desktop")
        side_windows = SidePage(1, _("Windows"), "preferences-system-windows")
        side_interface = SidePage(2, _("Interface"), "preferences-desktop")

        # TODO - Review this when Compiz is running.
        if "Marco" in commands.getoutput("wmctrl -m"):
            self.sidePages = [side_desktop_options, side_interface, side_windows]
        else:
            self.sidePages = [side_desktop_options, side_interface]
            self.builder.get_object("frame_marco1").hide()
            self.builder.get_object("frame_marco2").hide()
        
        # create the backing store for the side nav-view.
        theme = Gtk.IconTheme.get_default()
        self.store = Gtk.ListStore(str, GdkPixbuf.Pixbuf)
        for sidePage in self.sidePages:
            img = theme.load_icon(sidePage.icon, 36, 0)
            self.store.append([sidePage.name, img])

        target = self.sidePages[0].notebook_index
        self.builder.get_object("notebook1").set_current_page(target)

        # set up the side view - navigation.
        self.builder.get_object("side_view").set_text_column(0)
        self.builder.get_object("side_view").set_pixbuf_column(1)
        self.builder.get_object("side_view").set_model(self.store)
        self.builder.get_object("side_view").select_path(Gtk.TreePath.new_first())
        self.builder.get_object("side_view").connect("selection_changed", self.side_view_nav )

        # set up larger components.
        self.builder.get_object("main_window").set_title("MATE Tweak")
        self.builder.get_object("main_window").connect("destroy", Gtk.main_quit)

        # i18n
        self.builder.get_object("label_desktop_icons").set_markup("<b>" + _("Desktop icons") + "</b>")
        self.builder.get_object("label_performance").set_markup("<b>" + _("Performance") + "</b>")
        self.builder.get_object("label_appearance").set_markup("<b>" + _("Appearance") + "</b>")
        self.builder.get_object("label_icons").set_markup("<b>" + _("Icons") + "</b>")
        self.builder.get_object("label_context_menus").set_markup("<b>" + _("Context menus") + "</b>")
        self.builder.get_object("label_toolbars").set_markup("<b>" + _("Toolbars") + "</b>")
        self.builder.get_object("label_wm").set_markup("<b>" + _("Window Manager") + "</b>")

        self.builder.get_object("caption_desktop_icons").set_markup("<small><i><span foreground=\"#555555\">" + _("Select the items you want to see on the desktop:") + "</span></i></small>")

        self.builder.get_object("checkbox_computer").set_label(_("Computer"))
        self.builder.get_object("checkbox_home").set_label(_("Home"))
        self.builder.get_object("checkbox_network").set_label(_("Network"))
        self.builder.get_object("checkbox_trash").set_label(_("Trash"))
        self.builder.get_object("checkbox_volumes").set_label(_("Mounted Volumes"))

        self.builder.get_object("checkbutton_resources").set_label(_("Don't show window content while dragging them"))
        self.builder.get_object("checkbox_compositing").set_label(_("Use compositing"))
        self.builder.get_object("checkbutton_titlebar").set_label(_("Use system font in titlebar"))

        self.builder.get_object("label_layouts").set_text(_("Buttons layout:"))

        self.builder.get_object("label_window_manager").set_text(_("Window manager:"))

        self.builder.get_object("checkbutton_menuicon").set_label(_("Show icons on menus"))
        self.builder.get_object("checkbutton_button_icons").set_label(_("Show icons on buttons"))
        self.builder.get_object("checkbutton_im_menu").set_label(_("Show Input Methods menu in context menus"))
        self.builder.get_object("checkbutton_unicode").set_label(_("Show Unicode Control Character menu in context menus"))

        self.builder.get_object("label_tool_icons").set_text(_("Buttons labels:"))
        self.builder.get_object("label_icon_size").set_text(_("Icon size:"))

        # Desktop page
        self.init_checkbox("org.mate.caja.desktop", "computer-icon-visible", "checkbox_computer")
        self.init_checkbox("org.mate.caja.desktop", "home-icon-visible", "checkbox_home")
        self.init_checkbox("org.mate.caja.desktop", "network-icon-visible", "checkbox_network")
        self.init_checkbox("org.mate.caja.desktop", "trash-icon-visible", "checkbox_trash")
        self.init_checkbox("org.mate.caja.desktop", "volumes-visible", "checkbox_volumes")

        # Window Manager page
        self.init_checkbox("org.mate.Marco.general", "reduced-resources", "checkbutton_resources")
        self.init_checkbox("org.mate.Marco.general", "compositing-manager", "checkbox_compositing")
        self.init_checkbox("org.mate.Marco.general", "titlebar-uses-system-font", "checkbutton_titlebar")

        # interface page
        self.init_checkbox("org.mate.interface", "menus-have-icons", "checkbutton_menuicon")
        self.init_checkbox("org.mate.interface", "show-input-method-menu","checkbutton_im_menu")
        self.init_checkbox("org.mate.interface", "show-unicode-menu", "checkbutton_unicode")
        self.init_checkbox("org.mate.interface", "buttons-have-icons", "checkbutton_button_icons")
        
        iconSizes = Gtk.ListStore(str, str)
        iconSizes.append([_("Small"), "small-toolbar"])
        iconSizes.append([_("Large"), "large-toolbar"])
        self.builder.get_object("combobox_icon_size").set_model(iconSizes)
        self.init_combobox("org.mate.interface", "toolbar-icons-size", "combobox_icon_size")

        # Metacity button layouts..
        layouts = Gtk.ListStore(str, str)
        layouts.append([_("Traditional style (Right)"), "menu:minimize,maximize,close"])
        layouts.append([_("Mac style (Left)"), "close,minimize,maximize:"])
        self.builder.get_object("combo_wmlayout").set_model(layouts)
        self.init_combobox("org.mate.Marco.general", "button-layout", "combo_wmlayout")

        wms = Gtk.ListStore(str, str)
        wms.append([_("Marco (stable and reliable)"), "marco"])
        wms.append([_("Compiz (impressive desktop effects)"), "compiz"])
        self.builder.get_object("combo_wm").set_model(wms)
        self.builder.get_object("combo_wm").set_tooltip_text(_("Log out and log back in for changes to take effect."))
        self.init_combobox("org.mate.session.required-components", "windowmanager", "combo_wm")

        # toolbar icon styles
        iconStyles = Gtk.ListStore(str, str)
        iconStyles.append([_("Text below items"), "both"])
        iconStyles.append([_("Text beside items"), "both-horiz"])
        iconStyles.append([_("Icons only"), "icons"])
        iconStyles.append([_("Text only"), "text"])
        self.builder.get_object("combobox_toolicons").set_model(iconStyles)
        self.init_combobox("org.mate.interface", "toolbar-style", "combobox_toolicons")

        self.builder.get_object("main_window").show()       

    
if __name__ == "__main__":
    MateTweak()
    Gtk.main()
