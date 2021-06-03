from CCSDS_Beacon_Decoder import CCSDS_Beacon_Decoder
from CCSDS_Downlink_Decoder import CCSDS_Downlink_Decoder
from CCSDS_HK_Util import CCSDS_HK_Util


class CCSDS_Decoder():
    def __init__(self, isBeacon, isHK):
        if isBeacon:
            self.beacon_decoder = CCSDS_Beacon_Decoder()
        elif isHK:
            self.hk_decoder = CCSDS_HK_Util()
        else:
            self.downlink_decoder = CCSDS_Downlink_Decoder()

    def parse_beacon(self, beacon):
        return self.beacon_decoder.parse(beacon)

    def parse_housekeeping_data(self, packet):
        return self.hk_decoder.parse(packet)

    def parse_downlink_packet(self, packet):
        return self.downlink_decoder.parse(packet)

    def quick_parse_downlink(self, packet):
        return self.downlink_decoder.quick_parse(packet)
