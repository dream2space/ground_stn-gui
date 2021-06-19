import tkinter as tk

import App_Parameters as app_param


class BeaconPanel(tk.Frame):
    def __init__(self, parent, pipe):
        tk.Frame.__init__(self, parent, width=app_param.APP_WIDTH/2,
                          height=app_param.APP_HEIGHT, padx=10, pady=10)
        self.parent = parent
        self.beacon_pipe = pipe

        # Create container to store all subsections
        self.container = tk.Frame(self)
        self.container.pack()

        # Create a section/labelframe for beacon data
        self.beacon_frame = BeaconFrame(
            self.container, text="Beacon Data", padx=10, pady=8)
        self.parent.after(10, self.update_beacon_values)

    def update_beacon_values(self):
        if self.beacon_pipe.poll(timeout=0):
            ls = self.beacon_pipe.recv()
            temp = ls[0]
            gx = ls[1]
            gy = ls[2]
            gz = ls[3]
            adc = ls[4]
            ax = ls[5]
            ay = ls[6]
            az = ls[7]
            self.beacon_frame.update_beacon_values(temp, gx, gy, gz, adc, ax, ay, az)
        self.parent.after(500, self.update_beacon_values)


class BeaconFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack()

        # Create variable to store beacon values
        self.temp = tk.StringVar()
        self.temp.set("0.00")
        self.adc = tk.StringVar()
        self.adc.set("0.00")
        self.gx = tk.StringVar()
        self.gx.set("0")
        self.gy = tk.StringVar()
        self.gy.set("0")
        self.gz = tk.StringVar()
        self.gz.set("0")
        self.ax = tk.StringVar()
        self.ax.set("0")
        self.ay = tk.StringVar()
        self.ay.set("0")
        self.az = tk.StringVar()
        self.az.set("0")
        self.timestamp_date = tk.StringVar()
        self.timestamp_date.set("0")
        self.timestamp_time = tk.StringVar()
        self.timestamp_time.set("0")

        # Label for timestamp
        self.timestamp_header_label = tk.Label(self, text="Timestamp data")
        self.timestamp_header_label.pack(anchor=tk.NW)

        # Create container for timestamp data
        self.timestamp_data_container = tk.Frame(self)
        self.timestamp_data_container.pack(anchor=tk.NW, pady=2)
        self.timestamp_date_label = self._create_header_label(self.timestamp_data_container, "Date")
        self.timestamp_time_label = self._create_header_label(self.timestamp_data_container, "Time")
        self.timestamp_date_text = self._create_text_label(self.timestamp_data_container, self.timestamp_date)
        self.timestamp_time_text = self._create_text_label(self.timestamp_data_container, self.timestamp_time)
        self._arrange_timestamp_grid()

        # Label for EPS data
        self.eps_header_label = tk.Label(self, text="EPS data")
        self.eps_header_label.pack(anchor=tk.NW, pady=2)

        # Create container for EPS data
        self.eps_data_container = tk.Frame(self)
        self.eps_data_container.pack(anchor=tk.NW, pady=2)
        self.temperature_label = self._create_header_label(self.eps_data_container, "Temp")
        self.adc_label = self._create_header_label(self.eps_data_container, "Vbatt")
        self.temp_text = self._create_text_label(self.eps_data_container, self.temp)
        self.adc_text = self._create_text_label(self.eps_data_container, self.adc)
        self._arrange_eps_grid()

        # Label for ADCS data
        self.adcs_header_label = tk.Label(self, text="ADCS data")
        self.adcs_header_label.pack(anchor=tk.NW, pady=2)

        # Create container for ADCS data
        self.adcs_data_container = tk.Frame(self)
        self.adcs_data_container.pack(anchor=tk.NW)
        self.gx_label = self._create_header_label(self.adcs_data_container, "GX")
        self.gy_label = self._create_header_label(self.adcs_data_container, "GY")
        self.gz_label = self._create_header_label(self.adcs_data_container, "GZ")
        self.gx_text = self._create_text_label(self.adcs_data_container, self.gx)
        self.gy_text = self._create_text_label(self.adcs_data_container, self.gy)
        self.gz_text = self._create_text_label(self.adcs_data_container, self.gz)
        self.ax_label = self._create_header_label(self.adcs_data_container, "AX")
        self.ay_label = self._create_header_label(self.adcs_data_container, "AY")
        self.az_label = self._create_header_label(self.adcs_data_container, "AZ")
        self.ax_text = self._create_text_label(self.adcs_data_container, self.ax)
        self.ay_text = self._create_text_label(self.adcs_data_container, self.ay)
        self.az_text = self._create_text_label(self.adcs_data_container, self.az)
        self._arrange_adcs_grid()

    def update_beacon_values(self, temp, gx, gy, gz, adc, ax, ay, az):
        def uncolor():
            self.temperature_label['bg'] = 'grey94'
            self.gx_label['bg'] = 'grey94'
            self.gy_label['bg'] = 'grey94'
            self.gz_label['bg'] = 'grey94'
            self.adc_label['bg'] = 'grey94'
            self.ax_label['bg'] = 'grey94'
            self.ay_label['bg'] = 'grey94'
            self.az_label['bg'] = 'grey94'
            self.timestamp_date_label['bg'] = 'grey94'
            self.timestamp_time_label['bg'] = 'grey94'

        self.temp.set(temp)
        self.gx.set(gx)
        self.gy.set(gy)
        self.gz.set(gz)
        self.adc.set(adc)
        self.ax.set(ax)
        self.ay.set(ay)
        self.az.set(az)

        self.temperature_label['bg'] = 'yellow'
        self.gx_label['bg'] = 'yellow'
        self.gy_label['bg'] = 'yellow'
        self.gz_label['bg'] = 'yellow'
        self.ax_label['bg'] = 'yellow'
        self.ay_label['bg'] = 'yellow'
        self.az_label['bg'] = 'yellow'
        self.adc_label['bg'] = 'yellow'
        self.timestamp_date_label['bg'] = 'yellow'
        self.timestamp_time_label['bg'] = 'yellow'
        self.parent.after(1200, uncolor)

    def _create_header_label(self, parent, header_text):
        return tk.Label(parent, width=8, text=header_text, borderwidth=1, relief="groove")

    def _create_text_label(self, parent, text_container):
        return tk.Label(parent, width=10, textvariable=text_container,
                        bg="white", borderwidth=1, relief="groove")

    def _arrange_eps_grid(self):
        self.temperature_label.grid(row=0, column=0)
        self.adc_label.grid(row=0, column=2)
        self.temp_text.grid(row=0, column=1)
        self.adc_text.grid(row=0, column=3)

    def _arrange_adcs_grid(self):
        self.gx_label.grid(row=1, column=0)
        self.gy_label.grid(row=1, column=2)
        self.gz_label.grid(row=1, column=4)
        self.ax_label.grid(row=0, column=0)
        self.ay_label.grid(row=0, column=2)
        self.az_label.grid(row=0, column=4)

        self.gx_text.grid(row=1, column=1)
        self.gy_text.grid(row=1, column=3)
        self.gz_text.grid(row=1, column=5)
        self.ax_text.grid(row=0, column=1)
        self.ay_text.grid(row=0, column=3)
        self.az_text.grid(row=0, column=5)

    def _arrange_timestamp_grid(self):
        self.timestamp_date_label.grid(row=0, column=0)
        self.timestamp_time_label.grid(row=0, column=2)

        self.timestamp_date_text.grid(row=0, column=1)
        self.timestamp_time_text.grid(row=0, column=3)
