import requests
import time

# ThingSpeak channel settings
CHANNEL_ID = "2954416"  # Replace with your ThingSpeak Channel ID
READ_API_KEY = "BHGP4YRDAWHKPPSE"  # Replace with your Read API Key
BASE_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

# Function to retrieve the last data entry from ThingSpeak
def get_last_thingspeak_entry():
    try:
        params = {
            "api_key": READ_API_KEY,
            "results": 1  # Only get the last entry
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        feeds = data.get("feeds", [])

        if feeds:
            latest_entry = feeds[0]
            value1 = latest_entry.get("field1")
            value2 = latest_entry.get("field2")
            print("Field1:", value1)
            print("Field2:", value2)
            print("Created at:", latest_entry.get("created_at"))
            return value1, value2
        else:
            print("No data found.")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None, None