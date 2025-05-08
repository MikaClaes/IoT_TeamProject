import time
import board
import busio
import adafruit_bmp280
from adafruit_bus_device.i2c_device import I2CDevice

# Set up I2C for BH1750 (I2C0)
i2c0 = busio.I2C(board.GP1, board.GP0)
device_bh = I2CDevice(i2c0, 0x23)

# Initialize BH1750 in Continuously H Resolution Mode
with device_bh:
    device_bh.write(bytes([0x10]))

def read_bh1750():
    with device_bh:
        data = bytearray(2)
        device_bh.readinto(data)
    lux = ((data[0] << 8) | data[1]) / 1.2
    return lux

# Set up I2C for BMP280 (I2C1)
i2c1 = busio.I2C(board.GP3, board.GP2)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c1, address=0x77)


while True:
    lux = read_bh1750()
    temperature = bmp280.temperature
    #pressure = bmp280.pressure

    print(f"Light: {lux:.2f} lux")
    print(f"Temperature: {temperature:.2f} °C")
    #print(f"Pressure: {pressure:.2f} hPa")
    time.sleep(1)

