import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FolderTreeView(ttk.Frame):
    def __init__(self, parent, root_path=None, selection_storage=None, *args, **kwargs):
        """
        Initialize the FolderTreeView.

        :param parent: Parent tkinter widget.
        :param root_path: The root directory to display. If None, prompts the user to select.
        :param selection_storage: A dictionary or similar to store selected paths.
        """
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.root_path = root_path
        self.selection_storage = selection_storage if selection_storage is not None else {}
        self.selected_items = set()

        # Setup Treeview
        self.tree = ttk.Treeview(self, selectmode='extended')
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Setup Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Define columns
        self.tree["columns"] = ("fullpath", "type")
        self.tree.column("#0", width=300, anchor='w')  # Folder/File name
        self.tree.column("fullpath", width=0, stretch=False)  # Hidden
        self.tree.column("type", width=0, stretch=False)  # Hidden

        self.tree.heading("#0", text="Name", anchor='w')

        # Bind events
        self.tree.bind('<<TreeviewOpen>>', self.on_open)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Initialize root
        if not self.root_path:
            self.choose_root_directory()
        else:
            self.populate_tree()

    def choose_root_directory(self):
        """Prompt the user to select a root directory."""
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.root_path = selected_dir
            self.populate_tree()
        else:
            messagebox.showerror("No Directory Selected", "No root directory was selected.")

    def populate_tree(self):
        """Populate the tree view with the directory structure."""
        # Clear existing tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert root node
        root_node = self.tree.insert('', 'end', text=self.root_path, values=(self.root_path, "directory"), open=True)
        self.populate_node(root_node, self.root_path)

        # Restore previous selection
        self.restore_selection()

    def populate_node(self, parent, path):
        """Recursively populate the tree node with folders and files."""
        try:
            for p in os.listdir(path):
                fullpath = os.path.join(path, p)
                if os.path.isdir(fullpath):
                    node = self.tree.insert(parent, 'end', text=p, values=(fullpath, "directory"))
                    # Insert a dummy child to make the node expandable
                    self.tree.insert(node, 'end')
                else:
                    self.tree.insert(parent, 'end', text=p, values=(fullpath, "file"))
        except PermissionError:
            pass  # Skip folders that cannot be accessed

    def on_open(self, event):
        """Handle the event when a node is expanded."""
        node = self.tree.focus()
        if self.tree.get_children(node):
            first_child = self.tree.get_children(node)[0]
            # Check if it's a dummy node
            if self.tree.item(first_child, "values")[1] == "":
                self.tree.delete(first_child)
                path = self.tree.set(node, "fullpath")
                self.populate_node(node, path)

    def on_select(self, event):
        """Handle selection events and store selected paths."""
        selected = self.tree.selection()
        self.selected_items.clear()
        for item in selected:
            path = self.tree.set(item, "fullpath")
            self.selected_items.add(path)
            # Update the storage
            self.selection_storage[path] = True

    def restore_selection(self):
        """Restore previously selected items."""
        for node in self.tree.get_children():
            self.restore_node_selection(node)

    def restore_node_selection(self, node):
        """Recursively restore selection for a node and its children."""
        path = self.tree.set(node, "fullpath")
        if path in self.selection_storage:
            self.tree.selection_add(node)

        # If directory and not yet populated, populate it
        item_type = self.tree.set(node, "type")
        if item_type == "directory":
            # Populate children if not already
            if not self.tree.get_children(node):
                self.populate_node(node, path)
            for child in self.tree.get_children(node):
                self.restore_node_selection(child)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Folder Tree View Example")
        self.geometry("600x400")

        # Storage for selections
        self.selection_storage = {}

        # Button to open folder tree
        self.open_button = ttk.Button(self, text="Open Folder Tree", command=self.open_folder_tree)
        self.open_button.pack(pady=10)

        # Label to show selected items
        self.selected_label = ttk.Label(self, text="Selected Items: None", wraplength=500, justify=tk.LEFT)
        self.selected_label.pack(pady=10)

        # Reference to the tree view window
        self.tree_window = None

    def open_folder_tree(self):
        """Open the folder tree in a new window."""
        if self.tree_window and tk.Toplevel.winfo_exists(self.tree_window):
            self.tree_window.focus()
            return

        self.tree_window = tk.Toplevel(self)
        self.tree_window.title("Folder Tree View")
        self.tree_window.geometry("500x400")

        # Initialize FolderTreeView
        folder_tree = FolderTreeView(self.tree_window, selection_storage=self.selection_storage)
        folder_tree.pack(fill=tk.BOTH, expand=True)

        # Button to confirm selection
        confirm_button = ttk.Button(self.tree_window, text="Confirm Selection",
                                    command=lambda: self.confirm_selection(folder_tree))
        confirm_button.pack(pady=5)

    def confirm_selection(self, folder_tree):
        """Handle the confirmation of selected items."""
        selected = folder_tree.selected_items
        if selected:
            self.selected_label.config(text="Selected Items:\n" + "\n".join(selected))
        else:
            self.selected_label.config(text="Selected Items: None")
        self.tree_window.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
