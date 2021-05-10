from GroundStationGUI import MainApp
import App_Parameters as app_params
import multiprocessing
import tkinter as tk
import os

# Serial port scan
import serial
import glob
import sys


# Testing flag
from Testing import IS_TESTING


def scan_serial_ports():
    ports = []
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    # else:
    #     raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# Start running GUI
if __name__ == "__main__":

    # To fix the multiple tkinter window spawning problem
    multiprocessing.freeze_support()

    # Check folder path to save CSV file
    if not os.path.exists(app_params.HOUSEKEEPING_DATA_FOLDER_FILEPATH):
        os.makedirs(app_params.HOUSEKEEPING_DATA_FOLDER_FILEPATH)

    # Scan for serial ports
    ports = scan_serial_ports()
    ports.insert(0, " ")

    # In testing, add dummy entries
    if IS_TESTING:
        ports.append("COM14")
        ports.append("COM15")

    # Create locks for serial port
    serial_ttnc_lock = multiprocessing.Lock()

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    MainApp(root, ports, serial_ttnc_lock)

    # Thread to read data

    # Start Tk GUI in main thread
    root.mainloop()
