import datetime
import tkinter as tk

import tkcalendar

from Mission import Mission
from Tk_Timestamp_Picker import TimestampPicker


class MissionWindow(tk.Toplevel):
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Mission and Downlink")

        self.grab_set()  # only allow window to react

        self.controller = controller

        # Container for mission and downlink widgets
        self.container = tk.Frame(self)
        self.container.pack(padx=30, pady=10)

        self.top_container = tk.Frame(self.container)
        self.top_container.pack()

        self.bottom_container = tk.Frame(self.container)
        self.bottom_container.pack()

        self.mission_timestamp_container = tk.Frame(self.top_container)
        self.mission_timestamp_container.pack(side=tk.LEFT, padx=10, pady=10)

        self.mission_definition_container = tk.Frame(self.top_container)
        self.mission_definition_container.pack(side=tk.LEFT, padx=10, pady=10, expand=1, fill="both")

        self.downlink_timestamp_container = tk.Frame(self.top_container)
        self.downlink_timestamp_container.pack(side=tk.RIGHT, padx=10, pady=10)

        # Mission start date labelframe
        self.mission_start_date_frame = tk.LabelFrame(
            self.mission_timestamp_container, text="Mission Start Date")
        self.mission_start_date_frame.pack(expand=1, fill="both", padx=3, pady=3)

        # Mission start date label
        self.mission_start_date_label = tk.Label(
            self.mission_start_date_frame, text="Select Mission Start date:")
        self.mission_start_date_label.pack(side=tk.TOP)

        # Mission start calendar
        self.mission_calendar_container = tk.Frame(
            self.mission_start_date_frame)
        self.mission_calendar_container.pack(padx=5, pady=3)
        self.mission_start_calendar = tkcalendar.Calendar(
            self.mission_calendar_container, date_pattern='y-mm-dd')
        self.mission_start_calendar.pack(side=tk.BOTTOM)

        # Mission start time labelframe
        self.mission_start_time_frame = tk.LabelFrame(
            self.mission_timestamp_container, text="Mission Start Time")
        self.mission_start_time_frame.pack(expand=True, fill="both", padx=3, pady=3)

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
            self.mission_definition_container, text="Mission Image Count")
        self.mission_number_images_frame.pack(expand=1, fill="both", padx=3, pady=3)

        self.mission_number_images_container = tk.Frame(self.mission_number_images_frame)
        self.mission_number_images_container.pack(
            padx=5, pady=5, expand=True, fill="none")  # Centralize the widget in labelframe

        self.image_number_selection_label = tk.Label(
            self.mission_number_images_container, text="Select images count:")
        self.image_number_selection_label.pack()

        # Mission number of image selector
        self.image_number_selection = tk.Spinbox(
            self.mission_number_images_container, from_=1, to=3, width=5, increment=1, state='readonly',
            readonlybackground='white', justify=tk.CENTER)
        self.image_number_selection.pack(padx=5, pady=5)

        # Mission time interval container
        self.mission_interval_frame = tk.LabelFrame(
            self.mission_definition_container, text="Mission Image Interval")
        self.mission_interval_frame.pack(expand=True, fill="both", padx=3, pady=3)

        self.mission_time_interval_container = tk.Frame(self.mission_interval_frame)
        self.mission_time_interval_container.pack(
            padx=5, pady=5, expand=True, fill="none")  # Centralize the widget in labelframe

        # Mission time interval label
        self.interval_selection_label = tk.Label(self.mission_time_interval_container,
                                                 text="Select image interval :")
        self.interval_selection_label.pack()

        # Mission time interval selector
        self.interval_selection = tk.Spinbox(
            self.mission_time_interval_container, from_=1000, to=5000, width=5, increment=1000, state='readonly',
            readonlybackground='white', justify=tk.CENTER)
        self.interval_selection.pack()

        # Downlink start date labelframe
        self.downlink_start_date_frame = tk.LabelFrame(
            self.downlink_timestamp_container, text="Downlink Start Date")
        self.downlink_start_date_frame.pack(expand=1, fill="both", padx=3, pady=3)

        # Downlink start date label
        self.downlink_start_date_label = tk.Label(
            self.downlink_start_date_frame, text="Select Downlink Start date:")
        self.downlink_start_date_label.pack(side=tk.TOP)

        # Downlink start calendar
        self.downlink_calendar_container = tk.Frame(
            self.downlink_start_date_frame)
        self.downlink_calendar_container.pack(padx=5, pady=3)
        self.downlink_start_calendar = tkcalendar.Calendar(
            self.downlink_calendar_container, date_pattern='y-mm-dd')
        self.downlink_start_calendar.pack(side=tk.BOTTOM)

        # Downlink start time labelframe
        self.downlink_start_time_frame = tk.LabelFrame(
            self.downlink_timestamp_container, text="Downlink Start Time")
        self.downlink_start_time_frame.pack(expand=1, fill="both", padx=3, pady=3)

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

        # Error message
        self.error_message = tk.StringVar()
        self.error_message_label = tk.Label(self.bottom_container, textvariable=self.error_message)
        self.error_message_label.pack(side=tk.TOP)

        # Submit button container
        self.button_container = tk.Frame(self.bottom_container)
        self.button_container.pack(side=tk.BOTTOM)
        self.submit_button = tk.Button(self.button_container, text="Submit",
                                       command=self.controller.handle_mission_scheduling)
        self.submit_button.pack(padx=5, pady=5)

    def get_user_mission_input(self):
        mission_date = self.mission_start_calendar.get_date()
        downlink_date = self.downlink_start_calendar.get_date()
        mission_time = self.mission_start_time_picker.get_timestamp()
        downlink_time = self.downlink_start_time_picker.get_timestamp()
        image_count = self.image_number_selection.get()
        interval = self.interval_selection.get()
        self.current_mission = Mission(mission_date, downlink_date, mission_time, downlink_time, image_count, interval)
        return self.current_mission

    def display_error_message(self, num_current_missions):
        self.error_message_label['fg'] = 'red'

        is_future_mission = self.current_mission.mission_datetime > datetime.datetime.now()
        is_downlink_valid = self.current_mission.downlink_datetime > self.current_mission.mission_datetime

        if num_current_missions >= 3:
            self.error_message.set('Error! There should be not more than 3 pending missions!')
        elif not is_future_mission and not is_downlink_valid:
            self.error_message.set('Error! Mission and Downlink Start time are not valid!')
        elif is_future_mission and not is_downlink_valid:
            self.error_message.set('Error! Downlink Start time should be after mission time!')
        elif not is_future_mission and is_downlink_valid:
            self.error_message.set('Error! Mission Start time has passed!')

    def handle_mission_success(self):
        self.destroy()
