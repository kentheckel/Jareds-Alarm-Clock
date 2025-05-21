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

menu_mode = False
last_minute = None

try:
    while True:
        now = datetime.now()
        current_minute = now.strftime("%H:%M")

        # Update the clock only when the minute changes
        if not menu_mode and current_minute != last_minute:
            last_minute = current_minute
            display.update_clock(hour_format=config["hour_format"], alarms=alarms.get_alarms())

        # Check for dial input
        action = dial.get_input()
        if action:
            print("Action:", action)

        if action == "press":
            menu_mode = not menu_mode
            if menu_mode:
                display.draw_menu()
            else:
                # Reset selected index if you want to return to top each time:
                # display.selected_index = 0
                display.update_clock(hour_format=config["hour_format"], alarms=alarms.get_alarms())

        elif action in ["up", "down"] and menu_mode:
            display.update_menu_selection(action)

        time.sleep(0.05)  # faster polling for more responsive scrolling

except KeyboardInterrupt:
    print("Exiting.")
