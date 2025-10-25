# modules/data_manager.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from modules.data_fetcher import fetch_data

class DataManagerWindow(tk.Toplevel):
    def __init__(self, parent, data_cache=None, logger=None):
        super().__init__(parent)
        self.title("Data Manager")
        self.geometry("600x400")
        self.parent = parent
        self.logger = logger
        self.data_cache = data_cache or {}
        self.create_widgets()
        self.populate_listbox()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Listbox with scrollbar showing downloaded tickers
        lb_frame = ttk.Frame(frame)
        lb_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(lb_frame, height=12, selectmode=tk.SINGLE)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(lb_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Entry to add a new ticker
        entry_frame = ttk.Frame(frame)
        entry_frame.pack(fill="x", pady=8)

        ttk.Label(entry_frame, text="New ticker:").pack(side="left")
        self.ticker_entry = ttk.Entry(entry_frame)
        self.ticker_entry.pack(side="left", padx=6, fill="x", expand=True)
        add_button = ttk.Button(entry_frame, text="Add and Download", command=self.add_and_download)
        add_button.pack(side="left", padx=6)

        # Buttons: Download selected to Excel, Refresh list, Remove selected
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=8)

        self.down_to_excel_btn = ttk.Button(btn_frame, text="Save Selected to Excel", command=self.save_selected_to_excel)
        self.down_to_excel_btn.pack(side="left", padx=4)

        refresh_btn = ttk.Button(btn_frame, text="Refresh List", command=self.populate_listbox)
        refresh_btn.pack(side="left", padx=4)

        remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=self.remove_selected)
        remove_btn.pack(side="left", padx=4)

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        # show tickers present in data_cache
        tickers = sorted(self.data_cache.keys())
        for t in tickers:
            self.listbox.insert(tk.END, t)

    def add_and_download(self):
        ticker = self.ticker_entry.get().strip().upper()
        if not ticker:
            messagebox.showinfo("Input", "Please enter a ticker symbol.")
            return
        try:
            self.logger and self.logger.log(f"Downloading ticker {ticker}...")
            df = fetch_data(tickers=[ticker], period="max").get(ticker)
            if df is None or df.empty:
                raise ValueError("No data returned for ticker.")
            # store in both local cache and parent's cache if available
            self.data_cache[ticker] = df
            if hasattr(self.parent, "data_cache"):
                self.parent.data_cache[ticker] = df
            self.populate_listbox()
            self.logger and self.logger.log(f"Downloaded {ticker} with {len(df)} rows.")
            messagebox.showinfo("Downloaded", f"{ticker} downloaded successfully.")
        except Exception as e:
            self.logger and self.logger.log(f"Download failed for {ticker}: {e}")
            messagebox.showerror("Download Error", f"Failed to download {ticker}:\n{e}")

    def save_selected_to_excel(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Selection", "Please select a ticker from the list.")
            return
        ticker = self.listbox.get(sel[0])
        df = self.data_cache.get(ticker)
        if df is None:
            messagebox.showerror("Data Error", "Data for selected ticker is not available.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=f"{ticker}.xlsx",
                                                filetypes=[("Excel workbook", "*.xlsx")])
        if not filepath:
            return
        try:
            # write to excel with sheet name = ticker
            with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=ticker, index=True)
            self.logger and self.logger.log(f"Saved {ticker} to {filepath}")
            messagebox.showinfo("Saved", f"{ticker} saved to:\n{filepath}")
        except Exception as e:
            self.logger and self.logger.log(f"Save failed for {ticker}: {e}")
            messagebox.showerror("Save Error", f"Failed to save {ticker}:\n{e}")

    def remove_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Selection", "Please select a ticker to remove.")
            return
        ticker = self.listbox.get(sel[0])
        if messagebox.askyesno("Remove", f"Remove {ticker} from downloaded data?"):
            self.data_cache.pop(ticker, None)
            if hasattr(self.parent, "data_cache"):
                self.parent.data_cache.pop(ticker, None)
            self.populate_listbox()
            self.logger and self.logger.log(f"Removed {ticker} from data cache.")
