import tkinter.font as tkFont
from PIL import Image, ImageTk
import tkinter as tk


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # Extract list of ports
        ports = controller.ports

        # Main container
        self.main_container = tk.Frame(self.parent)
        self.main_container.pack()

        # Create top and bottom container
        self.top_container = tk.Frame(self.main_container)
        self.bottom_container = tk.Frame(self.main_container)
        self.top_container.pack(side=tk.TOP, padx=5, pady=5)
        self.bottom_container.pack(side=tk.BOTTOM, padx=5, pady=5)

        # Create welcome and logo
        fontStyle = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.welcome = tk.Label(
            self.top_container, text="Welcome to dream2space Cubesat Ground Station!", compound=tk.CENTER, font=fontStyle)
        self.welcome.pack(side=tk.TOP, padx=5, pady=5)
        img = ImageTk.PhotoImage(Image.open("images/d2s.png").convert("RGBA"))
        self.image_logo = tk.Label(
            self.top_container, image=img, compound=tk.CENTER)
        self.image_logo.photo = img
        self.image_logo.pack(side=tk.BOTTOM, fill="both",
                             expand="yes", padx=5, pady=5)

        # Create label to prompt ttnc port selection
        self.ttnc_label = tk.Label(
            self.bottom_container, text="Select TT&C COM port")
        self.ttnc_label.grid(row=0, column=0, padx=50)

        # Setup option menu for ttnc
        self.ttnc_value_in_menu = tk.StringVar()
        self.ttnc_value_in_menu.set(ports[0])
        self.ttnc_option_menu = tk.OptionMenu(
            self.bottom_container, self.ttnc_value_in_menu, *ports)
        self.ttnc_option_menu.grid(row=1, column=0, padx=10)

        # Create label to prompt payload port selection
        self.payload_label = tk.Label(
            self.bottom_container, text="Select Payload COM port")
        self.payload_label.grid(row=0, column=2, padx=50)

        # Setup option menu for payload
        self.payload_value_in_menu = tk.StringVar()
        self.payload_value_in_menu.set(ports[0])
        self.payload_option_menu = tk.OptionMenu(
            self.bottom_container, self.payload_value_in_menu, *ports)
        self.payload_option_menu.grid(row=1, column=2, padx=10)

        # Button to confirm choice
        self.button = tk.Button(self.bottom_container, text="Start",
                                command=controller.handle_transition)
        self.button.grid(row=2, column=1, padx=40)

        # Create a label for warning
        self.warning_text = tk.StringVar()

        self.warning_label = tk.Label(
            self.bottom_container, textvariable=self.warning_text)
        self.warning_label.grid(row=3, column=1)

    def get_ttnc_port(self):
        return self.ttnc_value_in_menu.get()

    def get_payload_port(self):
        return self.payload_value_in_menu.get()

    def set_port_warning_message(self):
        self.warning_text.set("Invalid!")
