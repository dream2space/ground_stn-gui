import tkinter as tk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.minsize(450, 80)
        self.parent.title("Ground Station")

        # Create a section/labelframe for beacon data
        self.beacon_frame = BeaconFrame(self.parent, text="Beacon Data")


class BeaconFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(padx=10, pady=10)

        # Create label for beacon data header
        self.temperature_label = self._create_header_label("Temp")
        self.gx_label = self._create_header_label("GX")
        self.gy_label = self._create_header_label("GY")
        self.gz_label = self._create_header_label("GZ")

        # Create label to store beacon data
        self.temp_text = self._create_text_label("37.60")
        self.gx_text = self._create_text_label("-5")
        self.gy_text = self._create_text_label("8")
        self.gz_text = self._create_text_label("3")

        # Put the labels in grids with row/col
        self._arrange_grid()

    def _create_header_label(self, header_text):
        return tk.Label(self, width=6, text=header_text, borderwidth=1, relief="groove")

    def _create_text_label(self, value_text):
        return tk.Label(self, width=6, text=value_text,
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


# Start running GUI
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
