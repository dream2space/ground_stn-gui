import tkinter as tk


class MainApp(tk.Frame):
    def __init__(self, parent, pipe, ports):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.minsize(450, 80)
        self.parent.title("Ground Station")

        # Beacon pipes
        self.pipe = pipe

        # Serial ports
        self.ports = ports

        # Put all pages into container
        self.container = tk.Frame(self.parent)
        self.container.grid()
        self.make_start_page()

    def make_start_page(self):
        self.start = StartPage(self.container, self)

    def make_ground_page(self):
        self.container.grid_forget()
        self.container = tk.Frame(self.parent)
        self.ground = GroundStationPage(self.parent, self.pipe)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Create and display select port
        ttnc_label = tk.Label(self.parent, text="Select TT&C COM port")
        ttnc_label.grid(row=0, column=0, padx=50, pady=10)

        ports = controller.ports

        ttnc_value_in_menu = tk.StringVar()
        ttnc_value_in_menu.set(ports[0])
        ttnc_option_menu = tk.OptionMenu(
            self.parent, ttnc_value_in_menu, *ports)
        ttnc_option_menu.grid(row=1, column=0, padx=10, pady=10)

        payload_label = tk.Label(self.parent, text="Select Payload COM port")
        payload_label.grid(row=0, column=2, padx=50, pady=10)

        payload_value_in_menu = tk.StringVar()
        payload_value_in_menu.set(ports[0])
        payload_option_menu = tk.OptionMenu(
            self.parent, payload_value_in_menu, *ports)
        payload_option_menu.grid(row=1, column=2, padx=10, pady=10)

        # Button to confirm
        b = tk.Button(self.parent, text="Start",
                      command=controller.make_ground_page)
        b.grid(row=2, column=1, padx=40, pady=10)


class GroundStationPage(tk.Frame):
    def __init__(self, parent, pipe):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Create a section/labelframe for beacon data
        self.beacon_pipe = pipe
        self.beacon_frame = BeaconFrame(self.parent, text="Beacon Data")
        self.parent.after(1000, self.update_beacon_values)

    def update_beacon_values(self):
        if self.beacon_pipe.poll():
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
        self.gx = tk.StringVar()
        self.gy = tk.StringVar()
        self.gz = tk.StringVar()

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

        self.update_beacon_values("0.0", "0", "0", "0")

    def update_beacon_values(self, temp, gx, gy, gz):
        self.temp.set(temp)
        self.gx.set(gx)
        self.gy.set(gy)
        self.gz.set(gz)

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
