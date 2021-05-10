from Command_Panel import Command_Panel
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
    def __init__(self, parent, pipe_beacon, ports):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.minsize(650, 140)
        self.parent.title("Ground Station")

        # Beacon pipes
        self.pipe_beacon = pipe_beacon

        # Serial ports
        self.ports = ports

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
                self.ttnc_serial.timeout = 0.5

            # Pass ttnc serial object via pipe to thread
            self.pipe_beacon.send(self.ttnc_serial)
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
        self.p1 = Process(target=get_HK_logs, daemon=True)
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


def get_HK_logs():
    pass

# def sample_process():
#     i = 0
#     max_val = 10000
#     while i < max_val:
#         print(i)
#         i += 1
