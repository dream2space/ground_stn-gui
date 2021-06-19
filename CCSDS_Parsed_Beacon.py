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
        list_gyro = self.get_rotation(ret_adcs['gx'], ret_adcs['gy'], ret_adcs['gz'])
        list_accel = self.get_accel(ret_adcs['ax'], ret_adcs['ay'], ret_adcs['az'])
        self.gx = list_gyro[0]
        self.gy = list_gyro[1]
        self.gz = list_gyro[2]
        self.ax = list_accel[0]
        self.ay = list_accel[1]
        self.az = list_accel[2]

        # Unpack eps
        self.temp = ret_eps['Temperature']
        self.adc = ret_eps['adc']

        # Unpack payload
        self.r1 = ret_payload['Reserved byte 1']
        self.r2 = ret_payload['Reserved byte 2']
        self.r3 = ret_payload['Reserved byte 3']
        self.r4 = ret_payload['Reserved byte 4']

        # Unpack timestamp
        self.ts_date = ret_timestamp['date']
        self.ts_time = ret_timestamp['time']

    def __str__(self):
        ret = ""
        for field, field_dict in self.ret.items():
            ret += f"---- {field} ----"
            ret += "\n".join("{:<30} {}".format(k, v)
                             for k, v in field_dict.items())
        return ret

    def get_temp(self):
        return self.temp

    def get_adcs_data(self):
        return {'gx': self.gx, 'gy': self.gy, 'gz': self.gz, 'ax': self.ax, 'ay': self.ay, 'az': self.az}

    def get_vbatt(self):
        '''
        Process and convert ADC value to vbatt
        '''

        def convert_adc_to_vbatt(adc):
            max_vbatt = 8.4
            max_adc = 1024
            return adc / max_adc * max_vbatt

        return convert_adc_to_vbatt(self.adc)

    def get_accel(self, raw_x, raw_y, raw_z):
        '''
        Process and convert raw accelerometer value to converted value
        '''

        def convert_raw_accel(raw_acc):
            max_int = 32768  # 16 bit signed integer data bits
            g2 = 2 * 9.8
            return raw_acc / max_int * g2

        return [convert_raw_accel(raw_x), convert_raw_accel(raw_y), convert_raw_accel(raw_z)]

    def get_rotation(self, raw_x, raw_y, raw_z):
        '''
        Process and convert raw gyroscope value to converted value
        '''

        def convert_raw_gyro(raw_g):
            max_int = 32768  # 16 bit signed integer data bits
            rotation_per_sec = 250
            return raw_g/max_int * rotation_per_sec

        return [convert_raw_gyro(raw_x), convert_raw_gyro(raw_y), convert_raw_gyro(raw_z)]

    def get_timestamp_date(self):
        return self.ts_date

    def get_timestamp_time(self):
        return self.ts_time
