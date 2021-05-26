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


class MissionTable(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Display currently pending missions
        column_id = (1, 2, 3, 4)
        column_names = ('Mission Start', 'Downlink Start', 'Count', 'Interval')
        self.mission_pending_view = ttk.Treeview(self.parent, column=column_id, show='headings', height=3)
        self.mission_pending_view.pack(padx=2, pady=2)

        # Setup column in treeview table for datetimes
        self.mission_pending_view.column(column_id[0], width=140, anchor=tk.CENTER)
        self.mission_pending_view.heading(column_id[0], text=column_names[0], anchor=tk.CENTER)
        self.mission_pending_view.column(column_id[1], width=140, anchor=tk.CENTER)
        self.mission_pending_view.heading(column_id[1], text=column_names[1], anchor=tk.CENTER)

        # Setup column in treeview table for count and interval
        self.mission_pending_view.column(column_id[2], width=60, anchor=tk.CENTER)
        self.mission_pending_view.heading(column_id[2], text=column_names[2], anchor=tk.CENTER)
        self.mission_pending_view.column(column_id[3], width=60, anchor=tk.CENTER)
        self.mission_pending_view.heading(column_id[3], text=column_names[3], anchor=tk.CENTER)

    # Add a mission entry into table
    def update_mission_entry(self, mission_list):
        pass
        iid = 0
        for mission in mission_list:
            self.mission_pending_view.insert(
                parent='', index=iid, iid=iid,
                values=(mission.get_mission_datetime_string(),
                        mission.get_downlink_datetime_string(),
                        mission.image_count, mission.interval))
            iid += 1
