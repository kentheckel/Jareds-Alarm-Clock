import RPi.GPIO as GPIO
import time

# Rotary encoder GPIO pins
CLK = 23      # Rotary encoder pin A
DT = 22       # Rotary encoder pin B
BUTTON = 27   # Rotary encoder push button

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_clk = GPIO.input(CLK)
last_button = GPIO.input(BUTTON)
last_turn_time = time.time()

print("Spin or press the dial... (CTRL+C to quit)")

try:
    while True:
        current_clk = GPIO.input(CLK)
        current_dt = GPIO.input(DT)
        current_time = time.time()

        # Detect falling edge on CLK
        if last_clk == GPIO.HIGH and current_clk == GPIO.LOW:
            if current_dt == GPIO.HIGH:
                print("Rotated clockwise")
            else:
                print("Rotated counterclockwise")
            last_turn_time = current_time

        last_clk = current_clk

        # Detect button press (with debounce)
        if GPIO.input(BUTTON) == GPIO.LOW and last_button == GPIO.HIGH:
            print("Button pressed!")
            time.sleep(0.2)
        last_button = GPIO.input(BUTTON)

        time.sleep(0.005)

except KeyboardInterrupt:
    print("Exiting.")
finally:
    GPIO.cleanup()
