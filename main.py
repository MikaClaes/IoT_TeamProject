import threading
from servo_led import pomodoro_timer
from voice_ai import speech_recognition
from mqtt import get_last_thingspeak_entry
from display import ChangeDisplay
from drukknop import button_press
import time

#Functions
def timer_thread():
    print("Starting Pomodoro timer with servo and RGB LED indication")
    print("Servo angles: Work (0°), Short Break (180°), Long Break (180°)")
    print("LED: Red (blink 3x then solid for work), Green (blink 3x then solid for short break), Blue (blink 3x then solid for long break)")
    pomodoro_timer()


def voice_ai_thread():
    speech_recognition()
    

def display_thread():
    while True:
        current_lux, current_temp = get_last_thingspeak_entry()
        ChangeDisplay(float(current_lux), float(current_temp))
        
#Variabelen
current_temp = 0
current_lux = 0

# Multithread setup with separate threads for each function
timer = threading.Thread(target=timer_thread)
ai = threading.Thread(target=voice_ai_thread)
display =threading.Thread(target=display_thread)

# Start all threads
timer.start()
ai.start()
display.start()

#TODO: LED-bar

#FIX: Display

#TEST: AI Speech commands

