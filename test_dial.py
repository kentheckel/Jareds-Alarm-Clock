import RPi.GPIO as GPIO
import time

# BCM pin numbers
CLK = 22      # Rotary encoder pin A
DT = 23       # Rotary encoder pin B
BUTTON = 27   # Encoder push button

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_clk = GPIO.input(CLK)

print("Rotate the dial or press the button... (CTRL+C to quit)")

try:
    while True:
        clk_state = GPIO.input(CLK)
        dt_state = GPIO.input(DT)

        if clk_state != last_clk:
            if dt_state != clk_state:
                print("Rotated clockwise")
            else:
                print("Rotated counterclockwise")
            last_clk = clk_state
            time.sleep(0.05)  # debounce rotation

        if GPIO.input(BUTTON) == GPIO.LOW:
            print("Button pressed!")
            time.sleep(0.2)  # debounce press

except KeyboardInterrupt:
    print("Exiting test.")
finally:
    GPIO.cleanup()
