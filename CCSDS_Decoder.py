from CCSDS_Beacon_Decoder import CCSDS_Beacon_Decoder
from CCSDS_HK_Util import CCSDS_HK_Util


class CCSDS_Decoder():
    def __init__(self, isBeacon):
        if isBeacon:
            self.beacon_decoder = CCSDS_Beacon_Decoder()
        else:
            self.hk_decoder = CCSDS_HK_Util()

    def parse_beacon(self, beacon):
        return self.beacon_decoder.parse(beacon)

    def parse_housekeeping_data(self, packet):
        return self.hk_decoder.parse(packet)
