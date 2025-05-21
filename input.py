import RPi.GPIO as GPIO
import time

CLK = 23
DT = 22
BUTTON = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class DialInput:
    def __init__(self):
        self.last_clk = GPIO.input(CLK)
        self.last_button = GPIO.input(BUTTON)

    def get_input(self):
        result = None
        current_clk = GPIO.input(CLK)
        current_dt = GPIO.input(DT)
        current_button = GPIO.input(BUTTON)

        # Detect falling edge on CLK for rotation
        if self.last_clk == GPIO.HIGH and current_clk == GPIO.LOW:
            if current_dt == GPIO.HIGH:
                result = "down"
            else:
                result = "up"

        # Detect button press
        if current_button == GPIO.LOW and self.last_button == GPIO.HIGH:
            result = "press"
            time.sleep(0.2)  # debounce

        self.last_clk = current_clk
        self.last_button = current_button
        return result
