import CCSDS_Parameters as ccsds_params


class CCSDS_Encoder():
    def __init__(self):
        self.packet_count = 0

    def generate_HK_telecommand(self, telecommand_type, timestamp_query_start, timestamp_query_end):
        packet_field = bytearray(0)

        # Create the other fields in packet first
        packet_field = packet_field + telecommand_type.to_bytes(1, 'big')
        packet_field = packet_field + \
            self._process_timestamp(timestamp_query_start)
        packet_field = packet_field + \
            self._process_timestamp(timestamp_query_end)

        # Create header
        header = self._generate_packet_header(len(packet_field))

        # Return appended packet
        return self._pad(header + packet_field)

    def generate_mission_telecommand(
            self, telecommand_type, timestamp_start_mission, num_images, interval, timestamp_start_downlink):
        packet_field = bytearray(0)

        # Create the other fields in packet first
        packet_field = packet_field + telecommand_type.to_bytes(1, 'big')

        # Mission related
        packet_field = packet_field + self._process_timestamp(timestamp_start_mission)
        packet_field = packet_field + num_images.to_bytes(1, 'big')
        packet_field = packet_field + interval.to_bytes(2, 'big')
        packet_field = packet_field + self._process_timestamp(timestamp_start_downlink)

        # Create header
        header = self._generate_packet_header(len(packet_field))

        # Return appended packet
        return self._pad(header + packet_field)

    def _pad(self, packet):
        """Pad with fake header"""
        while len(packet) < ccsds_params.TELECOMMAND_PACKET_LEN_BYTES:
            packet = packet + b'B'

        # Add fake header
        packet = b'A' + packet
        return packet

    def _generate_packet_header(self, length):
        # Abstract header as 6 bytes
        header = bytearray(0)  # octet 1, 2, ..., 6

        octet = 0b0

        # Version number
        octet = octet << 3 | 0b000

        # # Packet identification
        # # @Type indicator -- Set to 0 to indicate telemetry packet
        octet = octet << 1 | 0b0

        # # @Packet Secondary Header Flag -- Set to 0 to indicate that secondary header not present
        octet = octet << 1 | 0b0

        # # @Application Process ID
        # # Defines the process onboard that is sending the packet --> TBC
        octet = octet << 11 | 0b10

        header = header + octet.to_bytes(2, 'big')

        octet = 0b0

        # # Packet Sequence Control
        # # @Grouping packets -- No grouping so set to 0
        octet = octet << 2 | 0b11

        # # @Source Sequence Count
        # # Sequence number of packet modulo 16384
        octet = octet << 14 | self.packet_count
        self.packet_count += 1

        header = header + octet.to_bytes(2, 'big')

        octet = 0b0

        # # Packet Data Length
        # In terms of octets
        # Total number of octets in packet data field - 1
        octet = octet << 16 | (length - 1)

        header = header + octet.to_bytes(2, 'big')

        return header

    def _process_timestamp(self, timestamp):
        ret = bytearray(0)
        ts_list = [int(s) for s in timestamp.split('-')]

        # DD
        ret = ret + ts_list[0].to_bytes(1, 'big')

        # MM
        ret = ret + ts_list[1].to_bytes(1, 'big')

        # YYYY
        ret = ret + ts_list[2].to_bytes(2, 'big')

        # hh
        ret = ret + ts_list[3].to_bytes(1, 'big')

        # mm
        ret = ret + ts_list[4].to_bytes(1, 'big')

        # ss
        ret = ret + ts_list[5].to_bytes(1, 'big')

        return ret
