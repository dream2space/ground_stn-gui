import tkinter as tk
import tkinter.ttk as ttk

from Misson_Table_Frame import MissionTableFrame


class MissionDownlinkFrame(tk.LabelFrame):
    def __init__(self, parent, controller, pos, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.pack(side=pos, anchor=tk.SW, fill="both")

        # Display table for pending mission
        self.pending_mission_table = MissionTableFrame(self, text="Pending Missions", padx=3, pady=5)

        # Display table for currently executing mission
        self.current_mission_table = MissionTableFrame(self, text="Current Missions", padx=3, pady=5)

        # Add line for Mission and Downlink command
        self.label = tk.Label(
            self, text="Send Mission + Downlink Command", pady=8)
        self.label.pack()

        # Add button to start process to send Mission and Downlink command
        self.button = tk.Button(self, text="Click here",
                                command=self.controller.open_mission_downlink_command_window)
        self.button.pack()

        # Add progress bar
        self.pbar_container = tk.Frame(self, pady=4)
        self.pbar = ttk.Progressbar(self.pbar_container, mode='indeterminate', length=100)

        # Add a success message
        self.success_message = tk.StringVar()
        self.success_label = tk.Label(self, textvariable=self.success_message)
        self.success_label.pack(side=tk.BOTTOM)

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
