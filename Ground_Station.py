import multiprocessing
import os
import threading
import tkinter as tk

import App_Parameters as app_params
import Mission_Parameters as mission_params
from App_Util import beacon_collection
from GroundStationGUI import MainApp

# Start running GUI
if __name__ == "__main__":

    # To fix the multiple tkinter window spawning problem
    multiprocessing.freeze_support()

    # Check folder path to save CSV file
    if not os.path.exists(app_params.HOUSEKEEPING_DATA_FOLDER_FILEPATH):
        os.makedirs(app_params.HOUSEKEEPING_DATA_FOLDER_FILEPATH)

    # Check folder path to save mission
    if not os.path.exists(mission_params.GROUND_STN_MISSION_FOLDER_PATH):
        os.makedirs(mission_params.GROUND_STN_MISSION_FOLDER_PATH)

    # Create pipes for beacon
    pipe_beacon, pipe_gui = multiprocessing.Pipe(True)

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    MainApp(root, pipe_gui)

    # Thread to read data
    beacon_thread = threading.Thread(
        target=beacon_collection, daemon=True, args=(pipe_beacon,))
    beacon_thread.start()

    # Start Tk GUI in main thread
    root.mainloop()
