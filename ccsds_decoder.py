from CCSDS_Beacon_Decoder import CCSDS_Beacon_Decoder


class CCSDS_Decoder():
    def __init__(self):
        self.beacon_decoder = CCSDS_Beacon_Decoder()

    def parse_beacon(self, beacon):
        return self.beacon_decoder.parse(beacon)
