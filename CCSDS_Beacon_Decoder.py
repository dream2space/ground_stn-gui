from CCSDS_Parsed_Beacon import CCSDS_Parsed_Beacon


class CCSDS_Beacon_Decoder:
    def __init__(self):
        pass

    def parse(self, packet):
        # header = packet[0:6]
        # telemetry_packet_type = packet[6]

        ttnc_field = packet[7:9]
        ret_ttnc = self._parse_ttnc_field(ttnc_field)

        adcs_field = packet[9:21]
        ret_adcs = self._parse_adcs_field(adcs_field)

        eps_field = packet[21:27]
        ret_eps = self._parse_eps_field(eps_field)

        payload_field = packet[27:31]
        ret_payload = self._parse_payload_field(payload_field)

        timestamp_field = packet[31:]
        ret_timestamp = self._parse_timestamp_field(timestamp_field)

        return CCSDS_Parsed_Beacon(ret_ttnc, ret_adcs, ret_eps, ret_payload, ret_timestamp)

    def _parse_ttnc_field(self, ttnc_field):
        # Decode mode
        mode_lookup = {0: 'FU1', 1: 'FU2', 2: 'FU3', 3: 'FU4'}
        mode_bits = (ttnc_field[0] & 0b01100000) >> 5
        mode = mode_lookup.get(mode_bits)

        # Decode baud
        baud_lookup = {0: '1200', 1: '2400', 2: '4800', 3: '9600',
                       4: '19200', 5: '38400', 6: '57600', 7: '115200'}
        baud_bits = (ttnc_field[0] & 0b00011100) >> 2
        baud = baud_lookup.get(baud_bits)

        # Channel
        channel_bits = ((ttnc_field[0] & 0b00000011)
                        << 5) | (ttnc_field[1] >> 3)
        channel = str(int(f'{channel_bits:#0}'))

        # Transmit Power
        tx_power_lookup = {0: '-1', 1: '2', 2: '5',
                           3: '8', 4: '11', 5: '14', 6: '17', 7: '20'}
        tx_power_bits = (ttnc_field[1] & 0b111)
        tx_power = tx_power_lookup.get(tx_power_bits)

        ret_ttnc = {'Transmission Mode': mode, 'Baud Rate': baud,
                    'Channel': channel, 'Transmit Power': tx_power}
        return ret_ttnc

    def _parse_adcs_field(self, adcs_field):
        # Decode gx
        gx = int.from_bytes(adcs_field[0:2], byteorder='big', signed=True)

        # Decode gy
        gy = int.from_bytes(adcs_field[2:4], byteorder='big', signed=True)

        # Decode gz
        gz = int.from_bytes(adcs_field[4:6], byteorder='big', signed=True)

        # Decode mx
        ax = int.from_bytes(adcs_field[6:8], byteorder='big', signed=True)

        # Decode my
        ay = int.from_bytes(adcs_field[8:10], byteorder='big', signed=True)

        # Decode mz
        az = int.from_bytes(
            adcs_field[10:12], byteorder='big', signed=True)

        ret_adcs = {'gx': gx, 'gy': gy, 'gz': gz,
                    'ax': ax, 'ay': ay, 'az': az}
        return ret_adcs

    def _parse_eps_field(self, eps_field):
        temp_int = int.from_bytes(
            eps_field[0:3], byteorder='big', signed=True)
        temp = temp_int / 100
        adc_value = int.from_bytes(
            eps_field[3:5], byteorder='big', signed=True)

        return {'Temperature': temp, 'adc': adc_value}

    def _parse_payload_field(self, payload_field):
        r1 = payload_field[0]
        r2 = payload_field[1]
        r3 = payload_field[2]
        r4 = payload_field[3]

        ret_payload = {'Reserved byte 1': r1, 'Reserved byte 2': r2,
                       'Reserved byte 3': r3, 'Reserved byte 4': r4}
        return ret_payload

    def _parse_timestamp_field(self, timestamp_field):
        decoded_string = timestamp_field.decode('utf-8')

        timestamp_dd = decoded_string[0:2]
        timestamp_MM = decoded_string[2:4]
        timestamp_yy = decoded_string[4:6]

        timestamp_hh = decoded_string[6:8]
        timestamp_mm = decoded_string[8:10]
        timestamp_ss = decoded_string[10:12]

        date = f"{timestamp_dd}/{timestamp_MM}/{timestamp_yy}"
        time = f"{timestamp_hh}:{timestamp_mm}:{timestamp_ss}"

        ret_timestamp = {"date": date, "time": time}
        return ret_timestamp
