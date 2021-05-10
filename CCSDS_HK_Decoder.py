from CCSDS_Parsed_Beacon import CCSDS_Parsed_Beacon
from CCSDS_Parsed_HK import CCSDS_Parsed_HK
import App_Parameters as app_params


class CCSDS_HK_Decoder:
    def __init__(self):
        pass

    def parse(self, packet):
        # # Shave off the header and telemetry packet type
        # header = packet[0:6]
        # telemetry_packet_type = packet[6]

        # Slice out packet data
        hk_payload = packet[7:]

        # Packet cannot be parsed correctly
        if len(hk_payload) != app_params.CCSDS_OBC_HK_DATAPOINT_LEN_BYTES * app_params.CCSDS_OBC_HK_DATAPOINTS_COUNT:
            return []

        # Extract out each hk datapoint
        list_hk_datapoints = []
        idx = 0
        # i is count to 20 since 20 dataset in packets
        for count in range(app_params.CCSDS_OBC_HK_DATAPOINTS_COUNT):
            slice = hk_payload[idx: idx +
                               app_params.CCSDS_OBC_HK_DATAPOINT_LEN_BYTES]
            idx = idx + app_params.CCSDS_OBC_HK_DATAPOINT_LEN_BYTES

            # Parse each hk datapoint
            parsed_hk = self._parse_each_hk(slice, count)
            list_hk_datapoints.append(parsed_hk)

        return list_hk_datapoints

    def _parse_each_hk(self, hk_slice, count):
        temp = int.from_bytes(
            hk_slice[0:3], byteorder='big', signed=True) / 100
        gx = int.from_bytes(hk_slice[3:5], byteorder='big', signed=True)
        gy = int.from_bytes(hk_slice[5:7], byteorder='big', signed=True)
        gz = int.from_bytes(hk_slice[7:], byteorder='big', signed=True)

        return CCSDS_Parsed_HK(temp, gx, gy, gz, count)
