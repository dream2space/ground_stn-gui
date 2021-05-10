from multiprocessing import Process, Queue
from CCSDS_HK_Util import CCSDS_HK_Util
from CCSDS_Encoder import CCSDS_Encoder
from Command_Panel import Command_Panel
import CCSDS_Parameters as ccsds_param
from Beacon_Panel import BeaconPanel
import App_Parameters as app_param
from Start_Page import StartPage
from Testing import IS_TESTING
import tkinter as tk
import subprocess
import serial
import sys
import os

# CCSDS
from CCSDS_Parameters import CCSDS_BEACON_LEN_BYTES
from CCSDS_Decoder import CCSDS_Decoder


import random
import time


class MainApp(tk.Frame):
    def __init__(self, parent, ports, ttnc_lock):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.minsize(650, 140)
        self.parent.title("Ground Station")

        # Serial ports
        self.ports = ports

        # Locks for serial ports
        self. serial_ttnc_lock = ttnc_lock

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.grid()
        self.make_start_page()

    def make_start_page(self):
        self.start = StartPage(self.container, self)

    def handle_transition(self):
        # Extract ports selected
        self.port_ttnc = self.start.get_ttnc_port()
        self.port_payload = self.start.get_payload_port()

        if self.port_ttnc == self.port_payload or self.port_ttnc == " " or self.port_ttnc == " ":
            # Same ports selected
            self.start.set_port_warning_message()

        else:
            self.ttnc_serial = None
            if not IS_TESTING:
                # Setup ttnc port serial object
                self.ttnc_serial = serial.Serial(self.port_ttnc)
                self.ttnc_serial.baudrate = 9600
                # Changed the time since child processes will not block parent process
                self.ttnc_serial.timeout = 10

            # Create pipes
            pipe_ttnc = Queue()

            # Erase Start Page
            self.container.grid_forget()

            # Generate Container to store new page
            self.container = tk.Frame(
                self.parent, width=app_param.APP_WIDTH, height=app_param.APP_HEIGHT)
            self.container.pack()

            # Generate Beacon page for left
            self.beacon = BeaconPanel(self.container, pipe_ttnc)
            self.beacon.pack(side=tk.RIGHT, anchor=tk.NW, fill="both")

            self.command = Command_Panel(self.container, self)
            self.command.pack(side=tk.LEFT)

            # Pass ttnc serial object via pipe to thread
            self.data_process = Process(
                target=beacon_collection, args=(self.ttnc_serial, self.serial_ttnc_lock, pipe_ttnc,), daemon=True)
            self.data_process.start()

    def hk_process(self):
        # self.p1 = Process(target=sample_process, daemon=True,
        #                 args=(self.serial_ttnc_lock,))  # Testing
        self.p1 = Process(target=get_HK_logs, daemon=True,
                          args=(self.ttnc_serial, self.serial_ttnc_lock,))
        self.p1.start()

        # Hide button
        self.command.housekeeping_command.start_hk_button.pack_forget()

        # Display the progress bar
        self.command.housekeeping_command.pbar_container.pack()
        self.command.housekeeping_command.pbar.pack()
        self.command.housekeeping_command.pbar.start()
        self.after(100, self.checking)

    def checking(self):
        if self.p1.is_alive():
            self.after(100, self.checking)
        else:
            self.command.housekeeping_command.pbar.stop()
            self.command.housekeeping_command.pbar_container.pack_forget()
            self.command.housekeeping_command.start_hk_button.pack()

            # Open up explorer
            path = os.path.relpath(app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH)
            if sys.platform.startswith('win'):
                os.startfile(path)
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                subprocess.check_call(['xdg-open', '--', path])


def get_HK_logs(ttnc_serial, lock):
    Encoder = CCSDS_Encoder()
    HK_Util = CCSDS_HK_Util()

    # Default for command
    timestamp_query_start = '0-0-0-0-0-0'
    timestamp_query_end = '0-0-0-0-0-0'

    telecommand = Encoder.generate_HK_telecommand(
        ccsds_param.TELECOMMAND_TYPE_OBC_HK_REQUEST, timestamp_query_start, timestamp_query_end)

    lock.acquire()
    ttnc_serial.write(telecommand)
    hk_bytes = ttnc_serial.read(
        ccsds_param.CCSDS_OBC_TELEMETRY_LEN_BYTES)
    lock.release()

    if hk_bytes:
        list_hk_obj = HK_Util.parse(hk_bytes)
        HK_Util.log(list_hk_obj)
    else:
        print("hk logs failed")


def sample_process(lock):
    i = 0
    max_val = 1000000
    lock.acquire()
    while i < max_val:
        print(i)
        i += 1
    lock.release()


def beacon_collection(serial_ttnc, lock, pipe_beacon):
    # Setup CCSDS Decoder
    Decoder = CCSDS_Decoder(isBeacon=True)

    # Setup ttnc serial port
    temp = 0
    gx = 0
    gy = 0
    gz = 0
    pipe_beacon.send([temp, gx, gy, gz])

    while True:
        # Acquire lock
        lock.acquire()

        if IS_TESTING:
            temp = f"{random.randrange(20, 40)}"
            gx = f"{random.randint(-50, 50)}"
            gy = f"{random.randint(-50, 50)}"
            gz = f"{random.randint(-50, 50)}"
            print("beacon", temp, gx, gy, gz)
            time.sleep(10)
            pipe_beacon.put([temp, gx, gy, gz])
            lock.release()
            continue

        # Read beacon packets
        ccsds_beacon_bytes = serial_ttnc.read(CCSDS_BEACON_LEN_BYTES)
        # print(ccsds_beacon_bytes)
        lock.release()

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
            pipe_beacon.put([temp, gx, gy, gz])
