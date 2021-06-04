class CCSDS_Parsed_Beacon:
    def __init__(self, ret_ttnc, ret_adcs, ret_eps, ret_payload, ret_timestamp):
        self.ret = {'TT&C': ret_ttnc, 'ADCS': ret_adcs, 'EPS': ret_eps,
                    'Payload': ret_payload, 'Timestamp': ret_timestamp}

        # Unpack ttnc
        self.mode = ret_ttnc['Transmission Mode']
        self.baud = ret_ttnc['Baud Rate']
        self.channel = ret_ttnc['Channel']
        self.tx_power = ret_ttnc['Transmit Power']

        # Unpack adcs
        self.gx = ret_adcs['gx']
        self.gy = ret_adcs['gy']
        self.gz = ret_adcs['gz']
        self.mx = ret_adcs['mx']
        self.my = ret_adcs['my']
        self.mz = ret_adcs['mz']

        # Unpack eps
        self.temp = ret_eps['Temperature']
        self.adc = ret_eps['adc']

        # Unpack payload
        self.r1 = ret_payload['Reserved byte 1']
        self.r2 = ret_payload['Reserved byte 2']
        self.r3 = ret_payload['Reserved byte 3']
        self.r4 = ret_payload['Reserved byte 4']

        # Unpack timestamp
        self.ts_DD = ret_timestamp['DD']
        self.ts_MM = ret_timestamp['MM']
        self.ts_YYYY = ret_timestamp['YYYY']
        self.ts_hh = ret_timestamp['hh']
        self.ts_mm = ret_timestamp['mm']
        self.ts_ss = ret_timestamp['ss']

    def __str__(self):
        ret = ""
        for field, field_dict in self.ret.items():
            ret += f"---- {field} ----"
            ret += "\n".join("{:<30} {}".format(k, v)
                             for k, v in field_dict.items())
        return ret

    def get_temp(self):
        return self.temp

    def get_gyro(self):
        return {'gx': self.gx, 'gy': self.gy, 'gz': self.gz}
