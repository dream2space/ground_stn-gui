from GroundStationGUI import GroundStationPage
from multiprocessing import Pipe
import tkinter as tk
import threading
import random
import time


def data_creation(pipe_beacon):
    while True:
        # Feed data into pipes
        temp = f"{random.randrange(20, 40)}"
        gx = f"{random.randint(-50, 50)}"
        gy = f"{random.randint(-50, 50)}"
        gz = f"{random.randint(-50, 50)}"

        pipe_beacon.send([temp, gx, gy, gz])
        time.sleep(1)


# Start running GUI
if __name__ == "__main__":

    # Create pipe for between Tk GUI and data thread
    pipe_gui, pipe_beacon = Pipe()

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    GroundStationPage(root, pipe_gui)

    # Thread to read data
    data_thread = threading.Thread(
        group=None, target=data_creation, args=(pipe_beacon, ))
    data_thread.setDaemon(True)
    data_thread.start()

    # Start Tk GUI in main thread
    root.mainloop()
