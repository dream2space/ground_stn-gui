import datetime
import tkinter as tk
from tkinter import ttk

import tkcalendar


class MissionWindow(tk.Toplevel):
    def __init__(self, parent, controller):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Mission and Downlink")

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

    def display_error_message(self):
        self.error_message_label['fg'] = 'red'

        is_future_mission = self.current_mission.mission_datetime > datetime.datetime.now()
        is_downlink_valid = self.current_mission.downlink_datetime > self.current_mission.mission_datetime

        if not is_future_mission and not is_downlink_valid:
            self.error_message.set('Error! Mission and Downlink Start time are not valid!')
        if is_future_mission and not is_downlink_valid:
            self.error_message.set('Error! Downlink Start time should be after mission time!')
        if not is_future_mission and is_downlink_valid:
            self.error_message.set('Error! Mission Start time has passed!')

    def handle_mission_success(self):
        self.destroy()


class Mission:
    def __init__(self, mission_date, downlink_date, mission_time, downlink_time, image_count, interval):
        self._parse(mission_date, downlink_date, mission_time, downlink_time, image_count, interval)

    def __str__(self):
        _1 = f"mission date: {self.mission_datetime.strftime('%d/%m/%Y')} | mission time: {self.mission_datetime.strftime('%H:%M:%S')}\n"
        _2 = f"downlink date: {self.downlink_datetime.strftime('%d/%m/%Y')} | downlink time: {self.downlink_datetime.strftime('%H:%M:%S')}\n"
        _3 = f"image count: {self.image_count} | image interval: {self.interval}"
        return _1 + _2 + _3

    def _parse(self, mission_date, downlink_date, mission_time, downlink_time, image_count, interval):

        # date format: yyyy/MM/dd
        def _parse_date(date):
            date_split = date.split('-')
            return date_split

        # time format: hh mm ss
        def _parse_time(time):
            time_split = time.split(' ')
            return time_split

        try:
            parsed_mission_date = _parse_date(mission_date)
            parsed_mission_time = _parse_time(mission_time)
            mission_date_yyyy = int(parsed_mission_date[0])
            mission_date_MM = int(parsed_mission_date[1])
            mission_date_dd = int(parsed_mission_date[2])
            mission_time_hh = int(parsed_mission_time[0])
            mission_time_mm = int(parsed_mission_time[1])
            mission_time_ss = int(parsed_mission_time[2])
            self.mission_datetime = datetime.datetime(
                year=mission_date_yyyy, month=mission_date_MM, day=mission_date_dd, hour=mission_time_hh,
                minute=mission_time_mm, second=mission_time_ss)

            parsed_downlink_date = _parse_date(downlink_date)
            parsed_downlink_time = _parse_time(downlink_time)
            downlink_date_yyyy = int(parsed_downlink_date[0])
            downlink_date_MM = int(parsed_downlink_date[1])
            downlink_date_dd = int(parsed_downlink_date[2])
            downlink_time_hh = int(parsed_downlink_time[0])
            downlink_time_mm = int(parsed_downlink_time[1])
            downlink_time_ss = int(parsed_downlink_time[2])
            self.downlink_datetime = datetime.datetime(
                year=downlink_date_yyyy, month=downlink_date_MM, day=downlink_date_dd, hour=downlink_time_hh,
                minute=downlink_time_mm, second=downlink_time_ss)

            self.image_count = int(image_count)
            self.interval = int(interval)

        except ValueError:
            # blanks found in datetime fields -> put dummy values
            self.image_count = int(image_count)
            self.interval = int(interval)

            self.mission_datetime = datetime.datetime.now()
            self.downlink_datetime = datetime.datetime.now()


class TimestampPicker(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack()
        self.parent = parent

        # Timestamp list variables
        hh_values = tuple()
        for i in range(0, 24):
            hh_values += ("{:02d}".format(i),)

        mm_values = tuple()
        for i in range(0, 60):
            mm_values += ("{:02d}".format(i),)

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
        return f"{hh} {mm} {ss}"  # return string
