from tabulate import tabulate


class Mission_Status_Recorder():
    def __init__(self):
        self.image_status_record = []

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
        pass
