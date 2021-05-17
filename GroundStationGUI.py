from CCSDS_HK_Util import CCSDS_HK_Util
from CCSDS_Encoder import CCSDS_Encoder
from Command_Panel import CommandPanel
import CCSDS_Parameters as ccsds_param
from Beacon_Panel import BeaconPanel
from multiprocessing import Process
import App_Parameters as app_param
from Start_Page import StartPage
from Testing import IS_TESTING
import tkinter as tk
import tkcalendar
import subprocess
import serial
import sys
import os


class MainApp(tk.Frame):
    def __init__(self, parent, ports, pipe_beacon):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)
        self.parent.title("Ground Station")

        # Serial ports
        self.ports = ports

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

            self.command = CommandPanel(self.container, self)
            self.command.pack(side=tk.LEFT)

    def hk_process(self):
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
        self.command.housekeeping_command.start_hk_button.pack_forget()

        # Display the progress bar
        self.command.housekeeping_command.pbar_container.pack()
        self.command.housekeeping_command.pbar.pack()
        self.command.housekeeping_command.pbar.start()
        self.after(100, self.hk_process_checking)

    def hk_process_checking(self):
        if self.p1.is_alive():
            self.after(100, self.hk_process_checking)
        else:
            self.command.housekeeping_command.pbar.stop()
            self.command.housekeeping_command.pbar_container.pack_forget()
            self.command.housekeeping_command.start_hk_button.pack()

            # Determine if telecommand obtaining is successful
            curr_number_files = len(os.listdir(
                app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH))
            if curr_number_files > self.prev_file_number:
                self.is_hk_process_success = True
                self.prev_file_number = curr_number_files

            # Open up explorer
            if self.is_hk_process_success == True:
                path = os.path.relpath(
                    app_param.HOUSEKEEPING_DATA_FOLDER_FILEPATH)
                if sys.platform.startswith('win'):
                    os.startfile(path)
                elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                    subprocess.check_call(['xdg-open', '--', path])

                # display success message
                self.command.housekeeping_command.outcome_message.set(
                    "Success!")
                self.command.housekeeping_command.outcome_message_label["fg"] = 'green'
            else:
                # display fail message
                self.command.housekeeping_command.outcome_message.set(
                    "Failed!")
                self.command.housekeeping_command.outcome_message_label["fg"] = 'red'

            # Display message
            self.command.housekeeping_command.outcome_message_label.pack(
                side=tk.BOTTOM)

            # Set task to clear the message
            self.after(10000, self.hk_outcome_message_clear)

            # Undo flag
            self.is_hk_process_success = False

    def hk_outcome_message_clear(self):
        self.command.housekeeping_command.outcome_message.set("  ")

    def open_mission_downlink_command_window(self):
        self.mission_window = tk.Toplevel(self.parent)
        self.mission_window.title("Mission and Downlink Command")

        # Container for mission and downlink widgets
        self.container = tk.Frame(self.mission_window)
        self.container.pack(anchor=tk.NW, padx=30, pady=10)

        # Mission start date labelframe
        self.mission_start_date_frame = tk.LabelFrame(
            self.container, text="Mission Start Date")
        self.mission_start_date_frame.pack(expand=1, fill="both")

        # Mission start date label
        self.mission_start_date_label = tk.Label(
            self.mission_start_date_frame, text="Select Mission Start date:")
        self.mission_start_date_label.pack(side=tk.TOP)

        # Mission start calendar
        self.mission_calendar_container = tk.Frame(
            self.mission_start_date_frame)
        self.mission_calendar_container.pack(padx=5, pady=5)
        self.mission_start_calendar = tkcalendar.Calendar(
            self.mission_calendar_container)
        self.mission_start_calendar.pack(side=tk.BOTTOM)

        # Mission start time labelframe
        self.mission_start_time_frame = tk.LabelFrame(
            self.container, text="Mission Start Time")
        self.mission_start_time_frame.pack(expand=1, fill="both")

        # Mission start time label
        self.mission_start_time_container = tk.Frame(
            self.mission_start_time_frame)
        self.mission_start_time_container.pack(padx=5, pady=5)
        self.mission_start_time_label = tk.Label(
            self.mission_start_time_container, text="Select Mission Start time:")
        self.mission_start_time_label.pack()

        # Mission start time selector
        self.mission_start_time_picker = tk.Label(
            self.mission_start_time_container, text="--- Placeholder ---")
        self.mission_start_time_picker.pack()

        # Mission number of images
        self.mission_number_images_frame = tk.LabelFrame(
            self.container, text="Mission Image Count")
        self.mission_number_images_frame.pack(expand=1, fill="both")

        self.image_number_selection_label = tk.Label(self.mission_number_images_frame,
                                                     text="Select number of images:")
        self.image_number_selection_label.pack()

        # Mission number of image selector
        self.image_number_selection = tk.Label(
            self.mission_number_images_frame, text="--- Placeholder ---")
        self.image_number_selection.pack()

        # Mission time interval frame
        self.mission_interval_frame = tk.LabelFrame(
            self.container, text="Mission Image Interval")
        self.mission_interval_frame.pack(expand=1, fill="both")

        self.interval_selection_label = tk.Label(self.mission_interval_frame,
                                                 text="Select interval between images:")
        self.interval_selection_label.pack()

        # Mission number of image selector
        self.interval_selection = tk.Label(
            self.mission_interval_frame, text="--- Placeholder ---")
        self.interval_selection.pack()

        # Downlink start date labelframe
        self.downlink_start_date_frame = tk.LabelFrame(
            self.container, text="Downlink Start Date")
        self.downlink_start_date_frame.pack(expand=1, fill="both")

        # Downlink start date label
        self.downlink_start_date_label = tk.Label(
            self.downlink_start_date_frame, text="Select Downlink Start date:")
        self.downlink_start_date_label.pack(side=tk.TOP)

        # Downlink start calendar
        self.downlink_calendar_container = tk.Frame(
            self.downlink_start_date_frame)
        self.downlink_calendar_container.pack(padx=5, pady=5)
        self.downlink_start_calendar = tkcalendar.Calendar(
            self.downlink_calendar_container)
        self.downlink_start_calendar.pack(side=tk.BOTTOM)

        # Downlink start time labelframe
        self.downlink_start_time_frame = tk.LabelFrame(
            self.container, text="Downlink Start Time")
        self.downlink_start_time_frame.pack(expand=1, fill="both")

        # Downlink start time label
        self.downlink_start_time_container = tk.Frame(
            self.downlink_start_time_frame)
        self.downlink_start_time_container.pack(padx=5, pady=5)
        self.downlink_start_time_label = tk.Label(
            self.downlink_start_time_container, text="Select Downlink Start time:")
        self.downlink_start_time_label.pack()

        # Downlink start time selector
        self.downlink_start_time_picker = tk.Label(
            self.downlink_start_time_container, text="--- Placeholder ---")
        self.downlink_start_time_picker.pack()

        # Submit button container
        self.button_container = tk.Frame(self.container)
        self.button_container.pack()

        self.submit_button_label = tk.Label(self.button_container)
        self.submit_button_label.pack(side=tk.TOP)

        self.submit_button = tk.Button(self.button_container, text="Submit")
        self.submit_button.pack(side=tk.BOTTOM)


def get_HK_logs(pipe, ttnc_serial_port):

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

    ttnc_serial = setup_serial(ttnc_serial_port)

    print(f"telecommand is {telecommand}")
    print(f"telecommand len is {len(telecommand)}")
    ttnc_serial.write(telecommand)
    hk_bytes = ttnc_serial.read(
        ccsds_param.CCSDS_OBC_TELEMETRY_LEN_BYTES)
    # print(f"hk bytes {hk_bytes}")

    print("done sending command")
    ttnc_serial.close()
    pipe.send("open_serial")

    if hk_bytes:
        list_hk_obj = HK_Util.parse(hk_bytes)
        HK_Util.log(list_hk_obj)
        print("done do logs")
    else:
        print("hk logs failed")


def sample_process():
    i = 0
    max_val = 50000

    while i < max_val:
        print(i)
        i += 1
