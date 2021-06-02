import datetime
import glob
import os
import subprocess
import sys
import tkinter as tk
from multiprocessing import Process
from tkinter import messagebox

import serial

import App_Parameters as app_param
from App_Util import (process_get_HK_logs, resource_path,
                      sample_hk_command_process)
from Beacon_Panel import BeaconPanel
from Housekeeping_DataFrame import HousekeepingDataFrame
from Mission_Downlink_DataFrame import MissionDownlinkFrame
from Mission_Util import (process_handle_downlink,
                          process_send_mission_telecommand,
                          sample_downlink_process,
                          sample_mission_command_process)
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

        # List of pending missions
        self.pending_mission_list = []

        # List of executing missions
        self.current_mission_list = []

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.grid()
        self.make_start_page()

        # Poll and check for missions to execute
        self.mission_execution_check()

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
            self.housekeeping_process = Process(target=sample_hk_command_process, daemon=True)  # Testing
        else:
            self.is_hk_process_success = False
            self.prev_file_number = len(os.listdir(
                app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH))
            self.housekeeping_process = Process(target=process_get_HK_logs, daemon=True,
                                                args=(self.pipe_beacon, self.port_ttnc, ))
        self.housekeeping_process.start()
        self.housekeeping_command.show_progress_bar()

        # Disable mission function
        self.mission_command.disable_mission_command()

    # Checks regularly if housekeeping process is complete
    def hk_process_checking(self):
        # If process still alive, continute to check
        if self.housekeeping_process.is_alive():
            self.after(100, self.hk_process_checking)

        # If process ended, inform user
        else:
            self.housekeeping_command.stop_showing_progress_bar()

            # Re-enable mission command
            self.mission_command.stop_mission_block()

            if not IS_TESTING:
                # Determine if telecommand obtaining is successful
                curr_number_files = len(os.listdir(
                    app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH))
                if curr_number_files > self.prev_file_number:
                    self.is_hk_process_success = True
                    self.prev_file_number = curr_number_files
            else:
                self.is_hk_process_success = True

            # Housekeeping data parsing sucess - Open up explorer
            if self.is_hk_process_success == True:
                path = os.path.relpath(
                    app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH)
                if sys.platform.startswith('win'):
                    os.startfile(path)
                elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                    subprocess.check_call(['xdg-open', '--', path])

                # display success message
                self.housekeeping_command.display_success_message()

            # Housekeeping data parsing failed
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
        def validate_mission(mission_input):
            # print(mission_input)
            is_mission_time_future = mission_input.mission_datetime > datetime.datetime.now()
            is_downlink_after_mission = mission_input.downlink_datetime > mission_input.mission_datetime
            num_mission = len(self.pending_mission_list)
            if is_mission_time_future and is_downlink_after_mission and num_mission < 3:
                return True
            else:
                return False

        # Do input validation
        mission = self.mission_window.get_user_mission_input()
        is_valid_input = validate_mission(mission)

        if is_valid_input:
            # Close top window
            self.mission_window.handle_mission_success()

            # Display success and show mission loading screen
            self.mission_command.display_add_success_msg()
            self.mission_command.show_progress_bar()
            self.mission_command.after(10000, self.mission_command.stop_mission_block)

            # Disable housekeeping data function
            self.housekeeping_command.disable_housekeeping_command()
            self.housekeeping_command.after(10000, self.housekeeping_command.stop_showing_progress_bar)

            # Add into pending mission list
            self.pending_mission_list.append(mission)
            self.pending_mission_list.sort(key=lambda x: x.downlink_datetime)  # Sort on earliest downlink datetime
            print(self.pending_mission_list)

            # Display the pending mission into mission table
            self.mission_command.pending_mission_table.update_mission_entry(self.pending_mission_list)

            # Send CCSDS mission command to Cubesat
            if IS_TESTING:
                self.mission_command_process = Process(target=sample_mission_command_process, daemon=True)  # Testing
            else:
                self.mission_command_process = Process(target=process_send_mission_telecommand, daemon=True, args=(
                    mission, self.pipe_beacon, self.port_ttnc, ))  # Testing
            self.mission_command_process.start()

        else:
            # Input time is not valid
            num_current_missions = len(self.pending_mission_list)
            self.mission_window.display_error_message(num_current_missions)

    def mission_execution_check(self):
        print(f"CHECK! {datetime.datetime.now()}")

        num_mission = len(self.pending_mission_list)
        print(self.pending_mission_list)
        if num_mission != 0:
            # Check top most mission item
            # Start collection process if within 2 minutes of downlink
            earliest_mission = self.pending_mission_list[0]
            upcoming_downlink_datetime = earliest_mission.downlink_datetime

            if upcoming_downlink_datetime - datetime.datetime.now() < datetime.timedelta(seconds=120):
                print("less than 2 minutes to mission!!")
                self.current_mission_list.append(earliest_mission)
                del self.pending_mission_list[0]

                if IS_TESTING:
                    self.downlink_process = Process(target=sample_downlink_process, daemon=True)  # Testing
                else:
                    self.downlink_process = Process(target=process_handle_downlink, daemon=True, args=(
                        self.port_payload, earliest_mission.get_mission_name(),))

                self.downlink_process.start()

                # Render on the missions screens
                self.mission_command.pending_mission_table.update_mission_entry(self.pending_mission_list)
                self.mission_command.current_mission_table.update_mission_entry(self.current_mission_list)

        try:
            if len(self.current_mission_list) != 0 and not self.downlink_process.is_alive():
                del self.current_mission_list[0]
                self.mission_command.current_mission_table.update_mission_entry(self.current_mission_list)
        except AttributeError:
            pass

        self.after(app_param.APP_DOWNLINK_PROCESS_CHECK_INTERVAL, self.mission_execution_check)

    # Respond to button pressed when User wishes to view completed Missions/Downlink
    def view_completed_missions(self):

        # If no mission created yet, not records found
        # Show popup warning
        if not os.path.exists(f"{app_param.GROUND_STN_MISSION_LOG_FILEPATH}"):
            messagebox.showerror(title="Dream2space Ground Station",
                                 message="Mission records not found!\nTry to send a mission command.")
