# window.py

from gi.repository import Adw
from gi.repository import Gtk, Gio


@Gtk.Template(resource_path="/io/github/alexkdeveloper/baichat/ui/window.ui")
class BaichatWindow(Adw.ApplicationWindow):
    __gtype_name__ = "BaichatWindow"

    toast_overlay = Gtk.Template.Child()
    prompt_text_view = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    ask_button = Gtk.Template.Child()
    wait_button = Gtk.Template.Child()
    banner = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings(schema_id="io.github.alexkdeveloper.baichat")

        self.settings.bind(
            "width", self, "default-width", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "height", self, "default-height", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "is-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "is-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT
        )
