def button_press(paused_event):
    pinSwitch = 3
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(pinSwitch, 0)

    while True:
        try:
            if wiringpi.digitalRead(pinSwitch) == 1:
                if paused_event.is_set():
                    paused_event.clear()
                    print("Timer hervat")
                else:
                    paused_event.set()
                    print("Timer gepauzeerd")
                time.sleep(0.3)
                while wiringpi.digitalRead(pinSwitch) == 1:
                    time.sleep(0.01)
            else:
                time.sleep(0.01)
        except KeyboardInterrupt:
            break
