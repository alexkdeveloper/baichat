# main.py

import sys
import gi
import threading
import socket

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk, Gio, Adw, Gdk, GLib
from .window import BaichatWindow

from .constants import app_id, version

from baichat_py import BAIChat


class BaichatApplication(Adw.Application):
    """The main application singleton class."""
    
    def __init__(self):
        super().__init__(
            application_id="io.github.alexkdeveloper.baichat",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("copy_prompt", self.on_copy_prompt_action)
        self.create_action("ask", self.on_ask_action, ["<primary>Return"])    
        self.resp = ''

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = BaichatWindow(application=self)
        self.win.present()
        
        self.win.prompt_text_view.grab_focus()

    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="BAI Chat",
            application_icon="io.github.alexkdeveloper.baichat",
            developer_name="Alex K",
            developers=["Alex K https://github.com/alexkdeveloper/baichat"],
            license_type=Gtk.License.GPL_3_0,
            version="1.0.0",
            copyright="© 2023 Alex K")
        about.present()

    def on_copy_prompt_action(self, widget, _):

        toast = Adw.Toast()

        text = self.win.prompt_text_view.get_buffer()
        toast.set_title("Text copied")

        (start, end) = text.get_bounds()
        text = text.get_text(start, end, False)

        if len(text) == 0:
            return

        Gdk.Display.get_default().get_clipboard().set(text)

        self.win.toast_overlay.add_toast(toast)

    def ask(self, prompt):
        chat = BAIChat(sync=True)
        try:
            response = chat.sync_ask(self.prompt)
        except KeyError:
            self.win.banner.set_revealed(False)
            return ""
        except socket.gaierror:
            self.win.banner.set_revealed(True)
            return ""
        else:
            self.win.banner.set_revealed(False)
            return response.text

    def on_ask_action(self, widget, _):

        self.prompt = self.win.prompt_text_view.get_buffer().props.text
        if self.prompt == "" or self.prompt is None: 
           return
            
        self.win.spinner.start()
        self.win.ask_button.set_visible(False)
        self.win.wait_button.set_visible(True)

        def thread_run():
            response = self.ask(self.prompt)
            GLib.idle_add(cleanup, response)

        def cleanup(response):
            self.win.spinner.stop()
            self.win.ask_button.set_visible(True)
            self.win.wait_button.set_visible(False)
            t.join()
            
            self.resp = self.prompt + '\n\n******\n\n' + response + '\n\n******\n\n'
            self.win.prompt_text_view.get_buffer().set_text(self.resp)

        t = threading.Thread(target=thread_run)
        t.start()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    app = BaichatApplication()
    return app.run(sys.argv)
