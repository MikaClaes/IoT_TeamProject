import os
import ctypes
import subprocess
import speech_recognition as sr
import time
import sys

# Suppress ALSA warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['ALSA_CARD'] = '0'
os.environ['SDL_AUDIODRIVER'] = 'alsa'

# Set ALSA error handler to suppress warnings
try:
    asound = ctypes.CDLL('libasound.so')
    asound.snd_lib_error_set_handler(None)
except Exception as e:
    print(f"Kon ALSA error handler niet instellen: {e}")

# Constants
OPTIMAL_LIGHT_MIN = 450
OPTIMAL_LIGHT_MAX = 500
OPTIMAL_TEMPERATURE_MIN = 21.5
OPTIMAL_TEMPERATURE_MAX = 22.5

# Debug mode
DEBUG = True

# Command variants (Dutch)
command_variants = {
    "start": ["start", "staart", "stard", "stort", "star", "stah", "staat", "st", "sart",
              "starten", "beginnen", "begin", "aan", "ga", "gaan"],
    "stop": ["stop", "stap", "stob", "stahp", "stoph", "shtop", "sluit", "sloot", "slui",
             "slud", "sto", "stoppen", "afsluiten", "uit", "pauze", "pauzeren"]
}

def debug_print(message):
    """Print debug messages if DEBUG is enabled"""
    if DEBUG:
        print(f"[DEBUG] {message}")

def get_audio_devices():
    """Get a detailed list of audio devices using ALSA"""
    try:
        result = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return "Error getting audio devices"
    except Exception as e:
        return f"Exception: {e}"

def select_microphone():
    """List available microphones and select the correct one"""
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print("Beschikbare microfoons:")
        for i, mic in enumerate(mic_list):
            print(f"{i}: {mic}")
        
        # First try to find a headset/headphone microphone
        for i, mic_name in enumerate(mic_list):
            lower_name = mic_name.lower()
            if any(keyword in lower_name for keyword in ['headset', 'headphone', 'mic', 'acx00']):
                print(f"Geselecteerde microfoon: {mic_name} (index {i})")
                return i
        
        # If no headset mic found, try to use hw:0,0 which is often the default
        for i, mic_name in enumerate(mic_list):
            if 'hw:0,0' in mic_name:
                print(f"Geselecteerde microfoon: {mic_name} (index {i})")
                return i
                
        # Fall back to the first available microphone
        print(f"Geen specifieke microfoon gevonden, standaard microfoon gebruiken (index 0)")
        return 0
    except Exception as e:
        print(f"Fout bij microfoondetectie: {e}")
        print("Gedetailleerde audio-apparaatinformatie:")
        print(get_audio_devices())
        return 0

def setup_audio():
    """Configure audio settings for better recognition"""
    try:
        devnull = open(os.devnull, 'w')
        # Print current audio settings for debugging
        debug_print("Huidige audio-instellingen:")
        result = subprocess.run(["amixer", "get", "Capture"], capture_output=True, text=True, stderr=devnull)
        debug_print(result.stdout)
        
        # Set appropriate volume levels
        subprocess.run(["amixer", "set", "Capture", "90%"], stdout=subprocess.PIPE, stderr=devnull, check=False)
        subprocess.run(["amixer", "set", "Capture", "cap"], stdout=subprocess.PIPE, stderr=devnull, check=False)
        print("Microfoon volume ingesteld op 90% en capture ingeschakeld")
        
        # Check if settings were applied
        debug_print("Nieuwe audio-instellingen:")
        result = subprocess.run(["amixer", "get", "Capture"], capture_output=True, text=True, stderr=devnull)
        debug_print(result.stdout)
    except Exception as e:
        print(f"Kon microfoonvolume niet instellen: {e}")
        print("Probeer handmatig met 'alsamixer'")
    finally:
        devnull.close()

def test_microphone(recognizer, source):
    """Test if the microphone is picking up audio"""
    print("Microfoon test - Spreek gedurende 5 seconden...")
    try:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        print(f"Audio ontvangen! Lengte: {len(audio.frame_data)} bytes")
        debug_print(f"Sample rate: {audio.sample_rate}, Sample width: {audio.sample_width}")
        
        try:
            text = recognizer.recognize_google(audio, language="nl-NL")
            print(f"Herkende tekst: '{text}'")
        except sr.UnknownValueError:
            print("Spraak niet herkend, maar audio werd wel opgenomen")
        except sr.RequestError as e:
            print(f"Spraakherkenningsfout: {e}")
    except sr.WaitTimeoutError:
        print("WAARSCHUWING: Geen audio gedetecteerd. Controleer of de microfoon correct is aangesloten en werkt.")
    except Exception as e:
        print(f"Test microfoon fout: {e}")

def process_text(text):
    """Check for start/stop commands with variants"""
    if not text:
        return None
        
    text = text.lower().strip()
    print(f"Ontvangen tekst: '{text}'")
    
    # Split the text into words for more flexible matching
    words = text.split()
    debug_print(f"Woorden: {words}")
    
    # Check each word against the command variants
    for command, variants in command_variants.items():
        debug_print(f"Controleer commando: {command}, varianten: {variants}")
        for word in words:
            if word in variants:
                debug_print(f"Match gevonden: '{word}' voor commando '{command}'")
                return command
    
    # If no single word matches, check for partial matches in the full text
    for command, variants in command_variants.items():
        for variant in variants:
            if variant in text:
                debug_print(f"Partial match gevonden: '{variant}' in '{text}' voor commando '{command}'")
                return command
    
    debug_print("Geen commando herkend")
    return None

def listen_for_command(recognizer, source):
    """Listen for a single voice command"""
    try:
        print("\nLuisteren... (zeg 'start' of 'stop')")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        try:
            # Try with Dutch first
            text = recognizer.recognize_google(audio, language="nl-NL")
            debug_print(f"Herkend (nl-NL): '{text}'")
            result = process_text(text)
            if result:
                return result
                
            # If Dutch didn't match our commands, try English as fallback
            text = recognizer.recognize_google(audio, language="en-US")
            debug_print(f"Herkend (en-US): '{text}'")
            return process_text(text)
            
        except sr.UnknownValueError:
            print("Spraak niet herkend")
        except sr.RequestError as e:
            print(f"Spraakherkenningsfout: {e}")
    
    except sr.WaitTimeoutError:
        print("Geen spraak gedetecteerd (timeout)")
    except Exception as e:
        print(f"Luisterfout: {e}")
    
    return None

def check_internet_connection():
    """Check if we can connect to Google (required for speech recognition)"""
    try:
        response = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "speech.googleapis.com"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        return response.returncode == 0
    except:
        return False

def main():
    print("Orange Pi Spraakbesturing - Verbeterde versie")
    
    # Check internet connection
    if not check_internet_connection():
        print("WAARSCHUWING: Geen internetverbinding gedetecteerd. Spraakherkenning vereist internet.")
    
    # Initialize recognizer with more lenient settings
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 400  # Slightly higher threshold to reduce noise sensitivity
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    
    # Print audio device info
    debug_print("ALSA audio apparaten:")
    debug_print(get_audio_devices())
    
    # Select and setup microphone
    mic_index = select_microphone()
    setup_audio()
    
    app_running = False
    
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Kalibreren voor omgevingsgeluid... (3 seconden stilte aub)")
            recognizer.adjust_for_ambient_noise(source, duration=3)
            print(f"Microfoon klaar, drempel: {recognizer.energy_threshold}")
            
            # Test microphone
            test_microphone(recognizer, source)
            
            print("\nStart de normale luistermodus. Zeg 'start' om te beginnen of 'stop' om te eindigen.")
            
            while True:
                command = listen_for_command(recognizer, source)
                
                if command == "start" and not app_running:
                    print("\n=== APPLICATIE GESTART ===")
                    app_running = True
                elif command == "stop" and app_running:
                    print("\n=== APPLICATIE GESTOPT ===")
                    app_running = False
                elif command == "stop" and not app_running:
                    print("\nApplicatie is al gestopt")
                
                if app_running:
                    print("Applicatie actief...", end='\r')
                    time.sleep(0.1)
                else:
                    time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\nAfsluiten...")
    except Exception as e:
        print(f"Ernstige fout: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
