import App_Parameters as app_param
import tkinter as tk


class Command_Panel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=app_param.APP_WIDTH/2,
                          height=app_param.APP_HEIGHT, padx=10, pady=10)
        self.parent = parent

        # Create container to store all subsections
        self.container = tk.Frame(self)
        self.container.pack(expand=1, fill="both")

        # Create section to request for housekeeping data
        self.housekeeping_command = HousekeepingDataFrame(
            self.container, text="Housekeeping Command", padx=10, pady=8)

        # Create section for mission and downlink
        self.mission_command = MissionDownlinkFrame(
            self.container, text="Mission and Downlink Command", padx=10, pady=8)


class HousekeepingDataFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=tk.TOP, anchor=tk.NW, expand=1, fill="both")

        self.label = tk.Label(self, text="test")
        self.label.pack()


class MissionDownlinkFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=tk.BOTTOM, anchor=tk.SW, expand=1, fill="both")

        self.label = tk.Label(self, text="test")
        self.label.pack()
