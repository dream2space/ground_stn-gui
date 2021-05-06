from tkinter import *

root = Tk()
root.minsize(450, 80)

beacon_frame = LabelFrame(root, text="Beacon Data")
beacon_frame.pack(padx=10, pady=10)

# Create label
temperature_label = Label(beacon_frame, width=6, text="Temp",
                          borderwidth=1, relief="groove")
gx_label = Label(beacon_frame, width=6, text="GX",
                 borderwidth=1, relief="groove")
gy_label = Label(beacon_frame, width=6, text="GY",
                 borderwidth=1, relief="groove")
gz_label = Label(beacon_frame, width=6, text="GZ",
                 borderwidth=1, relief="groove")

# Display values
temp_text = Label(beacon_frame, width=6, text="ddddd",
                  bg="white", borderwidth=1, relief="groove")
gx_text = Label(beacon_frame, width=6, text="ddddd",
                bg="white", borderwidth=1, relief="groove")
gy_text = Label(beacon_frame, width=6, text="ddddd",
                bg="white", borderwidth=1, relief="groove")
gz_text = Label(beacon_frame, width=6, text="ddddd",
                bg="white", borderwidth=1, relief="groove")

# Put the labels in grids with row/col
temperature_label.grid(row=0, column=0)
gx_label.grid(row=0, column=2)
gy_label.grid(row=0, column=4)
gz_label.grid(row=0, column=6)

temp_text.grid(row=0, column=1)
gx_text.grid(row=0, column=3)
gy_text.grid(row=0, column=5)
gz_text.grid(row=0, column=7)

# Start running GUI
root.mainloop()
