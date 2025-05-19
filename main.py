import threading
from servo_led import pomodoro_timer
from voice_ai import speech_recognition


#Functions
def timer_thread():
    print("Starting Pomodoro timer with servo and RGB LED indication")
    print("Servo angles: Work (0°), Short Break (180°), Long Break (180°)")
    print("LED: Red (blink 3x then solid for work), Green (blink 3x then solid for short break), Blue (blink 3x then solid for long break)")
    pomodoro_timer()

def ai_thread():
    speech_recognition()

#Variabelen
optimal_light_min = 450
optimal_light_max = 500
optimal_temperature_min = 21.5
optimal_temperature_max = 22.5
current_temp = 0
current_lux = 0

# Multithread setup with separate threads for each function
timer = threading.Thread(target=timer_thread)
ai = threading.Thread(target=ai_thread)

# Start all threads
timer.start()
ai.start()

#TEST: Lichtsensor

#TEST: Temp sensor

#TODO: LED-bar

#TEST: Pomodoro Timer

#TEST: Motor (zandloper)

#TODO: Knop: voor in de bib

#TEST: Thingspeak

#IMPLEMENT: Display

#TODO: AI Speech commands