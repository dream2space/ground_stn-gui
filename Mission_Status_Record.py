import csv
import os

from tabulate import tabulate

import App_Parameters as app_params


class Mission_Status_Recorder():
    def __init__(self, mission_name, mission_datetime, mission_downlink_time):
        self.image_status_record = []
        self.mission_name = mission_name
        self.mission_start_time = mission_datetime
        self.mission_downlink_time = mission_downlink_time

        self.has_failure = False

        self.table_header = ['#', 'Downlink Status', 'Reed Solomon Decode Status', 'Unzip + Base64 Decode Status']

    def create_new_record(self, image_count):
        self.image_status_record.append(
            {'#': image_count, 'Downlink Status': "FAILED", 'Reed Solomon Decode Status': "FAILED",
             'Unzip + Base64 Decode Status': "FAILED"})

    def update_downlink_status(self, image_count, is_success):
        idx = image_count - 1
        if is_success:
            self.image_status_record[idx].update({'Downlink Status': "SUCCESS"})
        else:
            self.image_status_record[idx].update({'Downlink Status': "FAILED"})
            self.has_failure = True

    def update_rs_decode_status(self, image_count, is_success):
        idx = image_count - 1
        if is_success:
            self.image_status_record[idx].update({'Reed Solomon Decode Status': "SUCCESS"})
        else:
            self.image_status_record[idx].update({'Reed Solomon Decode Status': "FAILED"})
            self.has_failure = True

    def update_unzip_base64_decode_status(self, image_count, is_success):
        idx = image_count - 1
        if is_success:
            self.image_status_record[idx].update({'Unzip + Base64 Decode Status': "SUCCESS"})
        else:
            self.image_status_record[idx].update({'Unzip + Base64 Decode Status': "FAILED"})
            self.has_failure = True

    def create_mission_status_log(self):
        table_values = [list(x.values()) for x in self.image_status_record]

        # Create the log file
        with open(f"{app_params.GROUND_STN_MISSION_FOLDER_PATH}/{self.mission_name}/{self.mission_name}_status.txt", 'w') as status_log:
            to_print = ""

            status = [["Mission Name", self.mission_name],
                      ["Mission Start time", self.mission_start_time],
                      ["Mission Downlink time", self.mission_downlink_time]]
            to_print += tabulate(status, tablefmt="pretty")

            to_print += '\n'
            to_print += 'Mission Status:\n'
            to_print += tabulate(table_values, headers=self.table_header, tablefmt="pretty")
            status_log.write(to_print)
        status_log.close()

    def update_overall_mission_status_log(self, mission_name):
        header = "Mission Name,Mission Status"

        # Check overall status - success or failure
        outcome = ""
        if self.has_failure:
            outcome = "FAIL"
        else:
            outcome = "SUCCESS"

        # Create csv file if not already created
        if not os.path.exists(app_params.GROUND_STN_MISSION_LOG_FILEPATH):
            f = open(app_params.GROUND_STN_MISSION_LOG_FILEPATH, "w")
            f.write(header)
            f.close()

        # Append to csv
        with open(app_params.GROUND_STN_MISSION_LOG_FILEPATH, "a") as log:
            log.write(f"{mission_name},{outcome}")
        log.close()
