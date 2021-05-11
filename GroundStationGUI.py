from CCSDS_HK_Util import CCSDS_HK_Util
from CCSDS_Encoder import CCSDS_Encoder
from Command_Panel import Command_Panel
import CCSDS_Parameters as ccsds_param
from Beacon_Panel import BeaconPanel
from multiprocessing import Process
import App_Parameters as app_param
from Start_Page import StartPage
from Testing import IS_TESTING
import tkinter as tk
import subprocess
import serial
import sys
import os


class MainApp(tk.Frame):
    def __init__(self, parent, ports, pipe_beacon, ttnc_lock):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.minsize(650, 140)
        self.parent.title("Ground Station")

        # Serial ports
        self.ports = ports

        # Locks for serial ports
        self. serial_ttnc_lock = ttnc_lock

        # Pipe for beacon
        self.pipe_beacon = pipe_beacon

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

            # Pass ttnc serial object via pipe to thread
            self.pipe_beacon.send(self.port_ttnc)

            # Erase Start Page
            self.container.grid_forget()

            # Generate Container to store new page
            self.container = tk.Frame(
                self.parent, width=app_param.APP_WIDTH, height=app_param.APP_HEIGHT)
            self.container.pack()

            # Generate Beacon page for left
            self.beacon = BeaconPanel(self.container, self.pipe_beacon)
            self.beacon.pack(side=tk.RIGHT, anchor=tk.NW, fill="both")

            self.command = Command_Panel(self.container, self)
            self.command.pack(side=tk.LEFT)

    def hk_process(self):
        # self.p1 = Process(target=sample_process, daemon=True,
        #                   args=(self.pipe_beacon, self.serial_ttnc_lock,))  # Testing
        self.p1 = Process(target=get_HK_logs, daemon=True,
                          args=(self.pipe_beacon, self.port_ttnc, self.serial_ttnc_lock,))
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


def get_HK_logs(pipe, ttnc_serial_port, lock):

    def setup_serial(port):
        ttnc_ser = serial.Serial(port)
        ttnc_ser.baudrate = 9600
        ttnc_ser.timeout = 10
        return ttnc_ser

    Encoder = CCSDS_Encoder()
    HK_Util = CCSDS_HK_Util()

    # Default for command
    timestamp_query_start = '0-0-0-0-0-0'
    timestamp_query_end = '0-0-0-0-0-0'

    telecommand = Encoder.generate_HK_telecommand(
        ccsds_param.TELECOMMAND_TYPE_OBC_HK_REQUEST, timestamp_query_start, timestamp_query_end)

    pipe.send("close_serial")
    while pipe.poll() == "":
        pass
    print(f"process receive {pipe.recv()}")

    # lock.acquire()
    ttnc_serial = setup_serial(ttnc_serial_port)

    print(f"telecommand is {telecommand}")
    print(f"telecommand len is {len(telecommand)}")
    ttnc_serial.write(telecommand)
    hk_bytes = ttnc_serial.read(
        ccsds_param.CCSDS_OBC_TELEMETRY_LEN_BYTES)
    print(f"hk bytes {hk_bytes}")
    # lock.release()

    print("done sending command")
    ttnc_serial.close()
    pipe.send("open_serial")

    if hk_bytes:
        list_hk_obj = HK_Util.parse(hk_bytes)
        HK_Util.log(list_hk_obj)
        print("done do logs")
    else:
        print("hk logs failed")


def sample_process(pipe, lock):
    i = 0
    max_val = 1000000

    print("here")

    pipe.send("close_serial")
    while pipe.poll() == "":
        pass
    print(pipe.recv())

    lock.acquire()
    while i < max_val:
        print(i)
        i += 1
    lock.release()

    print("done")
    pipe.send("open_serial")
