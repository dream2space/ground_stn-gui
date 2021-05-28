import tkinter as tk
import tkinter.ttk as ttk


class MissionTableFrame(tk.LabelFrame):
    def __init__(self, parent, table_height, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack()

        self.container = tk.Frame(self)
        self.container.pack()

        # Display currently pending missions
        column_id = (1, 2, 3, 4)
        column_names = ('Mission Start', 'Downlink Start', 'Count', 'Interval')
        self.mission_pending_view = ttk.Treeview(
            self.container, column=column_id, show='headings', selectmode='none', height=table_height)
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
        # Clear list
        self.mission_pending_view.delete(*self.mission_pending_view.get_children())

        # Add each entry into list
        iid = 0
        for mission in mission_list:
            self.mission_pending_view.insert(
                parent='', index=iid, iid=iid,
                values=(mission.get_mission_datetime_string(),
                        mission.get_downlink_datetime_string(),
                        mission.image_count, mission.interval))
            iid += 1
