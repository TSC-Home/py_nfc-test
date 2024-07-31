import RPi.GPIO as GPIO
from smbus2 import SMBus, i2c_msg
import time

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Funktion zum Testen eines GPIO-Pins
def test_gpio_pin(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.1)
    state = GPIO.input(pin)
    GPIO.output(pin, GPIO.LOW)
    return state == GPIO.HIGH

# Liste aller GPIO-Pins auf dem Raspberry Pi 4
gpio_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

# Testen aller GPIO-Pins
print("Testing GPIO pins:")
for pin in gpio_pins:
    if test_gpio_pin(pin):
        print(f"GPIO pin {pin} works correctly.")
    else:
        print(f"GPIO pin {pin} does not work correctly.")

# I2C-Scan
def scan_i2c():
    bus = SMBus(1)  # I2C-Bus 1 verwenden
    devices = []
    for address in range(0x03, 0x78):
        try:
            bus.read_byte(address)
            devices.append(hex(address))
        except OSError:
            pass
    bus.close()
    return devices

# Testen der I2C-Verbindung
print("\nScanning I2C bus for devices:")
devices = scan_i2c()
if devices:
    print(f"Found I2C devices at: {', '.join(devices)}")
else:
    print("No I2C devices found.")

# Aufräumen
GPIO.cleanup()
