from Testing import IS_TESTING
import tkinter as tk
import serial


APP_HEIGHT = 300
APP_WIDTH = 900


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

            # Generate Containter to store new page
            self.container = tk.Frame(
                self.parent, width=APP_WIDTH, height=APP_HEIGHT)
            self.container.pack()

            # Generate Beacon page for left
            self.beacon = BeaconPanel(self.container, self.pipe_beacon)
            self.beacon.pack(side=tk.RIGHT, anchor=tk.NW)

            self.command = tk.Frame(
                self.container, width=APP_WIDTH/2, height=APP_HEIGHT)
            self.command.pack(side=tk.LEFT)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Extract list of ports
        ports = controller.ports

        # Create label to prompt ttnc port selection
        self.ttnc_label = tk.Label(self.parent, text="Select TT&C COM port")
        self.ttnc_label.grid(row=0, column=0, padx=50)

        # Setup option menu for ttnc
        self.ttnc_value_in_menu = tk.StringVar()
        self.ttnc_value_in_menu.set(ports[0])
        self.ttnc_option_menu = tk.OptionMenu(
            self.parent, self.ttnc_value_in_menu, *ports)
        self.ttnc_option_menu.grid(row=1, column=0, padx=10)

        # Create label to prompt payload port selection
        self.payload_label = tk.Label(
            self.parent, text="Select Payload COM port")
        self.payload_label.grid(row=0, column=2, padx=50)

        # Setup option menu for payload
        self.payload_value_in_menu = tk.StringVar()
        self.payload_value_in_menu.set(ports[0])
        self.payload_option_menu = tk.OptionMenu(
            self.parent, self.payload_value_in_menu, *ports)
        self.payload_option_menu.grid(row=1, column=2, padx=10)

        # Button to confirm choice
        self.button = tk.Button(self.parent, text="Start",
                                command=controller.handle_transition)
        self.button.grid(row=2, column=1, padx=40)

        # Create a label for warning
        self.warning_text = tk.StringVar()

        self.warning_label = tk.Label(
            self.parent, textvariable=self.warning_text)
        self.warning_label.grid(row=3, column=1)

    def get_ttnc_port(self):
        return self.ttnc_value_in_menu.get()

    def get_payload_port(self):
        return self.payload_value_in_menu.get()

    def set_port_warning_message(self):
        self.warning_text.set("Invalid!")


class BeaconPanel(tk.Frame):
    def __init__(self, parent, pipe):
        tk.Frame.__init__(self, parent, width=APP_WIDTH/2,
                          height=APP_HEIGHT, padx=10, pady=10)
        self.parent = parent

        # Create a section/labelframe for beacon data
        self.beacon_pipe = pipe
        self.beacon_frame = BeaconFrame(
            self, text="Beacon Data", padx=10, pady=8)
        self.parent.after(1000, self.update_beacon_values)

    def update_beacon_values(self):
        if self.beacon_pipe.poll(timeout=0):
            ls = self.beacon_pipe.recv()
            temp = ls[0]
            gx = ls[1]
            gy = ls[2]
            gz = ls[3]
            self.beacon_frame.update_beacon_values(temp, gx, gy, gz)
        self.parent.after(1000, self.update_beacon_values)


class BeaconFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack()

        # Create variable to store beacon values
        self.temp = tk.StringVar()
        self.temp.set("0.00")
        self.gx = tk.StringVar()
        self.gx.set("0")
        self.gy = tk.StringVar()
        self.gy.set("0")
        self.gz = tk.StringVar()
        self.gz.set("0")

        # Create label for beacon data header
        self.temperature_label = self._create_header_label("Temp")
        self.gx_label = self._create_header_label("GX")
        self.gy_label = self._create_header_label("GY")
        self.gz_label = self._create_header_label("GZ")

        # Create label to store beacon data
        self.temp_text = self._create_text_label(self.temp)
        self.gx_text = self._create_text_label(self.gx)
        self.gy_text = self._create_text_label(self.gy)
        self.gz_text = self._create_text_label(self.gz)

        # Put the labels in grids with row/col
        self._arrange_grid()

    def update_beacon_values(self, temp, gx, gy, gz):
        def uncolor():
            self.temperature_label['bg'] = 'grey94'
            self.gx_label['bg'] = 'grey94'
            self.gy_label['bg'] = 'grey94'
            self.gz_label['bg'] = 'grey94'

        self.temp.set(temp)
        self.gx.set(gx)
        self.gy.set(gy)
        self.gz.set(gz)

        self.temperature_label['bg'] = 'yellow'
        self.gx_label['bg'] = 'yellow'
        self.gy_label['bg'] = 'yellow'
        self.gz_label['bg'] = 'yellow'
        self.parent.after(1200, uncolor)

    def _create_header_label(self, header_text):
        return tk.Label(self, width=6, text=header_text, borderwidth=1, relief="groove")

    def _create_text_label(self, text_container):
        return tk.Label(self, width=6, textvariable=text_container,
                        bg="white", borderwidth=1, relief="groove")

    def _arrange_grid(self):
        self.temperature_label.grid(row=0, column=0)
        self.gx_label.grid(row=0, column=2)
        self.gy_label.grid(row=0, column=4)
        self.gz_label.grid(row=0, column=6)

        self.temp_text.grid(row=0, column=1)
        self.gx_text.grid(row=0, column=3)
        self.gy_text.grid(row=0, column=5)
        self.gz_text.grid(row=0, column=7)
