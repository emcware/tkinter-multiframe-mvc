# tab4_view.py
import tkinter as tk
from tkinter import ttk


class Tab_4:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text="This is Tab 4")
        self.label.pack(padx=20, pady=20)
