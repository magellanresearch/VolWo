# modules/logger.py
import tkinter as tk
from tkinter import scrolledtext, ttk
from datetime import datetime

class Logger:
    def __init__(self):
        self.entries = []           # list of (timestamp_str, message)
        self._subscribers = []      # callbacks to notify when new entry added

    def log(self, message):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{ts}  {message}"
        self.entries.append(entry)
        for cb in list(self._subscribers):
            try:
                cb(entry)
            except Exception:
                pass

    def get_all(self):
        return list(self.entries)

    def subscribe(self, callback):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback):
        if callback in self._subscribers:
            self._subscribers.remove(callback)

class LogWindow(tk.Toplevel):
    def __init__(self, parent, logger: Logger):
        super().__init__(parent)
        self.title("Application Log")
        self.geometry("800x400")
        self.logger = logger
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.create_widgets()
        # populate existing entries
        for e in self.logger.get_all():
            self._append(e)
        # subscribe to live updates
        self.logger.subscribe(self._append)

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        self.text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.NORMAL)
        self.text.pack(fill="both", expand=True)
        self.text.configure(state=tk.DISABLED)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=8, pady=(0,8))

        clear_btn = ttk.Button(btn_frame, text="Clear Log", command=self.clear_log)
        clear_btn.pack(side="left")

        save_btn = ttk.Button(btn_frame, text="Save Log As...", command=self.save_log)
        save_btn.pack(side="left", padx=6)

        close_btn = ttk.Button(btn_frame, text="Close", command=self._on_close)
        close_btn.pack(side="right")

    def _append(self, entry):
        self.text.configure(state=tk.NORMAL)
        self.text.insert(tk.END, entry + "\n")
        self.text.see(tk.END)
        self.text.configure(state=tk.DISABLED)

    def clear_log(self):
        if not tk.messagebox.askyesno("Clear Log", "Are you sure you want to clear the log?"):
            return
        self.logger.entries.clear()
        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.configure(state=tk.DISABLED)

    def save_log(self):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file","*.txt")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.logger.get_all()))
        tk.messagebox.showinfo("Saved", f"Log saved to:\n{path}")

    def _on_close(self):
        self.logger.unsubscribe(self._append)
        try:
            self.destroy()
        except Exception:
            pass
