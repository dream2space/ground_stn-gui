from GroundStationGUI import MainApp
import App_Parameters as app_params
import multiprocessing
import tkinter as tk
import threading
import os

# Serial port scan
import serial
import glob
import sys


# Testing flag
from Testing import IS_TESTING
from CCSDS_Decoder import CCSDS_Decoder
import CCSDS_Parameters as ccsds_params
import random
import time


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


def beacon_collection(lock, pipe_beacon):

    def setup_serial(port):
        ttnc_ser = serial.Serial(port)
        ttnc_ser.baudrate = 9600
        ttnc_ser.timeout = 0.8
        return ttnc_ser

    # Setup CCSDS Decoder
    Decoder = CCSDS_Decoder(isBeacon=True)

    while pipe_beacon.poll() == b"":
        pass

    # Obtain ttnc serial port object
    ttnc_serial_port = pipe_beacon.recv()

    # Setup ttnc port serial object
    if not IS_TESTING:
        ttnc_ser = setup_serial(ttnc_serial_port)
        print("first setup serial done")

    # Setup ttnc serial port
    temp = 0
    gx = 0
    gy = 0
    gz = 0
    pipe_beacon.send([temp, gx, gy, gz])

    isStopBeacon = False
    while True:

        # Acquire lock and begin beacon receiving

        if IS_TESTING:
            # lock.acquire()
            temp = f"{random.randrange(20, 40)}"
            gx = f"{random.randint(-50, 50)}"
            gy = f"{random.randint(-50, 50)}"
            gz = f"{random.randint(-50, 50)}"
            print("beacon", temp, gx, gy, gz)
            time.sleep(10)
            pipe_beacon.send([temp, gx, gy, gz])
            # lock.release()
            continue

        # If receive signal to close serial port
        if pipe_beacon.poll() == True:
            recv = pipe_beacon.recv()
            print(f"beacon process {recv}")

            if recv == "close_serial":
                ttnc_ser.close()
                pipe_beacon.send("done")
                isStopBeacon = True
                print("close serial")

            if recv == "open_serial":
                ttnc_ser = setup_serial(ttnc_serial_port)
                isStopBeacon = False

        if not isStopBeacon:
            # Read beacon packets
            print("reading beaconds")
            ccsds_beacon_bytes = ttnc_ser.read(
                ccsds_params.CCSDS_BEACON_LEN_BYTES)
            print(ccsds_beacon_bytes)
            # lock.release()

            if ccsds_beacon_bytes:
                try:
                    decoded_ccsds_beacon = Decoder.parse_beacon(
                        ccsds_beacon_bytes)
                except IndexError:
                    continue

                temp = f"{decoded_ccsds_beacon.get_temp():.2f}"
                gyro = decoded_ccsds_beacon.get_gyro()
                gx = f"{gyro['gx']}"
                gy = f"{gyro['gy']}"
                gz = f"{gyro['gz']}"

                # print("beacon", temp, gx, gy, gz)
                pipe_beacon.send([temp, gx, gy, gz])


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

    # Create pipes for beacon
    pipe_beacon, pipe_gui = multiprocessing.Pipe(True)

    # Initialize Tk GUI in main thread
    root = tk.Tk()
    MainApp(root, ports, pipe_gui, serial_ttnc_lock)

    # Thread to read data
    beacon_thread = threading.Thread(
        target=beacon_collection, daemon=True, args=(serial_ttnc_lock, pipe_beacon,))
    beacon_thread.start()

    # Start Tk GUI in main thread
    root.mainloop()
