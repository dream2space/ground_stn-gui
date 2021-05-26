import datetime


class Mission:
    def __init__(self, mission_date, downlink_date, mission_time, downlink_time, image_count, interval):
        self._parse(mission_date, downlink_date, mission_time, downlink_time, image_count, interval)

    def __str__(self):
        _1 = f"mission date: {self.mission_datetime.strftime('%d/%m/%Y')} | mission time: {self.mission_datetime.strftime('%H:%M:%S')}\n"
        _2 = f"downlink date: {self.downlink_datetime.strftime('%d/%m/%Y')} | downlink time: {self.downlink_datetime.strftime('%H:%M:%S')}\n"
        _3 = f"image count: {self.image_count} | image interval: {self.interval}"
        return _1 + _2 + _3

    def __repr__(self) -> str:
        _1 = f"\nmission date: {self.mission_datetime.strftime('%d/%m/%Y')} | mission time: {self.mission_datetime.strftime('%H:%M:%S')}\n"
        _2 = f"downlink date: {self.downlink_datetime.strftime('%d/%m/%Y')} | downlink time: {self.downlink_datetime.strftime('%H:%M:%S')}\n"
        _3 = f"image count: {self.image_count} | image interval: {self.interval}\n"
        return _1 + _2 + _3

    def _parse(self, mission_date, downlink_date, mission_time, downlink_time, image_count, interval):

        # date format: yyyy/MM/dd
        def _parse_date(date):
            date_split = date.split('-')
            return date_split

        # time format: hh mm ss
        def _parse_time(time):
            time_split = time.split(' ')
            return time_split

        try:
            parsed_mission_date = _parse_date(mission_date)
            parsed_mission_time = _parse_time(mission_time)
            mission_date_yyyy = int(parsed_mission_date[0])
            mission_date_MM = int(parsed_mission_date[1])
            mission_date_dd = int(parsed_mission_date[2])
            mission_time_hh = int(parsed_mission_time[0])
            mission_time_mm = int(parsed_mission_time[1])
            mission_time_ss = int(parsed_mission_time[2])
            self.mission_datetime = datetime.datetime(
                year=mission_date_yyyy, month=mission_date_MM, day=mission_date_dd, hour=mission_time_hh,
                minute=mission_time_mm, second=mission_time_ss)

            parsed_downlink_date = _parse_date(downlink_date)
            parsed_downlink_time = _parse_time(downlink_time)
            downlink_date_yyyy = int(parsed_downlink_date[0])
            downlink_date_MM = int(parsed_downlink_date[1])
            downlink_date_dd = int(parsed_downlink_date[2])
            downlink_time_hh = int(parsed_downlink_time[0])
            downlink_time_mm = int(parsed_downlink_time[1])
            downlink_time_ss = int(parsed_downlink_time[2])
            self.downlink_datetime = datetime.datetime(
                year=downlink_date_yyyy, month=downlink_date_MM, day=downlink_date_dd, hour=downlink_time_hh,
                minute=downlink_time_mm, second=downlink_time_ss)

            self.image_count = int(image_count)
            self.interval = int(interval)

        except ValueError:
            # blanks found in datetime fields -> put dummy values
            self.image_count = int(image_count)
            self.interval = int(interval)

            self.mission_datetime = datetime.datetime.now()
            self.downlink_datetime = datetime.datetime.now()

    def get_mission_datetime_string(self):
        return self.mission_datetime.strftime("%d-%b-%Y %H:%M:%S")

    def get_downlink_datetime_string(self):
        return self.downlink_datetime.strftime("%d-%b-%Y %H:%M:%S")
