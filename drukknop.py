import wiringpi
import time

def button_press():
    # SETUP

    pinSwitch = 3 # Button on pin 8
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(pinSwitch, 0)  # Set pinSwitch as INPUT

    # Initialize variables
    press_count = 0
    is_odd = False

    while True:
        try:
            if wiringpi.digitalRead(pinSwitch) == 1:  # Button pressed
                press_count += 1
                is_odd = (press_count % 2 == 1)  # True if odd, False if even
                print(f"Button pressed {press_count} times. is_odd: {is_odd}")
                time.sleep(0.3)  # Debounce delay
                while wiringpi.digitalRead(pinSwitch) == 1:  # Wait for button release
                    time.sleep(0.01)
            else:
                time.sleep(0.01)  # Small delay to reduce CPU usage
        except KeyboardInterrupt:
            break