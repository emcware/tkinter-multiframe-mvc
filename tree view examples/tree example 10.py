import tkinter as tk
from tkinter import ttk
from pathlib import Path


class FileTreeView:
    def __init__(self, parent, folder_path, heading='Files'):
        self.frame = ttk.Frame(parent)
        self.frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.base_folder = Path(folder_path)  # Store the base folder path

        # Treeview for displaying files with custom heading
        self.tree = ttk.Treeview(self.frame, selectmode='none')  # Disable extended selection
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind('<Button-1>', self.on_click)  # Bind click event for selection handling
        self.selected_files = set()

        # Scrollbars
        ysb = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        ysb.pack(side='right', fill='y')
        xsb.pack(side='bottom', fill='x')

        # Initialize columns with custom heading
        self.tree.heading('#0', text=heading, anchor='w')

        # Load the folder
        self.load_folder(self.base_folder)

    def load_folder(self, folder_path: Path):
        """Load the contents of the folder directly into the tree view, without showing the top-level folder."""
        self.tree.delete(*self.tree.get_children())
        self.populate_tree('', folder_path)

    def populate_tree(self, parent, folder_path: Path):
        """Populate tree with files and folders, hiding hidden files and sorting alphabetically."""
        items = sorted(folder_path.iterdir(), key=lambda p: p.name.lower())  # Sort alphabetically
        for item in items:
            if item.name.startswith('.'):
                continue  # Skip hidden files
            node_id = self.tree.insert(parent, 'end', text=item.name, open=False)
            if item.is_dir():
                self.tree.insert(node_id, 'end')  # Placeholder for folder
            elif str(item) in self.selected_files:
                self.tree.selection_add(node_id)  # Re-select previously selected files

    def open_node(self, event):
        """Open folder and populate its content when a node is expanded."""
        node_id = self.tree.focus()
        node_text = self.tree.item(node_id, 'text')
        parent_id = self.tree.parent(node_id)

        # Get the full path based on the current node and base folder
        parent_path = self.get_full_path(parent_id)
        full_path = Path(parent_path) / node_text

        if full_path.is_dir():
            # Clear placeholder children
            if self.tree.get_children(node_id):
                self.tree.delete(*self.tree.get_children(node_id))
            # Populate the folder
            self.populate_tree(node_id, full_path)

    def on_click(self, event):
        """Handle click event for selecting and deselecting files."""
        item_id = self.tree.identify_row(event.y)
        if item_id:
            full_path = Path(self.get_full_path(item_id))
            if full_path.is_dir():
                # Folders can only be opened, not selected
                return

            if str(full_path) in self.selected_files:
                self.selected_files.remove(str(full_path))
                self.tree.selection_remove(item_id)
            else:
                self.selected_files.add(str(full_path))
                self.tree.selection_add(item_id)

    def get_full_path(self, node_id):
        """Get full path of the selected node relative to the base folder."""
        parts = []
        while node_id:
            node_text = self.tree.item(node_id, 'text')
            parts.insert(0, node_text)
            node_id = self.tree.parent(node_id)
        return self.base_folder.joinpath(*parts)


# Main Application Window
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("File Browser Application")
        self.geometry('800x600')

        # Left panel with Listbox and Quit button
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.listbox = tk.Listbox(left_frame)
        self.listbox.pack(side=tk.TOP, fill=tk.Y, expand=True)

        # Add ranges to the listbox
        for i in range(1, 41):
            self.listbox.insert(tk.END, f'Range {i}')

        # Quit button
        quit_button = ttk.Button(left_frame, text='Quit', command=self.quit)
        quit_button.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Right panel with FileTreeView frames
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # File view 1 (Link Files with custom heading)
        self.link_files_view = FileTreeView(right_frame, '/Users/mikekriege/EMC/Factors', heading='Link Files')

        # File view 2 (Limits with custom heading)
        self.limits_view = FileTreeView(right_frame, '/Users/mikekriege/EMC/Limits', heading='Limits')


# Run the application
if __name__ == '__main__':
    app = Application()
    app.mainloop()
