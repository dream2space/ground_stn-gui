from tkinter import *

root = Tk()

# Create label
mylabel1 = Label(root, text="Hello world!")
mylabel2 = Label(root, text="Bye!")

# Put the labels in grids with row/col
mylabel1.grid(row=0, column=0)
mylabel2.grid(row=1, column=1)

# Start running GUI
root.mainloop()
