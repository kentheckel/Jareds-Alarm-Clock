from display import DisplayManager
from input import DialInput
from alarm import AlarmManager
from config import load_config

import time
from datetime import datetime

display = DisplayManager()
dial = DialInput()
alarms = AlarmManager()
config = load_config()

last_minute = None

try:
    while True:
        now = datetime.now()
        current_minute = now.strftime("%H:%M")

        # Update the clock only when the minute changes
        if current_minute != last_minute:
            last_minute = current_minute
            display.update_display(hour_format=config["hour_format"], alarms=alarms.get_alarms())

        # Check for dial input
        action = dial.get_input()
        if action:
            print("Action:", action)

        if action == "press":
            display.cycle_mode()
            display.update_display(hour_format=config["hour_format"], alarms=alarms.get_alarms())

        time.sleep(0.05)  # fast poll = smooth menu

except KeyboardInterrupt:
    print("Exiting.")
