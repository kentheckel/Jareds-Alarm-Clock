from datetime import datetime

class AlarmManager:
    def __init__(self):
        self.alarms = ["07:00", "08:30", ""]

    def get_alarms(self):
        return [alarm for alarm in self.alarms if alarm]
