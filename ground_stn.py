from GroundStationGUI import GroundStationPage, MainApp
from multiprocessing import Pipe
import tkinter as tk
import threading
import random
import time

# Serial port scan
import serial
import glob
import sys


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

    # Scan for serial ports
    ports = scan_serial_ports()

    # Create pipe for between Tk GUI and data thread
    pipe_gui, pipe_beacon = Pipe()

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    MainApp(root, pipe_gui, ports)

    # Thread to read data
    data_thread = threading.Thread(
        group=None, target=data_creation, args=(pipe_beacon, ))
    data_thread.setDaemon(True)
    data_thread.start()

    # Start Tk GUI in main thread
    root.mainloop()
