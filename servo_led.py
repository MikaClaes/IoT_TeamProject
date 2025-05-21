import wiringpi
import time

# Initialize WiringPi
wiringpi.wiringPiSetup()  # Use WiringPi pin numbering

# Pin definitions
SERVO_PIN = 2  # Adjust to your WiringPi pin (e.g., 0 for GPIO17)
LED_RED_PIN =5  # Adjust to your WiringPi pin for red LED
LED_GREEN_PIN = 7  # Adjust to your WiringPi pin for green LED
LED_BLUE_PIN = 8 # Adjust to your WiringPi pin for blue LED (unused)

# Set pins as output
wiringpi.pinMode(SERVO_PIN, 1)  # 1 = OUTPUT
wiringpi.pinMode(LED_RED_PIN, 1)
wiringpi.pinMode(LED_GREEN_PIN, 1)
wiringpi.pinMode(LED_BLUE_PIN, 1)

# PWM settings for 50Hz (20ms period)
PWM_FREQ = 50
PWM_PERIOD = 1000 / PWM_FREQ  # 20ms

def set_servo_angle(angle):
    """Set servo angle with PWM pulse width between 0.5ms and 2.5ms."""
    if not 0 <= angle <= 180:
        raise ValueError("Angle must be between 0 and 180 degrees")
    pulse_width = 0.5 + (angle / 180.0) * (2.5 - 0.5)  # 0.5ms to 2.5ms
    for _ in range(20):  # Send pulses for ~0.4s
        wiringpi.digitalWrite(SERVO_PIN, 1)
        time.sleep(pulse_width / 1000.0)  # Pulse high
        wiringpi.digitalWrite(SERVO_PIN, 0)
        time.sleep((PWM_PERIOD - pulse_width) / 1000.0)  # Pulse low

def blink_led(pin, times=3, duration=0.5):
    """Blink the specified LED pin a number of times."""
    for _ in range(times):
        wiringpi.digitalWrite(pin, 1)
        time.sleep(duration)
        wiringpi.digitalWrite(pin, 0)
        time.sleep(duration)

def pomodoro_timer(paused_event):
    WORK_TIME = 10
    SHORT_BREAK = 5
    LONG_BREAK = 20
    CYCLES = 4

    try:
        cycle_count = 0
        while True:
            for _ in range(CYCLES):
                print("Work session: 25 minutes")
                set_servo_angle(0)
                blink_led(LED_RED_PIN, 3)
                wiringpi.digitalWrite(LED_RED_PIN, 1)

                countdown(WORK_TIME, paused_event)

                wiringpi.digitalWrite(LED_RED_PIN, 0)

                print("Short break: 5 minutes")
                set_servo_angle(180)
                blink_led(LED_GREEN_PIN, 3)
                wiringpi.digitalWrite(LED_GREEN_PIN, 1)

                countdown(SHORT_BREAK, paused_event)

                wiringpi.digitalWrite(LED_GREEN_PIN, 0)
                cycle_count += 1

            print("Long break: 15 minutes")
            set_servo_angle(180)
            blink_led(LED_BLUE_PIN, 3)
            wiringpi.digitalWrite(LED_BLUE_PIN, 1)

            countdown(LONG_BREAK, paused_event)

            wiringpi.digitalWrite(LED_BLUE_PIN, 0)
            cycle_count = 0

    except KeyboardInterrupt:
        print("Pomodoro gestopt")
    finally:
        wiringpi.digitalWrite(SERVO_PIN, 0)
        wiringpi.digitalWrite(LED_RED_PIN, 0)
        wiringpi.digitalWrite(LED_GREEN_PIN, 0)
        wiringpi.digitalWrite(LED_BLUE_PIN, 0)

def countdown(duration, paused_event):
    remaining = duration
    while remaining > 0:
        if paused_event.is_set():
            print("Timer gepauzeerd")
            wiringpi.digitalWrite(LED_RED_PIN, 0)
            wiringpi.digitalWrite(LED_GREEN_PIN, 0)
            wiringpi.digitalWrite(LED_BLUE_PIN, 1)  # Blauwe LED aan
            while paused_event.is_set():
                time.sleep(0.1)
            wiringpi.digitalWrite(LED_BLUE_PIN, 0)  # Blauwe LED uit
            print("Timer hervat")
        time.sleep(1)
        remaining -= 1
