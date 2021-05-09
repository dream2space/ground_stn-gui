import tkinter as tk


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
