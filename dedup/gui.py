import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import threading
from .core import find_duplicates

class DedupApp:
    def __init__(self):
        self.window = Gtk.Window(title="Dedup")
        self.window.set_default_size(700, 500)
        self.window.connect("destroy", Gtk.main_quit)

        vbox = Gtk.VBox(margin=10, spacing=10)
        self.window.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Rutas separadas por comas: /home/user/Docs,/home/user/Descargas")
        btn = Gtk.Button(label="Escanear")
        btn.connect("clicked", self.on_scan)
        vbox.pack_start(self.entry, False, False, 0)
        vbox.pack_start(btn, False, False, 0)

        self.progress = Gtk.ProgressBar()
        vbox.pack_start(self.progress, False, False, 0)

        self.store = Gtk.ListStore(str, str)
        tree = Gtk.TreeView(model=self.store)
        for i, t in enumerate(["Hash", "Ruta"]):
            r = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(t, r, text=i)
            tree.append_column(col)
        scroll = Gtk.ScrolledWindow()
        scroll.add(tree)
        vbox.pack_start(scroll, True, True, 0)

        self.window.show_all()

    def on_scan(self, btn):
        text = self.entry.get_text()
        paths = [p.strip() for p in text.split(",") if p.strip()]
        if not paths:
            return
        self.store.clear()
        self.progress.set_fraction(0.0)
        threading.Thread(target=self._scan_bg, args=(paths,), daemon=True).start()

    def _scan_bg(self, paths):
        dups = find_duplicates(paths)
        total = sum(len(v) for v in dups.values())
        count = 0
        for h, filelist in dups.items():
            for f in filelist:
                count += 1
                GLib.idle_add(self.store.append, [h[:12]+"...", f])
                if total > 0:
                    GLib.idle_add(self.progress.set_fraction, min(count / total, 1.0))

def main():
    DedupApp()
    Gtk.main()
