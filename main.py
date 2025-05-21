from display import DisplayManager
from input import DialInput
from alarm import AlarmManager

display = DisplayManager()
dial = DialInput()
alarms = AlarmManager()

def main():
    while True:
        now = alarms.get_current_time()
        current_alarms = alarms.get_active_alarms()

        display.update_time(now)
        display.update_alarms(current_alarms)

        action = dial.check_input()
        if action == "MENU":
            display.show_menu()
            selected = dial.navigate_menu(["Alarms", "Sounds", "WiFi", "Brightness"])
            display.handle_menu_selection(selected, dial, alarms)

if __name__ == "__main__":
    main()
