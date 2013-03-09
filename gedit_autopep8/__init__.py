from gettext import gettext as _

try:
    from gi.repository import GObject, Gtk, Gedit
except ImportError, err:
    print 'GEdit-AutoPEP8 need to be launched by GEdit 3'
    print err

try:
    import autopep8
except ImportError, err:
    print ('GEdit-AutoPEP8 require autopep8 python module'
           ' from https://github.com/hhatto/autopep8')
    print err

# Menu item example, insert a new item in the Tools menu_
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="Auto PEP8" action="AutoPEP8" />
      </placeholder>
    </menu>
  </menubar>
</ui>
"""


class AutoPEP8WindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "AutoPEP8WindowActivatable"

    window = GObject.property(type=Gedit.Window)

    def __init__(self,):
        GObject.Object.__init__(self)

    def do_activate(self):
        # Insert menu items
        self._insert_menu()

    def do_deactivate(self):
        # Remove any installed menu items
        self._remove_menu()

        self._action_group = None

    def _insert_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Create a new action group
        self._action_group = Gtk.ActionGroup("AutoPEP8PluginActions")
        self._action_group.add_actions([("AutoPEP8", None, _("Auto PEP8"),
                                         '<Control><Shift>R',
                                         _("Reformat with Auto PEP8"),
                                         self.on_autopep8_activate)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def do_update_state(self):
        active = False
        try:
            if self.window.get_active_document() \
                    .get_language().get_name() == 'Python':
                active = True
        except AttributeError:
            pass

        self._action_group.set_sensitive(active)

    # Menu activate handlers
    def on_autopep8_activate(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return

        try:
            encoding = self.document.get_encoding().get_charset()
        except Exception:
            encoding = 'utf-8'

        start, end = doc.get_bounds()
        doc.set_text(autopep8.fix_string(unicode(
            doc.get_text(start, end,
                         include_hidden_chars=True), encoding)))

