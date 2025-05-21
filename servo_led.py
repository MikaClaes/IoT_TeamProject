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
