import tkinter as tk
import tkinter.ttk as ttk

from Tk_Misson_Table_Frame import MissionTableFrame


class MissionDownlinkFrame(tk.LabelFrame):
    def __init__(self, parent, controller, pos, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.pack(side=pos, anchor=tk.SW, fill="both")

        # Label frame for sending mission
        self.mission_labelframe = tk.LabelFrame(self, text="Send Mission / Downlink command", padx=3, pady=5)
        self.mission_labelframe.pack(fill="both", expand=True)

        # Add line for Mission and Downlink command
        self.label = tk.Label(
            self.mission_labelframe, text="Send Mission / Downlink Command", pady=8)
        self.label.pack()

        # Add button to start process to send Mission and Downlink command
        self.button = tk.Button(self.mission_labelframe, text="Click here",
                                command=self.controller.open_mission_downlink_command_window)
        self.button.pack()

        # Add progress bar
        self.pbar_container = tk.Frame(self.mission_labelframe, pady=4)
        self.pbar = ttk.Progressbar(self.pbar_container, mode='indeterminate', length=100)

        # Add a success message
        self.success_message = tk.StringVar()
        self.success_label = tk.Label(self.mission_labelframe, textvariable=self.success_message)
        self.success_label.pack(side=tk.BOTTOM)

        # Display table for pending mission
        self.pending_mission_table = MissionTableFrame(
            self, table_height=3, text="Missions Pending Downlink", padx=3, pady=5)

        # Display table for currently executing mission
        self.current_mission_table = MissionTableFrame(
            self, table_height=1, text="Missions Currently in Downlink", padx=3, pady=5)

        # Label frame for completed missions
        self.completed_missions_labelframe = tk.LabelFrame(self, text="Completed Missions / Downlinks", padx=3, pady=5)
        self.completed_missions_labelframe.pack(fill="both", expand=True)

        # Add label for completed Mission and Downlink section
        self.completed_missions_label = tk.Label(
            self.completed_missions_labelframe, text="View Completed Missions / Downlinks", pady=5)
        self.completed_missions_label.pack()

        # Add button to view Mission and Downlink
        self.view_completed_missions_button = tk.Button(self.completed_missions_labelframe, text="Click here",
                                                        command=self.controller.view_completed_missions)
        self.view_completed_missions_button.pack()

    def display_add_success_msg(self):
        self.success_message.set("Success! Sending command to Cubesat!")
        self.success_label['fg'] = 'green'

    def clear_success_message(self):
        self.success_message.set(" ")

    def show_progress_bar(self):
        # Remove button
        self.button.pack_forget()

        # Show up progress bar
        self.pbar_container.pack()
        self.pbar.pack()
        self.pbar.start()

    # Stop progress bar and reinstate button
    def stop_mission_block(self):
        # Stop progress bar and destroy
        self.pbar.stop()
        self.pbar_container.pack_forget()

        # Reinstate button
        self.button.pack()

        # Stop message display
        self.clear_success_message()

    def disable_mission_command(self):
        self.show_progress_bar()
