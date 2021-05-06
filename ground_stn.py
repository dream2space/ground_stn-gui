import tkinter as tk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.minsize(450, 80)

        # Create a section/labelframe for beacon data
        self.beacon_frame = tk.LabelFrame(root, text="Beacon Data")
        self.beacon_frame.pack(padx=10, pady=10)

        # Create label for beacon data header
        self.temperature_label = tk.Label(
            self.beacon_frame, width=6, text="Temp", borderwidth=1, relief="groove")
        self.gx_label = tk.Label(
            self.beacon_frame, width=6, text="GX", borderwidth=1, relief="groove")
        self.gy_label = tk.Label(
            self.beacon_frame, width=6, text="GY", borderwidth=1, relief="groove")
        self.gz_label = tk.Label(
            self.beacon_frame, width=6, text="GZ", borderwidth=1, relief="groove")

        # Create label to store beacon data
        self.temp_text = tk.Label(
            self.beacon_frame, width=6, text="ddddd", bg="white", borderwidth=1, relief="groove")
        self.gx_text = tk.Label(self.beacon_frame, width=6, text="ddddd",
                                bg="white", borderwidth=1, relief="groove")
        self.gy_text = tk.Label(self.beacon_frame, width=6, text="ddddd",
                                bg="white", borderwidth=1, relief="groove")
        self.gz_text = tk.Label(self.beacon_frame, width=6, text="ddddd",
                                bg="white", borderwidth=1, relief="groove")

        # Put the labels in grids with row/col
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
