from display import DisplayManager
from input import DialInput
from alarm import AlarmManager
from config import load_config

import time

display = DisplayManager()
dial = DialInput()
alarms = AlarmManager()
config = load_config()

menu_mode = False

try:
    while True:
        if not menu_mode:
            display.draw_clock(hour_format=config["hour_format"], alarms=alarms.get_alarms())
        time.sleep(0.5)

        action = dial.get_input()

        if action == "press":
            menu_mode = not menu_mode
            if menu_mode:
                display.draw_menu()
            else:
                display.draw_clock(hour_format=config["hour_format"], alarms=alarms.get_alarms())

        elif action in ["up", "down"] and menu_mode:
            display.update_menu_selection(action)

except KeyboardInterrupt:
    print("Exiting.")
