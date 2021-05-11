from CCSDS_Parsed_HK import CCSDS_Parsed_HK
import App_Parameters as app_params
import CCSDS_Parameters as ccsds_params
from datetime import datetime
import csv


class CCSDS_HK_Util:
    def __init__(self):
        pass

    def parse(self, packet):
        # # Shave off the header and telemetry packet type
        # header = packet[0:6]
        # telemetry_packet_type = packet[6]

        # Slice out packet data
        hk_payload = packet[7:]

        # Packet cannot be parsed correctly
        if len(hk_payload) != ccsds_params.CCSDS_OBC_HK_DATAPOINT_LEN_BYTES * ccsds_params.CCSDS_OBC_HK_DATAPOINT_COUNT:
            return []

        # Extract out each hk datapoint
        list_hk_datapoints = []
        idx = 0
        # i is count to 20 since 20 dataset in packets
        for count in range(ccsds_params.CCSDS_OBC_HK_DATAPOINT_COUNT):
            slice = hk_payload[idx: idx +
                               ccsds_params.CCSDS_OBC_HK_DATAPOINT_LEN_BYTES]
            idx = idx + ccsds_params.CCSDS_OBC_HK_DATAPOINT_LEN_BYTES

            # Parse each hk datapoint
            parsed_hk = self._parse_each_hk(slice, count)
            list_hk_datapoints.append(parsed_hk)

        return list_hk_datapoints

    def log(self, list_hk_obj):
        # Prepare filename
        file_name = app_params.HOUSEKEEPING_DATA_FILE_PREFIX
        file_name += datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

        # Prepare header of CSV file
        header = ["temp", "gx", "gy", "gz"]

        # Open CSV file
        with open(f'{app_params.HOUSEKEEPING_DATA_FOLDER_FILEPATH}/{file_name}.csv', mode='a', newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            for d in list_hk_obj:
                writer.writerow(d.get_list())

    def _parse_each_hk(self, hk_slice, count):
        temp = int.from_bytes(
            hk_slice[0:3], byteorder='big', signed=True) / 100
        gx = int.from_bytes(hk_slice[3:5], byteorder='big', signed=True)
        gy = int.from_bytes(hk_slice[5:7], byteorder='big', signed=True)
        gz = int.from_bytes(hk_slice[7:], byteorder='big', signed=True)

        return CCSDS_Parsed_HK(temp, gx, gy, gz, count)
