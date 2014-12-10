#!/usr/bin/env python
#-*- coding:utf-8 -*-

from gettext import gettext as _

try:
    from gi.repository import GObject, Gio, Gtk, Gdk, Gedit
except ImportError as err:
    print('GEdit-AutoPEP8 need to be launched by GEdit 3')
    print(err)

try:
    import autopep8
except ImportError as err:
    print('GEdit-AutoPEP8 require autopep8 python module'
          ' from https://github.com/hhatto/autopep8')
    print(err)


class AutoPEP8AppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.menu_ext = self.extend_menu("tools-section")
        item = Gio.MenuItem.new(_("PEP8 Auto format..."), "win.autopep8")
        self.menu_ext.prepend_menu_item(item)

    def do_deactivate(self):
        self.menu_ext = None


class AutoPEP8WindowActivatable(GObject.Object, Gedit.WindowActivatable):

    window = GObject.property(type=Gedit.Window)

    def __init__(self,):
        GObject.Object.__init__(self)

    def do_activate(self):
        # Install Menu Action
        action = Gio.SimpleAction(name="autopep8")
        action.connect('activate', lambda a, p: self.on_autopep8_activate())
        self.window.add_action(action)
        self._update()

    def do_deactivate(self):
        # Remove installed menu items
        self.window.remove_action("autopep8")

    def do_update_state(self):
        self._update()

    def _update(self):
        active = False
        try:
            if self.window.get_active_document() \
                    .get_language().get_name() == 'Python':
                active = True
        except AttributeError:
            pass

        if active:
            active = self.window.get_active_tab() is not None

        self.window.lookup_action("autopep8").set_enabled(active)

    # Menu activate handlers
    def on_autopep8_activate(self):
        doc = self.window.get_active_document()
        if not doc:
            return

        try:
            encoding = doc.get_encoding().get_charset()
        except Exception as err:
            encoding = 'utf-8'
            print('Encoding err', err)

        start, end = doc.get_bounds()
        doc.set_text(autopep8.fix_code(
            doc.get_text(start, end,
                         include_hidden_chars=True).encode(encoding),
            encoding=encoding))

