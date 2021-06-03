import tkinter as tk

from Tk_Beacon_Panel import BeaconPanel
from Tk_Housekeeping_DataFrame import HousekeepingDataFrame
from Tk_Mission_Downlink_DataFrame import MissionDownlinkFrame


class MainPage(tk.Frame):
    def __init__(self, parent, controller, beacon_pipe, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller

        # Generate Beacon page for left
        self.beacon = BeaconPanel(self.parent, beacon_pipe)
        self.beacon.pack(side=tk.RIGHT, anchor=tk.NW, fill="both")

        # Create container to store all subsections
        self.command_panel_container = tk.Frame(self.parent)
        self.command_panel_container.pack(side=tk.LEFT, expand=1, fill="both", padx=10, pady=10)

        # Create section to request for housekeeping data
        self.housekeeping_command = HousekeepingDataFrame(
            self.command_panel_container, self.controller, tk.TOP, text="Housekeeping Command", padx=10, pady=8)

        # Create section for mission and downlink
        self.mission_command = MissionDownlinkFrame(
            self.command_panel_container, self.controller, tk.BOTTOM, text="Mission and Downlink Command", padx=10, pady=8)

    # ---------------------------------------------------------------
    # Housekeeping methods
    # ---------------------------------------------------------------
    def show_disable_command_after_hk_command(self):
        self.housekeeping_command.show_progress_bar()
        self.mission_command.disable_mission_command()

    def show_enable_command_after_hk_command(self):
        self.housekeeping_command.stop_showing_progress_bar()
        self.mission_command.stop_mission_block()

    def show_status_after_hk_command(self, is_success):
        if is_success:
            self.housekeeping_command.display_success_message()
        else:
            self.housekeeping_command.display_failed_message()

    # ---------------------------------------------------------------
    # Mission methods
    # ---------------------------------------------------------------
    def show_disable_command_after_mission_command(self):
        # Display success and show mission loading screen
        self.mission_command.display_add_success_msg()
        self.mission_command.show_progress_bar()
        self.mission_command.after(10000, self.mission_command.stop_mission_block)

        # Disable housekeeping data function
        self.housekeeping_command.disable_housekeeping_command()
        self.housekeeping_command.after(10000, self.housekeeping_command.stop_showing_progress_bar)

    def update_pending_mission_table(self, mission_list):
        self.mission_command.pending_mission_table.update_mission_entry(mission_list)

    def update_current_mission_table(self, mission_list):
        self.mission_command.current_mission_table.update_mission_entry(mission_list)
