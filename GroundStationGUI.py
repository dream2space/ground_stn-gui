from multiprocessing.context import Process
from Command_Panel import Command_Panel
from Beacon_Panel import BeaconPanel
import App_Parameters as app_param
from Start_Page import StartPage
from Testing import IS_TESTING
import tkinter as tk
import serial


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
            self.ttnc_ser = None
            if not IS_TESTING:
                # Setup ttnc port serial object
                self.ttnc_ser = serial.Serial(self.port_ttnc)
                self.ttnc_ser.baudrate = 9600
                self.ttnc_ser.timeout = 0.5

            # Pass ttnc serial object via pipe to thread
            self.pipe_beacon.send(self.ttnc_ser)

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

    def start_hk_process(self):
        self.p1 = Process(target=sample_process)
        self.p1.start()


def sample_process():
    i = 0
    while i < 1000000:
        print(i)
        i += 1
