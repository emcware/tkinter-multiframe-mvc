# tab1_controller.py
from pubsub import pub
from models import Tab1Model
from tab1_view import Tab_1_View
import threading


class Tab_1_Controller:
    def __init__(self, parent):
        self.model = Tab1Model()
        self.view = Tab_1_View(parent)

        # Bind view buttons to controller methods
        self.view.table_button.config(command=self.start_rotate_table)
        self.view.tower_button.config(command=self.start_move_tower)
        self.view.instrument_button.config(command=self.start_read_instrument)
        self.view.abort_button.config(command=self.abort_process)

        # Subscribe to updates
        pub.subscribe(self.update_rotate_table, "rotate_table_update")
        pub.subscribe(self.update_move_tower, "move_tower_update")
        pub.subscribe(self.update_read_instrument, "read_instrument_update")

        # Subscribe to completions
        pub.subscribe(self.on_rotate_table_completed, "rotate_table_completed")
        pub.subscribe(self.on_move_tower_completed, "move_tower_completed")
        pub.subscribe(self.on_read_instrument_completed, "read_instrument_completed")

    def start_rotate_table(self):
        self.view.disable_buttons()
        self.model.abort_flag.clear()  # Reset the abort flag
        threading.Thread(target=self.model.rotate_table_task).start()

    def start_move_tower(self):
        self.view.disable_buttons()
        self.model.abort_flag.clear()  # Reset the abort flag
        threading.Thread(target=self.model.move_tower_task).start()

    def start_read_instrument(self):
        self.view.disable_buttons()
        self.model.abort_flag.clear()  # Reset the abort flag
        threading.Thread(target=self.model.read_instrument_task).start()

    def abort_process(self):
        self.model.abort_process()
        self.view.enable_buttons()

    def update_rotate_table(self, angle):
        if not self.model.abort_flag.is_set():
            self.view.table_label.config(text=f"Table Rotation: {angle}°")

    def update_move_tower(self, height):
        if not self.model.abort_flag.is_set():
            self.view.tower_label.config(text=f"Tower Height: {height} cm")

    def update_read_instrument(self, point):
        if not self.model.abort_flag.is_set():
            self.view.instrument_label.config(text=f"Instrument Reading: {point} points")

    def on_rotate_table_completed(self, status):
        if not self.model.abort_flag.is_set():
            self.view.table_label.config(text=status)
        self.view.enable_buttons()

    def on_move_tower_completed(self, status):
        if not self.model.abort_flag.is_set():
            self.view.tower_label.config(text=status)
        self.view.enable_buttons()

    def on_read_instrument_completed(self, status):
        if not self.model.abort_flag.is_set():
            self.view.instrument_label.config(text=status)
        self.view.enable_buttons()

