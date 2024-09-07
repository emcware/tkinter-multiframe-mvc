import os
import tkinter as tk
from tkinter import ttk

class FileTreeView:
    def __init__(self, root):
        self.root = root
        self.tree = ttk.Treeview(self.root, selectmode='none')  # Disable extended selection
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind('<Button-1>', self.on_click)  # Bind click event for selection handling
        self.selected_files = set()

        # Scrollbars
        ysb = ttk.Scrollbar(self.root, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.root, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        ysb.pack(side='right', fill='y')
        xsb.pack(side='bottom', fill='x')

        # Initialize columns
        self.tree.heading('#0', text='Files', anchor='w')

        # Hard-coded path to top-level folder
        self.top_folder = '/Users/mikekriege/EMC/Factors'
        self.load_folder(self.top_folder)

    def load_folder(self, folder_path):
        """Load a folder into the tree view."""
        self.tree.delete(*self.tree.get_children())
        root_node = self.tree.insert('', 'end', text=folder_path, open=True)
        self.populate_tree(root_node, folder_path)

    def populate_tree(self, parent, full_path):
        """Populate tree with files and folders."""
        for item in os.listdir(full_path):
            abs_path = os.path.join(full_path, item)
            node_id = self.tree.insert(parent, 'end', text=item, open=False)
            if os.path.isdir(abs_path):
                self.tree.insert(node_id, 'end')  # Placeholder for folder
            elif abs_path in self.selected_files:
                self.tree.selection_add(node_id)  # Re-select previously selected files

    def open_node(self, event):
        """Open folder and populate its content when a node is expanded."""
        node_id = self.tree.focus()
        node_text = self.tree.item(node_id, 'text')
        parent_id = self.tree.parent(node_id)
        parent_path = self.get_full_path(parent_id)
        full_path = os.path.join(parent_path, node_text)

        if os.path.isdir(full_path):
            # Clear placeholder children
            if self.tree.get_children(node_id):
                self.tree.delete(*self.tree.get_children(node_id))
            # Populate the folder
            self.populate_tree(node_id, full_path)

    def on_click(self, event):
        """Handle click event for selecting and deselecting files."""
        item_id = self.tree.identify_row(event.y)
        if item_id:
            full_path = self.get_full_path(item_id)
            if os.path.isdir(full_path):
                # Folders can only be opened, not selected
                return

            if full_path in self.selected_files:
                self.selected_files.remove(full_path)
                self.tree.selection_remove(item_id)
            else:
                self.selected_files.add(full_path)
                self.tree.selection_add(item_id)

    def get_full_path(self, node_id):
        """Get full path of the selected node."""
        parts = []
        while node_id:
            node_text = self.tree.item(node_id, 'text')
            parts.insert(0, node_text)
            node_id = self.tree.parent(node_id)
        return os.path.join(*parts)


# Usage example:
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x400')

    tree_view = FileTreeView(root)

    root.mainloop()
