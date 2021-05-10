class CCSDS_Parsed_HK:
    def __init__(self, temp, gx, gy, gz, count):
        self.temp = temp
        self.gx = gx
        self.gy = gy
        self.gz = gz
        self.count = count

    def __str___(self):
        return f"HK#{self.count} | temp: {self.temp} | gx: {self.gx} | gy: {self.gy} | gz: {self.gz}"
