"""TaskBreaker - GTK4/Adwaita-app för att bryta ner uppgifter."""

import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, Gtk

from taskbreaker.breakdown import break_down_task
from taskbreaker.storage import load_tasks, save_tasks


class TaskBreakerWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("TaskBreaker")
        self.set_default_size(450, 650)

        self.tasks = load_tasks()

        # Huvudlayout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(main_box)

        # Headerbar
        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="TaskBreaker"))

        clear_btn = Gtk.Button(label="Rensa allt")
        clear_btn.add_css_class("destructive-action")
        clear_btn.connect("clicked", self._on_clear_all)
        header.pack_end(clear_btn)

        main_box.append(header)

        # Innehåll med scroll
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content.set_margin_top(16)
        content.set_margin_bottom(16)
        content.set_margin_start(16)
        content.set_margin_end(16)

        # Välkomsttext
        welcome = Gtk.Label(
            label="Skriv in en uppgift som känns stor.\nJag bryter ner den åt dig!"
        )
        welcome.add_css_class("dim-label")
        welcome.set_wrap(True)
        welcome.set_justify(Gtk.Justification.CENTER)
        content.append(welcome)

        # Inmatningsrad
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("T.ex. städa rummet, plugga till provet...")
        self.entry.set_hexpand(True)
        self.entry.connect("activate", self._on_add_task)
        input_box.append(self.entry)

        add_btn = Gtk.Button(label="Bryt ner!")
        add_btn.add_css_class("suggested-action")
        add_btn.connect("clicked", self._on_add_task)
        input_box.append(add_btn)

        content.append(input_box)

        # Scrollbar för steg-listan
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.tasks_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        scroll.set_child(self.tasks_box)
        content.append(scroll)

        main_box.append(content)

        # Ladda sparade uppgifter
        self._rebuild_ui()

        # CSS för ADHD-anpassad design
        self._apply_css()

    def _apply_css(self):
        css = b"""
        window {
            font-size: 15px;
        }
        .task-title {
            font-size: 17px;
            font-weight: bold;
        }
        .step-done label {
            text-decoration: line-through;
            opacity: 0.5;
        }
        .task-card {
            padding: 12px;
            border-radius: 12px;
            background: alpha(@accent_color, 0.08);
        }
        .progress-text {
            font-size: 13px;
            font-weight: bold;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_add_task(self, _widget):
        text = self.entry.get_text().strip()
        if not text:
            return

        steps = break_down_task(text)
        task = {
            "title": text,
            "steps": [{"text": s, "done": False} for s in steps],
        }
        self.tasks.insert(0, task)
        self._save_and_rebuild()
        self.entry.set_text("")

    def _on_clear_all(self, _widget):
        self.tasks.clear()
        self._save_and_rebuild()

    def _on_step_toggled(self, check, task_idx, step_idx):
        self.tasks[task_idx]["steps"][step_idx]["done"] = check.get_active()
        save_tasks(self.tasks)
        self._rebuild_ui()

    def _on_remove_task(self, _btn, task_idx):
        self.tasks.pop(task_idx)
        self._save_and_rebuild()

    def _save_and_rebuild(self):
        save_tasks(self.tasks)
        self._rebuild_ui()

    def _rebuild_ui(self):
        # Ta bort alla barn
        while child := self.tasks_box.get_first_child():
            self.tasks_box.remove(child)

        if not self.tasks:
            empty = Gtk.Label(label="Inga uppgifter ännu.\nLägg till en ovan!")
            empty.add_css_class("dim-label")
            empty.set_margin_top(40)
            self.tasks_box.append(empty)
            return

        for task_idx, task in enumerate(self.tasks):
            card = self._build_task_card(task_idx, task)
            self.tasks_box.append(card)

    def _build_task_card(self, task_idx, task):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        card.add_css_class("task-card")

        # Rubrikrad med titel och ta bort-knapp
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        title = Gtk.Label(label=task["title"], xalign=0)
        title.add_css_class("task-title")
        title.set_hexpand(True)
        title.set_wrap(True)
        header.append(title)

        remove_btn = Gtk.Button(icon_name="user-trash-symbolic")
        remove_btn.add_css_class("flat")
        remove_btn.connect("clicked", self._on_remove_task, task_idx)
        header.append(remove_btn)

        card.append(header)

        # Framsteg
        done_count = sum(1 for s in task["steps"] if s["done"])
        total = len(task["steps"])
        progress_bar = Gtk.ProgressBar()
        progress_bar.set_fraction(done_count / total if total > 0 else 0)
        card.append(progress_bar)

        progress_label = Gtk.Label(
            label=f"{done_count}/{total} steg klara", xalign=0
        )
        progress_label.add_css_class("progress-text")
        if done_count == total:
            progress_label.set_label("Alla steg klara! Bra jobbat!")
            progress_label.add_css_class("success")
        card.append(progress_label)

        # Steg-lista
        for step_idx, step in enumerate(task["steps"]):
            step_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            step_row.set_margin_start(4)

            check = Gtk.CheckButton(label=step["text"])
            check.set_active(step["done"])
            check.connect("toggled", self._on_step_toggled, task_idx, step_idx)
            if step["done"]:
                step_row.add_css_class("step-done")

            step_row.append(check)
            card.append(step_row)

        return card


class TaskBreakerApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="se.taskbreaker.app",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = TaskBreakerWindow(application=self)
        win.present()


def main():
    app = TaskBreakerApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()
