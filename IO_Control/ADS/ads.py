import time
import board
import busio

from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn

RATIO = 24 / 2.17 # volts / volts
# i.e. 24V is represented as 2.17V

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ADS1015s at 0x48 and 0x49
ads1 = ADS1015(i2c, address=0x48)
ads2 = ADS1015(i2c, address=0x49)

# Create AnalogIn channels
ads1_channels = [AnalogIn(ads1, ch) for ch in [0,1,2,3]]
ads2_channels = [AnalogIn(ads2, ch) for ch in [0,1,2,3]]

try:
    while True:
        print("ADS1015 #1 (0x48) readings:")
        for i, ch in enumerate(ads1_channels):
            voltage = ch.voltage * RATIO
            print(f"  Channel {i}: {voltage:.3f} V")

        print("ADS1015 #2 (0x49) readings:")
        for i, ch in enumerate(ads2_channels):
            voltage = ch.voltage * RATIO
            print(f"  Channel {i}: {voltage:.3f} V")

        print("\n--- Waiting 1 second ---\n")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting cleanly...")
