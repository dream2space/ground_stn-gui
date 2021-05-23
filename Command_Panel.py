import tkinter as tk
import tkinter.ttk as ttk

import App_Parameters as app_param


class CommandPanel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=app_param.APP_WIDTH/2,
                          height=app_param.APP_HEIGHT, padx=10, pady=10)
        self.parent = parent
        self.controller = controller

        # Create container to store all subsections
        self.container = tk.Frame(self)
        self.container.pack(expand=1, fill="both")

        # Create section to request for housekeeping data
        self.housekeeping_command = HousekeepingDataFrame(
            self.container, self.controller, text="Housekeeping Command", padx=10, pady=8)

        # Create section for mission and downlink
        self.mission_command = MissionDownlinkFrame(
            self.container, self.controller,  text="Mission and Downlink Command", padx=10, pady=8)


class HousekeepingDataFrame(tk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=tk.TOP, anchor=tk.NW, expand=1, fill="both")

        # Add line for Housekeeping data
        self.label = tk.Label(
            self, text="Request for Housekeeping data", pady=8)
        self.label.pack()

        # Add button to trigger housekeeping data command
        self.start_hk_button = tk.Button(
            self, text="Click here", command=controller.hk_process)
        self.start_hk_button.pack()

        # Progress bar
        self.pbar_container = tk.Frame(self, pady=4)
        self.pbar_container.pack()
        self.pbar = ttk.Progressbar(
            self.pbar_container, mode='indeterminate', length=100)

        # Outcome message
        self.outcome_message = tk.StringVar()
        self.outcome_message_label = tk.Label(
            self, textvariable=self.outcome_message)
        self.outcome_message_label.pack()


class MissionDownlinkFrame(tk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.pack(side=tk.BOTTOM, anchor=tk.SW, expand=1, fill="both")

        # Add line for Mission and Downlink command
        self.label = tk.Label(
            self, text="Send Mission + Downlink Command")
        self.label.pack()

        # Add button to start process to send Mission and Downlink command
        self.button = tk.Button(self, text="Click here", pady=8,
                                command=self.controller.open_mission_downlink_command_window)
        self.button.pack()
