import threading
from servo_led import pomodoro_timer
from voice_ai import speech_recognition
from mqtt import get_last_thingspeak_entry
from display import ChangeDisplay
from drukknop import button_press
import time

# Paused event
paused_event = threading.Event()

# Functies
def timer_thread():
    pomodoro_timer(paused_event)  # Geef de event door

def voice_ai_thread():
    speech_recognition()

def display_thread():
    while True:
        current_lux, current_temp = get_last_thingspeak_entry()
        ChangeDisplay(float(current_lux), float(current_temp))

def button_thread():
    button_press(paused_event)  # Geef event door

# Threads
timer = threading.Thread(target=timer_thread)
ai = threading.Thread(target=voice_ai_thread)
display = threading.Thread(target=display_thread)
button = threading.Thread(target=button_thread)

# Start alles
timer.start()
ai.start()
display.start()
button.start()
