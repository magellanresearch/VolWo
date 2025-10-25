import tkinter as tk
from tkinter import ttk

class ProgressBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.bar = ttk.Progressbar(self, mode="indeterminate")
        self.bar.pack(fill="x")

    def start(self):
        self.bar.start()

    def complete(self):
        self.bar.stop()
