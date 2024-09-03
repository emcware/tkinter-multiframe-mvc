# tab1_view.py
import tkinter as tk
from tkinter import ttk


class Tab_1:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)

        # Labels to display task progress
        self.table_label = ttk.Label(self.frame, text="Table Rotation: Waiting...")
        self.table_label.grid(row=0, column=0, pady=10, sticky="w")

        self.tower_label = ttk.Label(self.frame, text="Tower Height: Waiting...")
        self.tower_label.grid(row=1, column=0, pady=10, sticky="w")

        self.instrument_label = ttk.Label(self.frame, text="Instrument Reading: Waiting...")
        self.instrument_label.grid(row=2, column=0, pady=10, sticky="w")

        # Buttons to start tasks
        self.table_button = ttk.Button(self.frame, text="Start Table Rotation")
        self.table_button.grid(row=3, column=0, padx=10, pady=5)

        self.tower_button = ttk.Button(self.frame, text="Start Tower Movement")
        self.tower_button.grid(row=4, column=0, padx=10, pady=5)

        self.instrument_button = ttk.Button(self.frame, text="Start Instrument Reading")
        self.instrument_button.grid(row=5, column=0, padx=10, pady=5)

        # Abort button
        self.abort_button = ttk.Button(self.frame, text="Abort", state=tk.DISABLED)
        self.abort_button.grid(row=6, column=0, padx=10, pady=5)

    def disable_buttons(self):
        self.table_button.config(state=tk.DISABLED)
        self.tower_button.config(state=tk.DISABLED)
        self.instrument_button.config(state=tk.DISABLED)
        self.abort_button.config(state=tk.NORMAL)

    def enable_buttons(self):
        self.table_button.config(state=tk.NORMAL)
        self.tower_button.config(state=tk.NORMAL)
        self.instrument_button.config(state=tk.NORMAL)
        self.abort_button.config(state=tk.DISABLED)
