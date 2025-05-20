import time
import wiringpi as wp

SWITCH_PIN = 8

wp.wiringPiSetup()
wp.pinMode(SWITCH_PIN, 0)

def switch_check():
    if(wp.digitalRead(SWITCH_PIN) == 0):
        return True
    else:
        return False
    