import tkinter as tk
from tkinter import ttk

import tkcalendar


class MissionWindow(tk.Toplevel):
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.title("Mission and Downlink Command")

        # Container for mission and downlink widgets
        self.container = tk.Frame(self)
        self.container.pack(anchor=tk.NW, padx=30, pady=10)

        # Mission start date labelframe
        self.mission_start_date_frame = tk.LabelFrame(
            self.container, text="Mission Start Date")
        self.mission_start_date_frame.pack(expand=1, fill="both")

        # Mission start date label
        self.mission_start_date_label = tk.Label(
            self.mission_start_date_frame, text="Select Mission Start date:")
        self.mission_start_date_label.pack(side=tk.TOP)

        # Mission start calendar
        self.mission_calendar_container = tk.Frame(
            self.mission_start_date_frame)
        self.mission_calendar_container.pack(padx=5, pady=3)
        self.mission_start_calendar = tkcalendar.Calendar(
            self.mission_calendar_container)
        self.mission_start_calendar.pack(side=tk.BOTTOM)

        # Mission start time labelframe
        self.mission_start_time_frame = tk.LabelFrame(
            self.container, text="Mission Start Time")
        self.mission_start_time_frame.pack(expand=1, fill="both")

        # Mission start time label
        self.mission_start_time_container = tk.Frame(
            self.mission_start_time_frame)
        self.mission_start_time_container.pack(padx=5, pady=3)
        self.mission_start_time_label = tk.Label(
            self.mission_start_time_container, text="Select Mission Start time:")
        self.mission_start_time_label.pack()

        # Mission start time selector
        self.mission_start_time_picker_container = tk.Frame(self.mission_start_time_container)
        self.mission_start_time_picker_container.pack()
        self.mission_start_time_picker = TimestampPicker(self.mission_start_time_picker_container)

        # Mission number of images
        self.mission_number_images_frame = tk.LabelFrame(
            self.container, text="Mission Image Count")
        self.mission_number_images_frame.pack(expand=1, fill="both")

        self.image_number_selection_label = tk.Label(self.mission_number_images_frame, text="Select number of images:")
        self.image_number_selection_label.pack()

        # Mission number of image selector
        self.image_number_selection = tk.Spinbox(
            self.mission_number_images_frame, from_=1, to=3, width=5, increment=1, state='readonly',
            readonlybackground='white', justify=tk.CENTER)
        self.image_number_selection.pack(padx=5, pady=5)

        # Mission time interval frame
        self.mission_interval_frame = tk.LabelFrame(
            self.container, text="Mission Image Interval")
        self.mission_interval_frame.pack(expand=1, fill="both")
        self.interval_selection_label = tk.Label(self.mission_interval_frame,
                                                 text="Select interval between images:")
        self.interval_selection_label.pack()

        # Mission time interval selector
        self.interval_selection = tk.Spinbox(
            self.mission_interval_frame, from_=1000, to=5000, width=5, increment=1000, state='readonly',
            readonlybackground='white', justify=tk.CENTER)
        self.interval_selection.pack(padx=5, pady=5)

        # Downlink start date labelframe
        self.downlink_start_date_frame = tk.LabelFrame(
            self.container, text="Downlink Start Date")
        self.downlink_start_date_frame.pack(expand=1, fill="both")

        # Downlink start date label
        self.downlink_start_date_label = tk.Label(
            self.downlink_start_date_frame, text="Select Downlink Start date:")
        self.downlink_start_date_label.pack(side=tk.TOP)

        # Downlink start calendar
        self.downlink_calendar_container = tk.Frame(
            self.downlink_start_date_frame)
        self.downlink_calendar_container.pack(padx=5, pady=3)
        self.downlink_start_calendar = tkcalendar.Calendar(
            self.downlink_calendar_container)
        self.downlink_start_calendar.pack(side=tk.BOTTOM)

        # Downlink start time labelframe
        self.downlink_start_time_frame = tk.LabelFrame(
            self.container, text="Downlink Start Time")
        self.downlink_start_time_frame.pack(expand=1, fill="both")

        # Downlink start time label
        self.downlink_start_time_container = tk.Frame(
            self.downlink_start_time_frame)
        self.downlink_start_time_container.pack(padx=5, pady=3)
        self.downlink_start_time_label = tk.Label(
            self.downlink_start_time_container, text="Select Downlink Start time:")
        self.downlink_start_time_label.pack()

        # Downlink start time selector
        self.downlink_start_time_picker_container = tk.Frame(
            self.downlink_start_time_container)  # Container to store timestamp picker
        self.downlink_start_time_picker_container.pack()
        self.downlink_start_time_picker = TimestampPicker(self.downlink_start_time_picker_container)

        # Submit button container
        self.button_container = tk.Frame(self.container)
        self.button_container.pack()

        self.submit_button_label = tk.Label(self.button_container)
        self.submit_button_label.pack(side=tk.TOP)

        self.submit_button = tk.Button(self.button_container, text="Submit")
        self.submit_button.pack(side=tk.BOTTOM)


class TimestampPicker(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.parent = parent

        # Timestamp list variables
        hh_values = tuple()
        for i in range(0, 24):
            hh_values += ("{:02d}".format(i),)

        mm_values = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

        ss_values = tuple()
        for i in range(0, 60):
            ss_values += ("{:02d}".format(i),)

        # Setup hh container
        self.downlink_start_time_hh = tk.Frame(self.parent)
        self.downlink_start_time_hh.pack(side=tk.LEFT, padx=10, pady=3)
        self.downlink_start_time_hh_label = tk.Label(
            self.downlink_start_time_hh, text="hh")
        self.downlink_start_time_hh_label.pack(side=tk.TOP)
        self.downlink_start_time_hh_current_option = tk.StringVar()
        self.downlink_start_time_select_hh = ttk.Combobox(
            self.downlink_start_time_hh, width=4, textvariable=self.downlink_start_time_hh_current_option,
            state='readonly', values=hh_values)
        self.downlink_start_time_select_hh.pack(side=tk.BOTTOM)

        # Setup mm container
        self.downlink_start_time_mm = tk.Frame(self.parent)
        self.downlink_start_time_mm.pack(side=tk.LEFT, padx=10, pady=3)
        self.downlink_start_time_mm_label = tk.Label(
            self.downlink_start_time_mm, text="mm")
        self.downlink_start_time_mm_label.pack()
        self.downlink_start_time_mm_current_option = tk.StringVar()
        self.downlink_start_time_select_mm = ttk.Combobox(
            self.downlink_start_time_mm, width=4, textvariable=self.downlink_start_time_mm_current_option,
            state='readonly', values=mm_values)
        self.downlink_start_time_select_mm.pack(side=tk.BOTTOM)

        # Setup ss container
        self.downlink_start_time_ss = tk.Frame(self.parent)
        self.downlink_start_time_ss.pack(side=tk.RIGHT, padx=10, pady=3)
        self.downlink_start_time_ss_label = tk.Label(
            self.downlink_start_time_ss, text="ss")
        self.downlink_start_time_ss_label.pack(side=tk.TOP)
        self.downlink_start_time_ss_current_option = tk.StringVar()
        self.downlink_start_time_select_ss = ttk.Combobox(
            self.downlink_start_time_ss, width=4, textvariable=self.downlink_start_time_ss_current_option,
            state='readonly', values=ss_values)
        self.downlink_start_time_select_ss.pack(side=tk.BOTTOM)

    def get_timestamp(self):
        hh = self.downlink_start_time_hh_current_option.get()
        mm = self.downlink_start_time_mm_current_option.get()
        ss = self.downlink_start_time_ss_current_option.get()
        return {'hh': hh, 'mm': mm, 'ss': ss}  # return dictionary of strings
