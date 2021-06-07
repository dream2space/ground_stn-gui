class CCSDS_Parsed_HK:
    def __init__(self, temp, adc, gx, gy, gz, count):
        self.temp = temp
        self.adc = adc
        self.gx = gx
        self.gy = gy
        self.gz = gz
        self.count = count

    def __str___(self):
        return f"HK#{self.count} | temp: {self.temp} | adc: {self.adc} | gx: {self.gx} | gy: {self.gy} | gz: {self.gz}"

    def get_list(self):

        def convert_adc_to_vbatt(adc):
            max_vbatt = 8.4
            max_adc = 1024
            return round(adc / max_adc * max_vbatt, 2)

        return {'temp': self.temp, 'gx': self.gx, 'gy': self.gy, 'gz': self.gz, 'vbatt': convert_adc_to_vbatt(self.adc)}
