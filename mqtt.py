import requests
import json

# ThingSpeak channel settings
CHANNEL_ID = "2954416"  # Replace with your ThingSpeak Channel ID
READ_API_KEY = "BHGP4YRDAWHKPPSE"  # Replace with your Read API Key
BASE_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

# Function to retrieve data from ThingSpeak
def get_thingspeak_data():
    try:
        # Construct the API URL with parameters
        params = {
            "api_key": READ_API_KEY,
            "results": 10  # Number of data points to retrieve (adjust as needed)
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the JSON response
        data = response.json()
        feeds = data.get("feeds", [])

        # Process the retrieved data
        for feed in feeds:
            print("Entry ID:", feed.get("entry_id"))
            for field in feed:
                if field.startswith("field"):
                    print(f"{field}: {feed[field]}")
            print("Created at:", feed.get("created_at"))
            print("---")

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data: {e}")

# Run the function
while True:
    get_thingspeak_data()