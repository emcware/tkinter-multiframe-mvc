# tab2_view.py
import tkinter as tk
from tkinter import ttk

class Tab_2:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text="This is Tab 2")
        self.label.pack(padx=20, pady=20)

