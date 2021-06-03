import tkinter as tk
from tkinter import ttk


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
