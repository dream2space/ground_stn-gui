import App_Parameters as app_param
import tkinter as tk


class BeaconPanel(tk.Frame):
    def __init__(self, parent, pipe):
        tk.Frame.__init__(self, parent, width=app_param.APP_WIDTH/2,
                          height=app_param.APP_HEIGHT, padx=10, pady=10)
        self.parent = parent

        # Create a section/labelframe for beacon data
        self.beacon_pipe = pipe
        self.container = tk.Frame(self)
        self.container.pack()
        self.beacon_frame = BeaconFrame(
            self.container, text="Beacon Data", padx=10, pady=8)
        self.parent.after(1000, self.update_beacon_values)

    def update_beacon_values(self):
        if self.beacon_pipe.poll(timeout=0):
            ls = self.beacon_pipe.recv()
            temp = ls[0]
            gx = ls[1]
            gy = ls[2]
            gz = ls[3]
            self.beacon_frame.update_beacon_values(temp, gx, gy, gz)
        self.parent.after(1000, self.update_beacon_values)


class BeaconFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack()

        # Create variable to store beacon values
        self.temp = tk.StringVar()
        self.temp.set("0.00")
        self.gx = tk.StringVar()
        self.gx.set("0")
        self.gy = tk.StringVar()
        self.gy.set("0")
        self.gz = tk.StringVar()
        self.gz.set("0")

        # Create label for beacon data header
        self.temperature_label = self._create_header_label("Temp")
        self.gx_label = self._create_header_label("GX")
        self.gy_label = self._create_header_label("GY")
        self.gz_label = self._create_header_label("GZ")

        # Create label to store beacon data
        self.temp_text = self._create_text_label(self.temp)
        self.gx_text = self._create_text_label(self.gx)
        self.gy_text = self._create_text_label(self.gy)
        self.gz_text = self._create_text_label(self.gz)

        # Put the labels in grids with row/col
        self._arrange_grid()

    def update_beacon_values(self, temp, gx, gy, gz):
        def uncolor():
            self.temperature_label['bg'] = 'grey94'
            self.gx_label['bg'] = 'grey94'
            self.gy_label['bg'] = 'grey94'
            self.gz_label['bg'] = 'grey94'

        self.temp.set(temp)
        self.gx.set(gx)
        self.gy.set(gy)
        self.gz.set(gz)

        self.temperature_label['bg'] = 'yellow'
        self.gx_label['bg'] = 'yellow'
        self.gy_label['bg'] = 'yellow'
        self.gz_label['bg'] = 'yellow'
        self.parent.after(1200, uncolor)

    def _create_header_label(self, header_text):
        return tk.Label(self, width=6, text=header_text, borderwidth=1, relief="groove")

    def _create_text_label(self, text_container):
        return tk.Label(self, width=6, textvariable=text_container,
                        bg="white", borderwidth=1, relief="groove")

    def _arrange_grid(self):
        self.temperature_label.grid(row=0, column=0)
        self.gx_label.grid(row=0, column=2)
        self.gy_label.grid(row=0, column=4)
        self.gz_label.grid(row=0, column=6)

        self.temp_text.grid(row=0, column=1)
        self.gx_text.grid(row=0, column=3)
        self.gy_text.grid(row=0, column=5)
        self.gz_text.grid(row=0, column=7)
