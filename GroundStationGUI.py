import datetime
import glob
import os
import subprocess
import sys
import tkinter as tk
from multiprocessing import Process

import serial

import App_Parameters as app_param
from App_Util import get_HK_logs, resource_path, sample_process
from Beacon_Panel import BeaconPanel
from Housekeeping_DataFrame import HousekeepingDataFrame
from Mission_Downlink_DataFrame import MissionDownlinkFrame
from Mission_Window import MissionWindow
from Start_Page import StartPage
from Testing import IS_TESTING


class MainApp(tk.Frame):
    def __init__(self, parent, pipe_beacon):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)
        self.parent.iconbitmap(resource_path("assets/satellite.ico"))
        self.parent.title("Dream2space Ground Station")

        # Scan for serial ports
        ports = self.scan_serial_ports()
        self.ports = ports

        # Pipe for beacon
        self.pipe_beacon = pipe_beacon

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.grid()
        self.make_start_page()

    # Initializing method to create Start Page
    def make_start_page(self):
        self.start = StartPage(self.container, self)

    # Scan Serial ports in PC
    def scan_serial_ports(self):
        ports = []
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                continue

        result.insert(0, " ")

        # In testing, add dummy entries
        if IS_TESTING:
            result.append("COM14")
            result.append("COM15")

        return result

    # Handle transition from Start Page to Main Page
    # Upon pressing button to select Serial ports
    def handle_transition(self):
        # Extract ports selected
        self.port_ttnc = self.start.get_ttnc_port()
        self.port_payload = self.start.get_payload_port()

        # Ports selected are wrong -> Prompt users to reselect
        if self.port_ttnc == self.port_payload or self.port_ttnc == " " or self.port_ttnc == " ":
            # Same ports selected
            self.start.set_port_warning_message()

        # Ports selected are correct -> Proceed to generate main page
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

            # Create container to store all subsections
            self.command_panel_container = tk.Frame(self.container)
            self.command_panel_container.pack(side=tk.LEFT, expand=1, fill="both", padx=10, pady=10)

            # Create section to request for housekeeping data
            self.housekeeping_command = HousekeepingDataFrame(
                self.command_panel_container, self, tk.TOP, text="Housekeeping Command", padx=10, pady=8)

            # Create section for mission and downlink
            self.mission_command = MissionDownlinkFrame(
                self.command_panel_container, self, tk.BOTTOM, text="Mission and Downlink Command", padx=10, pady=8)

    # Handles Housekeeping Process after button pressed
    def handle_hk_process_start(self):
        if IS_TESTING:
            self.p1 = Process(target=sample_process, daemon=True)  # Testing
        else:
            self.is_hk_process_success = False
            self.prev_file_number = len(os.listdir(
                app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH))
            self.p1 = Process(target=get_HK_logs, daemon=True,
                              args=(self.pipe_beacon, self.port_ttnc, ))
        self.p1.start()

        # Hide button
        self.housekeeping_command.start_hk_button.pack_forget()

        # Display the progress bar
        self.housekeeping_command.pbar_container.pack()
        self.housekeeping_command.pbar.pack()
        self.housekeeping_command.pbar.start()
        self.after(100, self.hk_process_checking)

    # Checks regularly if housekeeping process is complete
    def hk_process_checking(self):

        if self.p1.is_alive():
            self.after(100, self.hk_process_checking)
        else:
            self.housekeeping_command.pbar.stop()
            self.housekeeping_command.pbar_container.pack_forget()
            self.housekeeping_command.start_hk_button.pack()

            if not IS_TESTING:
                # Determine if telecommand obtaining is successful
                curr_number_files = len(os.listdir(
                    app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH))
                if curr_number_files > self.prev_file_number:
                    self.is_hk_process_success = True
                    self.prev_file_number = curr_number_files
            else:
                self.is_hk_process_success = True

            # Open up explorer
            if self.is_hk_process_success == True:
                path = os.path.relpath(
                    app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH)
                if sys.platform.startswith('win'):
                    os.startfile(path)
                elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                    subprocess.check_call(['xdg-open', '--', path])

                # display success message
                self.housekeeping_command.display_success_message()
            else:
                # display fail message
                self.housekeeping_command.display_failed_message()

            # Undo flag
            self.is_hk_process_success = False

    # Open mission window
    def open_mission_downlink_command_window(self):
        self.mission_window = MissionWindow(self.parent, self)

    # Handle mission checking and scheduling after submited on mission window
    def handle_mission_scheduling(self):
        # Validate if (1) mission time is after current time, (2) downlink time after mission time
        def validate_mission_input(mission_input):
            print(mission_input)
            is_mission_time_future = mission_input.mission_datetime > datetime.datetime.now()
            is_downlink_after_mission = mission_input.downlink_datetime > mission_input.mission_datetime
            if is_mission_time_future and is_downlink_after_mission:
                return True
            else:
                return False

        # Do input validation
        mission_input = self.mission_window.get_user_mission_input()
        is_valid_input = validate_mission_input(mission_input)

        if is_valid_input:
            # Close top window
            self.mission_window.destroy()
            self.mission_command.display_add_success_msg()

            # Disable and show mission loading screen

            # Send CCSDS mission command to Cubesat

            # Add into pending mission list

            # Display the pending mission into mission table

        else:
            # Input time is not valid
            self.mission_window.display_error_message()
