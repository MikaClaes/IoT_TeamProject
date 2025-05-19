
import queue
import time
#Functions

#Variabelen
optimal_light_min = 450
optimal_light_max = 500
optimal_temperature_min = 21.5
optimal_temperature_max = 22.5

#TODO: Lichtsensor

#TODO: Temp sensor

#TODO: LED-bar

#TODO: Pomodoro Timer

#TODO: Motor (zandloper)

#TODO: Knop

#TODO: Thingspeak

#TODO: Display

#TODO: AI Speech commands

speech_queue = queue.Queue()

# Varianten voor commando's
command_variants = {
    "start": ["start", "staart", "stard", "stort", "star", "stah", "staat", "st", "sart"],
    "stop": ["stop", "stap", "stob", "stahp", "stoph", "shtop", "sluit", "sloot", "slui", "slud", "sto"]
}

def process_text(text):
    """Check voor start/stop commando's met varianten"""
    text = text.lower().strip()
    for command, variants in command_variants.items():
        if text in variants or command in text:
            return command
    return None

def callback(recognizer, audio):
    """Verwerk spraakinput"""
    try:
        text = recognizer.recognize_google(audio, language="nl-NL")
        command = process_text(text)
        if command:
            speech_queue.put(command)
    except (sr.UnknownValueError, sr.RequestError):
        pass  # Negeer fouten stil

def init_speech_recognition():
    """Initialiseer spraakherkenning met Orange Pi 3 LTS ingebouwde microfoon"""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.5

    # Controleer beschikbare microfoons
    mics = sr.Microphone.list_microphone_names()
    if not mics:
        print("Geen microfoons gevonden!")
        return None, None

    # Selecteer ingebouwde microfoon (ALSA apparaat op Orange Pi)
    mic_index = None
    for i, mic_name in enumerate(mics):
        if "default" in mic_name.lower() or "alsa" in mic_name.lower() or "analog" in mic_name.lower():
            mic_index = i
            break
    if mic_index is None:
        print("Ingebouwde microfoon niet gevonden, eerste microfoon wordt gebruikt")
        mic_index = 0

    try:
        mic = sr.Microphone(device_index=mic_index)
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Microfoon klaar")
        stop_listening = recognizer.listen_in_background(mic, callback)
        return recognizer, stop_listening
    except Exception as e:
        print(f"Microfoon fout: {e}")
        return None, None

# Main-loop
def main():
    recognizer, stop_listening = init_speech_recognition()
    speech_enabled = stop_listening is not None

    try:
        while True:
            while not speech_queue.empty():
                try:
                    command = speech_queue.get_nowait()
                    print(command)  # Print "start" of "stop"
                except queue.Empty:
                    break
            time.sleep(0.1)  # Voorkom CPU-overbelasting
    except KeyboardInterrupt:
        print("Programma onderbroken met Ctrl+C")

    if speech_enabled:
        stop_listening(wait_for_stop=False)
        print("Spraakherkenning gestopt")

if __name__ == "__main__":
    main()