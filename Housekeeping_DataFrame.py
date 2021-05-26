import tkinter as tk
import tkinter.ttk as ttk


class HousekeepingDataFrame(tk.LabelFrame):
    def __init__(self, parent, controller, pos, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=pos, anchor=tk.NW, expand=1, fill="both")

        # Add line for Housekeeping data
        self.label = tk.Label(
            self, text="Request for Housekeeping data", pady=8)
        self.label.pack()

        # Add button to trigger housekeeping data command
        self.start_hk_button = tk.Button(
            self, text="Click here", command=controller.handle_hk_process_start)
        self.start_hk_button.pack()

        # Progress bar
        self.pbar_container = tk.Frame(self, pady=4)
        self.pbar_container.pack()
        self.pbar = ttk.Progressbar(
            self.pbar_container, mode='indeterminate', length=100)

        # Outcome message
        self.outcome_message = tk.StringVar()
        self.outcome_message_label = tk.Label(
            self, textvariable=self.outcome_message)
        self.outcome_message_label.pack()

    def display_success_message(self):
        self.outcome_message.set("Success!")
        self.outcome_message_label["fg"] = 'green'

        # Display message
        self.outcome_message_label.pack(side=tk.BOTTOM)

        # Set task to clear the message
        self.after(10000, self.hk_outcome_message_clear)

    def display_failed_message(self):
        self.outcome_message.set("Failed!")
        self.outcome_message_label["fg"] = 'red'

        # Display message
        self.outcome_message_label.pack(side=tk.BOTTOM)

        # Set task to clear the message
        self.after(10000, self.hk_outcome_message_clear)

    def hk_outcome_message_clear(self):
        self.outcome_message.set("  ")
