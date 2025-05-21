from datetime import datetime

class AlarmManager:
    def __init__(self):
        self.alarms = ["07:30", "08:00"]

    def get_current_time(self):
        return datetime.now()

    def get_active_alarms(self):
        return self.alarms
