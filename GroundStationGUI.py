from Mission_Window import MissionWindow
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
import subprocess
import serial
import glob
import sys
import os


class MainApp(tk.Frame):
    def __init__(self, parent, pipe_beacon):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False)
        self.parent.title("Ground Station")

        # Scan for serial ports
        ports = self.scan_serial_ports()
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

    def scan_serial_ports(self):
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

        result.insert(0, " ")

        # In testing, add dummy entries
        if IS_TESTING:
            result.append("COM14")
            result.append("COM15")

        return result

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
        self.mission_window = MissionWindow(self.parent, self)


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
