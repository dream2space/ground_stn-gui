import tkinter as tk
import tkinter.ttk as ttk


class MissionDownlinkFrame(tk.LabelFrame):
    def __init__(self, parent, controller, pos, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.pack(side=pos, anchor=tk.SW, fill="both")

        # Display table for pending mission
        self.pending_mission_table = MissionTable(self)

        # Add line for Mission and Downlink command
        self.label = tk.Label(
            self, text="Send Mission + Downlink Command", pady=8)
        self.label.pack()

        # Add button to start process to send Mission and Downlink command
        self.button = tk.Button(self, text="Click here",
                                command=self.controller.open_mission_downlink_command_window)
        self.button.pack()

        # Add a success message
        self.success_message = tk.StringVar()
        self.success_label = tk.Label(self, textvariable=self.success_message)
        self.success_label.pack()


class MissionTable(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        ttk.Treeview.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Display currently pending missions
        col = (1, 2, 3)
        self.mission_pending_view = ttk.Treeview(self.parent, columns=col, show='headings', height=3)
        self.mission_pending_view.pack(padx=2, pady=2)

        # Setup columns in treeview table
        for i in range(len(col)):
            self.mission_pending_view.column(col[i], width=100, anchor='e')
