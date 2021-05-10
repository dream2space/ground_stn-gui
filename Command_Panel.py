import App_Parameters as app_param
import tkinter as tk


class Command_Panel(tk.Frame):
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
            self.container, text="Mission and Downlink Command", padx=10, pady=8)


class HousekeepingDataFrame(tk.LabelFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=tk.TOP, anchor=tk.NW, expand=1, fill="both")

        # Add line for Housekeeping data
        self.label = tk.Label(self, text="Housekeeping data")
        self.label.pack()

        # Add button to trigger housekeeping data command
        self.start_hk_button = tk.Button(
            self, text="Click here", command=controller.start_hk_process)
        self.start_hk_button.pack()


class MissionDownlinkFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=tk.BOTTOM, anchor=tk.SW, expand=1, fill="both")

        # Add line for Mission and Downlink command
        self.label = tk.Label(self, text="test")
        self.label.pack()
