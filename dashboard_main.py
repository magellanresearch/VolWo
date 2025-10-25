# dashboard_main.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from modules.data_fetcher import fetch_data
from modules.signal_detector import detect_signals
from modules.exporter import export_to_xlsx
from modules.progress import ProgressBar
from modules.utils import get_status_date
from modules.data_manager import DataManagerWindow
from modules.logger import Logger, LogWindow
import os
from PIL import Image, ImageTk

class VolatilityDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Volatility Dashboard")
        self.geometry("1200x800")
        self.configure(bg="black")
        IMAGE_PATH = r"C:\Magellan\VolWo\program\welt.png"  # case-sensitive Pfad: überprüfe Groß-/Kleinschreibung

        # Logger initialisieren, damit _load_background_image darauf zugreifen kann
        self.logger = Logger()  # falls du einen anderen Logger-Namen verwendest, anpassen

        # Attributes for background image
        self.bg_image_orig = None
        self.bg_photo = None
        self.bg_label = tk.Label(self, bg="black")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Restliche Initialisierung
        self.signals = []
        self.data_cache = {}
        self.last_update = None

        self.create_menu()
        self.create_widgets()

        # Lade Hintergrundbild (als Methode der Klasse)
        self._load_background_image()

    def _load_background_image(self):
        try:
            if not os.path.isfile(IMAGE_PATH):
                self.logger.log(f"Background image not found: {IMAGE_PATH}")
                return
            img = Image.open(IMAGE_PATH).convert("RGBA")
            self.bg_image_orig = img
            self._update_background_image()
            self.bind("<Configure>", lambda e: self._update_background_image())
            self.logger.log("Background image loaded.")
        except Exception as e:
            self.logger.log(f"Failed to load background image: {e}")

    def _update_background_image(self):
        if not self.bg_image_orig:
            return
        try:
            w = max(1, self.winfo_width())
            h = max(1, self.winfo_height())
            img = self.bg_image_orig.copy()
            img_ratio = img.width / img.height
            win_ratio = w / h
            if win_ratio > img_ratio:
                new_w = w
                new_h = int(w / img_ratio)
            else:
                new_h = h
                new_w = int(h * img_ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 80))
            img = Image.alpha_composite(img, overlay)
            self.bg_photo = ImageTk.PhotoImage(img)
            self.bg_label.config(image=self.bg_photo)
            self.bg_label.image = self.bg_photo
        except Exception as e:
            self.logger.log(f"Failed to update background image: {e}")

        self.logger = Logger()        # in-memory logger (no visible widget by default)
        self.log_window = None

        self.signals = []
        self.data_cache = {}
        self.last_update = None

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self)

        # File menu with Log submenu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open...", command=self.menu_file_open)
        file_menu.add_command(label="Save As...", command=self.menu_file_save_as)

        # Submenu: Log
        log_submenu = tk.Menu(file_menu, tearoff=0)
        log_submenu.add_command(label="Show Log", command=self.menu_file_log)
        file_menu.add_cascade(label="Log", menu=log_submenu)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.menu_exit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Other menus
        vix_menu = tk.Menu(menubar, tearoff=0)
        vix_menu.add_command(label="Show VIX Chart", command=self.menu_vix_show)
        vix_menu.add_command(label="Download VIX Data", command=self.menu_vix_download)
        menubar.add_cascade(label="VIX", menu=vix_menu)

        vf_menu = tk.Menu(menubar, tearoff=0)
        vf_menu.add_command(label="Show VIX-Futures Curve", command=self.menu_vf_show)
        vf_menu.add_command(label="Compare Front Month", command=self.menu_vf_compare)
        menubar.add_cascade(label="VIX-Future", menu=vf_menu)

        strat_menu = tk.Menu(menubar, tearoff=0)
        strat_menu.add_command(label="List Strategies", command=self.menu_strategies_list)
        strat_menu.add_command(label="Reload Strategies", command=self.menu_strategies_reload)
        menubar.add_cascade(label="Strategies", menu=strat_menu)

        lit_menu = tk.Menu(menubar, tearoff=0)
        lit_menu.add_command(label="Open Papers Folder", command=self.menu_literature_open)
        lit_menu.add_command(label="Search Literature", command=self.menu_literature_search)
        menubar.add_cascade(label="Literature", menu=lit_menu)

        dm_menu = tk.Menu(menubar, tearoff=0)
        dm_menu.add_command(label="Open Data Manager", command=self.menu_data_manager)
        menubar.add_cascade(label="DataManager", menu=dm_menu)

        exit_menu = tk.Menu(menubar, tearoff=0)
        exit_menu.add_command(label="Quit", command=self.menu_exit)
        menubar.add_cascade(label="Exit", menu=exit_menu)

        self.config(menu=menubar)

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=8, pady=8)

        self.status_label = ttk.Label(top_frame, text="Status: Idle", foreground="white", background="black")
        self.status_label.pack(side="left")

        self.last_update_label = ttk.Label(top_frame, text="Last update: Never", foreground="white", background="black")
        self.last_update_label.pack(side="right")

        self.update_button = ttk.Button(self, text="Update Data", command=self.update_data)
        self.update_button.pack(padx=8, anchor="ne")

        self.progress = ProgressBar(self)
        self.progress.pack(pady=5, fill="x", padx=10)

        # No inline log panel anymore

        self.export_button = ttk.Button(self, text="Export XLSX", command=self.export_data)
        self.export_button.pack(pady=10)

    def update_data(self):
        try:
            self.logger.log("Manual update started...")
            self.status_label.config(text="Status: Updating...")
            self.update_button.config(state="disabled")
            self.progress.start()
            start = datetime.now()

            data = fetch_data()
            self.data_cache = data
            signals = detect_signals(data)
            self.signals = signals

            self.last_update = datetime.now()
            last_update_str = self.last_update.strftime("%Y-%m-%d %H:%M:%S")
            self.last_update_label.config(text=f"Last update: {last_update_str}")

            status_date = get_status_date(data)
            self.status_label.config(text=f"Status Date: {status_date}")

            elapsed = (datetime.now() - start).total_seconds()
            self.logger.log(f"Update complete in {elapsed:.2f}s.")
        except Exception as e:
            self.logger.log(f"Update failed: {e}")
            messagebox.showerror("Update Error", f"Failed to update data:\n{e}")
        finally:
            self.progress.complete()
            self.update_button.config(state="normal")

    def export_data(self):
        if not self.signals:
            messagebox.showinfo("Export", "No signals/data to export. Please update first.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if filepath:
            try:
                export_to_xlsx(self.signals, filepath)
                self.logger.log(f"Exported to {filepath}")
            except Exception as e:
                self.logger.log(f"Export failed: {e}")
                messagebox.showerror("Export Error", f"Failed to export:\n{e}")

    # DataManager menu callback
    def menu_data_manager(self):
        DataManagerWindow(self, data_cache=self.data_cache, logger=self.logger)

    # File -> Log
    def menu_file_log(self):
        if self.log_window and tk.Toplevel.winfo_exists(self.log_window):
            # bring to front
            self.log_window.lift()
            return
        self.log_window = LogWindow(self, logger=self.logger)

    # --- other menu placeholders ---
    def menu_file_open(self):
        path = filedialog.askopenfilename()
        if path:
            self.logger.log(f"Opened file: {path}")

    def menu_file_save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            self.logger.log(f"Saved file as: {path}")

    def menu_vix_show(self):
        self.logger.log("VIX chart requested")
        messagebox.showinfo("VIX", "VIX chart function not implemented yet")

    def menu_vix_download(self):
        self.logger.log("VIX data download requested")
        messagebox.showinfo("VIX", "VIX download function not implemented yet")

    def menu_vf_show(self):
        self.logger.log("VIX-Futures curve requested")
        messagebox.showinfo("VIX-Future", "VIX-Futures curve function not implemented yet")

    def menu_vf_compare(self):
        self.logger.log("VIX-Futures front month comparison requested")
        messagebox.showinfo("VIX-Future", "Compare front month function not implemented yet")

    def menu_strategies_list(self):
        self.logger.log("List strategies requested")
        messagebox.showinfo("Strategies", "List Strategies function not implemented yet")

    def menu_strategies_reload(self):
        self.logger.log("Reload strategies requested")
        messagebox.showinfo("Strategies", "Reload Strategies function not implemented yet")

    def menu_literature_open(self):
        self.logger.log("Open literature folder requested")
        messagebox.showinfo("Literature", "Open Papers Folder function not implemented yet")

    def menu_literature_search(self):
        self.logger.log("Search literature requested")
        messagebox.showinfo("Literature", "Search Literature function not implemented yet")

    def menu_exit(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = VolatilityDashboard()
    app.mainloop()
