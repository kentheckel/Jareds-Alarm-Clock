import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  # adjust as needed

class DialInput:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def check_input(self):
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            time.sleep(0.3)
            return "MENU"
        return None

    def navigate_menu(self, items):
        # placeholder: simulate selecting first item
        return items[0]
