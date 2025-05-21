import RPi.GPIO as GPIO
import time

# Corrected pin setup (adjust if needed)
CLK = 22      # Rotary encoder pin A
DT = 23       # Rotary encoder pin B
BUTTON = 27   # Encoder push button

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_clk = GPIO.input(CLK)
last_button = GPIO.input(BUTTON)
debounce_time = 0.05
last_turn_time = time.time()

print("Spin or press the dial... (CTRL+C to quit)")

try:
    while True:
        current_clk = GPIO.input(CLK)
        current_dt = GPIO.input(DT)
        current_time = time.time()

        # Detect rotation
        if current_clk == GPIO.LOW and current_time - last_turn_time > 0.1:
            last_turn_time = current_time
            if current_dt != current_clk:
                print("Rotated clockwise")
            else:
                print("Rotated counterclockwise")
        last_clk = current_clk

        # Detect button press (with debounce)
        if GPIO.input(BUTTON) == GPIO.LOW and last_button == GPIO.HIGH:
            print("Button pressed!")
            time.sleep(0.2)  # debounce
        last_button = GPIO.input(BUTTON)

        time.sleep(0.005)

except KeyboardInterrupt:
    print("Exiting.")
finally:
    GPIO.cleanup()
