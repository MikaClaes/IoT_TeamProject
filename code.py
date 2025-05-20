# Write your code here :-)
import time
import board
import busio
import wifi
import socketpool
import ssl
import os
from adafruit_bmp280 import Adafruit_BMP280_I2C
import adafruit_bh1750
from adafruit_minimqtt import adafruit_minimqtt as MQTT

MQTT_BROKER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_USERNAME = "NzATGQQiOTQ6Li4cDR0uPRU" #ours
MQTT_PASSWORD = "TIOMdunWkSkgieNfFse18ZR9" #ours
MQTT_CLIENT_ID = "NzATGQQiOTQ6Li4cDR0uPRU" #ours
MQTT_TOPIC = "channels/2954416/publish" #ours


i2c = busio.I2C(board.GP1, board.GP0)
bh1750 = adafruit_bh1750.BH1750(i2c)
bmp280 = Adafruit_BMP280_I2C(i2c)
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

mqtt_client = MQTT.MQTT(
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    client_id=MQTT_CLIENT_ID,
    socket_pool=pool,
    ssl_context=ssl_context
)

def connect_and_publish():
    try:
        mqtt_client.connect()
        print("Connected to MQTT broker.")

        while True:
            temp = bmp280.temperature
            pressure = bmp280.pressure
            lux = bh1750.lux

            print(f"Light: {lux:.2f} lux")
            print(f"Temperature: {temp:.2f} °C")

            # Create payload for ThingSpeak
            payload = f"field1={lux:.2f}&field2={temp:.2f}&status=MQTTPUBLISH"
            mqtt_client.publish(MQTT_TOPIC, payload)

            time.sleep(15)  # ThingSpeak rate limit
    except Exception as e:
        print("MQTT Error:", e)
        time.sleep(5)

connect_and_publish()
