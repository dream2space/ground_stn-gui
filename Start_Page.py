from PIL import Image, ImageTk
import tkinter.font as tkFont
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

        # Create holding containers
        self.top_container = tk.Frame(self.main_container)
        self.middle_up_container = tk.Frame(self.main_container)
        self.middle_down_container = tk.Frame(self.main_container)
        self.bottom_container = tk.Frame(self.main_container)
        self.top_container.pack(side=tk.TOP, padx=10, pady=10)
        self.middle_up_container.pack(padx=10)
        self.middle_down_container.pack(padx=10)
        self.bottom_container.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create welcome and logo
        welcome_fontStyle = tkFont.Font(
            family="Helvetica", size=14, weight="bold")
        self.welcome = tk.Label(
            self.top_container, text="Welcome to dream2space Cubesat Ground Station!", compound=tk.CENTER, font=welcome_fontStyle)
        self.welcome.pack(side=tk.TOP, padx=5, pady=5)
        img = ImageTk.PhotoImage(Image.open("assets/d2s.png").convert("RGBA"))
        self.image_logo = tk.Label(self.top_container, image=img)
        self.image_logo.photo = img
        self.image_logo.pack(side=tk.BOTTOM, fill="both",
                             expand="yes", padx=5, pady=5)

        # Create a label for messages and warning
        self.warning_container = tk.Frame(self.middle_up_container)
        self.warning_container.pack(side=tk.TOP)
        self.display_instruction_message(self.warning_container)

        # Create left and right for bottom container
        self.middle_left_container = tk.Frame(self.middle_up_container)
        self.middle_right_container = tk.Frame(self.middle_up_container)
        self.middle_left_container.pack(side=tk.LEFT, padx=40)
        self.middle_right_container.pack(side=tk.RIGHT, padx=40)

        # Create label to prompt ttnc port selection
        self.ttnc_label = tk.Label(
            self.middle_left_container, text="Select TT&C COM port")
        self.ttnc_label.pack(side=tk.TOP)

        # Setup option menu for ttnc
        self.ttnc_value_in_menu = tk.StringVar()
        self.ttnc_value_in_menu.set(ports[0])
        self.ttnc_option_menu = tk.OptionMenu(
            self.middle_left_container, self.ttnc_value_in_menu, *ports)
        self.ttnc_option_menu.pack(side=tk.BOTTOM)

        # Create label to prompt payload port selection
        self.payload_label = tk.Label(
            self.middle_right_container, text="Select Payload COM port")
        self.payload_label.pack(side=tk.TOP, anchor=tk.CENTER)

        # Setup option menu for payload
        self.payload_value_in_menu = tk.StringVar()
        self.payload_value_in_menu.set(ports[0])
        self.payload_option_menu = tk.OptionMenu(
            self.middle_right_container, self.payload_value_in_menu, *ports)
        self.payload_option_menu.pack(side=tk.BOTTOM)

        # Button to confirm choice
        self.button_container = tk.Frame(self.middle_down_container)
        self.button_container.pack(side=tk.BOTTOM)
        self.button = tk.Button(self.button_container, text="Start",
                                compound=tk.CENTER, command=controller.handle_transition)
        self.button.pack()

        # Button to hit refresh
        self.refresh_container = tk.Frame(self.bottom_container)
        self.refresh_container.pack(side=tk.RIGHT)
        refresh_image = ImageTk.PhotoImage(
            Image.open("assets/refresh.jpg").resize((20, 20)))
        self.refresh_button = tk.Button(
            self.refresh_container, text="Refresh ", image=refresh_image, compound=tk.RIGHT)
        self.refresh_button.photo = refresh_image
        self.refresh_button.pack(expand=True)

    def get_ttnc_port(self):
        return self.ttnc_value_in_menu.get()

    def get_payload_port(self):
        return self.payload_value_in_menu.get()

    def set_port_warning_message(self):
        self.warning_label['fg'] = 'red'
        self.warning_text.set("Invalid!")
        self.warning_label.pack()
        self.after(2000, self.reset_instruction_message)

    def display_instruction_message(self, parent):
        self.warning_fontStyle = tkFont.Font(
            family="TkDefaultFont", weight="bold", size=10)
        self.warning_text = tk.StringVar()
        self.warning_text.set(
            "To begin, select the COM ports for TT&C and Payload transceivers.")
        self.warning_label = tk.Label(
            parent, textvariable=self.warning_text, compound=tk.CENTER, font=self.warning_fontStyle)
        self.warning_label.pack(side=tk.TOP, padx=3, pady=3)

    def reset_instruction_message(self):
        self.warning_label['fg'] = 'black'
        self.warning_text.set(
            "To begin, select the COM ports for TT&C and Payload transceivers.")
        self.warning_label.pack()
