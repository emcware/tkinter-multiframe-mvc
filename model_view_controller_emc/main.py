# main.py
import tkinter as tk
from tkinter import ttk
from tab1_controller import Tab_1_Controller
from tab2_view import Tab_2
from tab3_view import Tab_3
from tab4_view import Tab_4


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Application with 4 Tabs")
        self.root.geometry("1100x800+100+100")

        self.notebook = ttk.Notebook(self.root)

        # Instantiate each tab controller/view
        self.tab1 = Tab_1_Controller(self.notebook)
        self.tab2 = Tab_2(self.notebook)
        self.tab3 = Tab_3(self.notebook)
        self.tab4 = Tab_4(self.notebook)

        # Add the tabs to the notebook (tab container)
        self.notebook.add(self.tab1.view.frame, text="Tab 1")
        self.notebook.add(self.tab2.frame, text="Tab 2")
        self.notebook.add(self.tab3.frame, text="Tab 3")
        self.notebook.add(self.tab4.frame, text="Tab 4")

        # Pack the notebook to make it visible
        self.notebook.pack(expand=True, fill='both')

        # Add a Quit button at the bottom of the main window
        quit_button = ttk.Button(self.root, text="Quit", command=self.root.quit)
        quit_button.pack(side="bottom", pady=10)


# Create the main window
root = tk.Tk()
app = MainApplication(root)
root.mainloop()
