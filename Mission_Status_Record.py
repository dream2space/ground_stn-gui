import os

from tabulate import tabulate

import App_Parameters as app_params


class Mission_Status_Recorder():
    def __init__(self, mission_name, mission_datetime, mission_downlink_time):
        self.image_status_record = []
        self.mission_name = mission_name
        self.mission_start_time = mission_datetime
        self.mission_downlink_time = mission_downlink_time

        self.table_header = ['#', 'Downlink Status', 'Reed Solomon Decode Status', 'Unzip + Base64 Decode Status']

    def create_new_record(self, image_count):
        self.image_status_record.append({'#': image_count, 'Downlink Status': False,
                                         'Reed Solomon Decode Status': False, 'Unzip + Base64 Decode Status': False})

    def update_downlink_status(self, image_count, is_success):
        idx = image_count - 1
        self.image_status_record[idx].update({'Downlink Status': is_success})

    def update_rs_decode_status(self, image_count, is_success):
        idx = image_count - 1
        self.image_status_record[idx].update({'Reed Solomon Decode Status': is_success})

    def update_unzip_base64_decode_status(self, image_count, is_success):
        idx = image_count - 1
        self.image_status_record[idx].update({'Unzip + Base64 Decode Status': is_success})

    def create_mission_status_log(self):
        table_values = [list(x.values()) for x in self.image_status_record]

        # Create the log file
        with open(f"{app_params.GROUND_STN_MISSION_FOLDER_PATH}/{self.mission_name}", 'w') as status_log:
            to_print = f"Mission Name: {self.mission_name}\n"
            to_print += f"Mission Start time: {self.mission_start_time}\n"
            to_print += f"Mission Downlink time: {self.mission_downlink_time}\n"
            to_print += '\n'
            to_print += 'Mission Status:\n'
            to_print += tabulate(table_values, headers=self.table_header, tablefmt="pretty")
            status_log.write(to_print)
        status_log.close()
