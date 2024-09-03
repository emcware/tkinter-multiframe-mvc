# models.py
import threading
import time
from pubsub import pub


class Tab1Model:
    def __init__(self):
        self.abort_flag = threading.Event()

    def rotate_table_task(self):
        for angle in range(0, 361):  # Rotate from 0 to 360 degrees
            if self.abort_flag.is_set():
                pub.sendMessage("rotate_table_completed", status="Rotation Aborted")
                return
            time.sleep(0.01)  # Simulate time taken for the task
            pub.sendMessage("rotate_table_update", angle=angle)
        pub.sendMessage("rotate_table_completed", status="Rotation Complete")

    def move_tower_task(self):
        for height in range(100, 401):  # Move from 100 cm to 400 cm
            if self.abort_flag.is_set():
                pub.sendMessage("move_tower_completed", status="Movement Aborted")
                return
            time.sleep(0.02)  # Simulate time taken for the task
            pub.sendMessage("move_tower_update", height=height)
        pub.sendMessage("move_tower_completed", status="Movement Complete")

    def read_instrument_task(self):
        for point in range(1, 1002):  # Read 1001 points
            if self.abort_flag.is_set():
                pub.sendMessage("read_instrument_completed", status="Reading Aborted")
                return
            time.sleep(0.005)  # Simulate time taken for the task
            pub.sendMessage("read_instrument_update", point=point)
        pub.sendMessage("read_instrument_completed", status="Reading Complete")

    def abort_process(self):
        self.abort_flag.set()  # Signal the threads to stop
