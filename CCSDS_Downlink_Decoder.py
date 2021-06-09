from reedsolo import RSCodec

import Mission_Parameters as mission_params


class CCSDS_Downlink_Decoder():
    """CCSDS Class decodes CCSDS Control (Start/Stop) and Chunk packets"""

    def __init__(self):
        self.rsc = RSCodec(16)  # 16 ecc symbols

    # Takes in bytearray to parse
    def parse(self, CCSDS_Packet):

        # Parse header
        # header = self._parse_header(CCSDS_Packet)

        # Detect if it is Chunk or Stop
        packet_data = CCSDS_Packet[6:]
        telemetry_packet_type = packet_data[0]

        if telemetry_packet_type == mission_params.TELEMETRY_PACKET_TYPE_DOWNLINK_PACKET:
            return self._parse_chunk(packet_data)
        else:
            return self._parse_stop()

    def _parse_header(self, CCSDS_Packet):
        # Extract header
        header = CCSDS_Packet[:6]
        version_number = header[0] >> 5
        type_indicator = (header[0] >> 4) & 0b1
        secondary_header_flag = (header[0] >> 3) & 0b1
        application_id = ((header[0] & 0b11) << 11) | header[1]
        group_flags = header[2] >> 6
        source_seq_count = ((header[2] & 0b00111111) << 8) | header[3]
        packet_length = (header[4] << 8) | header[5]

        ret_header = {'Version Number': version_number, 'Type Indicator': type_indicator,
                      'Secondary Header Flag': secondary_header_flag, 'Application ID': application_id,
                      'Group Flags': group_flags, 'Source Sequence Count': source_seq_count,
                      'Packet length': packet_length}
        return ret_header

    def _parse_chunk(self, packet_data):
        image_payload = packet_data[7:]
        return self.rsc.decode(image_payload)[0]

    def _parse_stop(self):
        return b"stop"

    # Quickly parse and return batch and chunk number
    def quick_parse(self, CCSDS_Packet):
        telemetry_packet_type = CCSDS_Packet[6]

        if telemetry_packet_type == mission_params.TELEMETRY_PACKET_TYPE_DOWNLINK_STOP:
            return {"fail": False, "stop": True}

        elif telemetry_packet_type == mission_params.TELEMETRY_PACKET_TYPE_DOWNLINK_PACKET:
            # Extract batch and chunk number
            curr_batch = int.from_bytes(
                CCSDS_Packet[7:10], byteorder='big', signed=False)
            curr_chunk = int.from_bytes(
                CCSDS_Packet[10:13], byteorder='big', signed=False)
            return {"fail": False, "stop": False, "curr_batch": curr_batch, "curr_chunk": curr_chunk, "len": len(CCSDS_Packet)}

        elif telemetry_packet_type == mission_params.TELEMETRY_PACKET_TYPE_DOWNLINK_START:
            start_packet_data = CCSDS_Packet[:13]
            total_batch_expected = int.from_bytes(start_packet_data[10:], 'big')
            return {"fail": False, "stop":False, "start": True, "total_batch": total_batch_expected}

        else:
            return {"fail": True}
