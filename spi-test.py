import spidev
import RPi.GPIO as GPIO
import time

class CustomNFCReader:
    def __init__(self, bus, device, rst_pin):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000  # 1MHz
        self.rst_pin = rst_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rst_pin, GPIO.OUT)
        self.reset()

    def reset(self):
        GPIO.output(self.rst_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.rst_pin, GPIO.HIGH)
        time.sleep(0.1)

    def write_register(self, address, value):
        self.spi.xfer2([(address << 1) & 0x7E, value])

    def read_register(self, address):
        return self.spi.xfer2([((address << 1) & 0x7E) | 0x80, 0])[1]

    def test_communication(self):
        # Versuche, einen Register zu lesen (z.B. VersionReg)
        version = self.read_register(0x37)
        if version:
            print(f"Kommunikation erfolgreich. Chip-Version: 0x{version:02x}")
            return True
        else:
            print("Kommunikation fehlgeschlagen.")
            return False

    def close(self):
        self.spi.close()
        GPIO.cleanup()

def test_nfc(bus, device, rst_pin):
    reader = CustomNFCReader(bus, device, rst_pin)
    try:
        if reader.test_communication():
            print("NFC-Modul funktioniert korrekt.")
        else:
            print("Problem mit dem NFC-Modul erkannt.")
    finally:
        reader.close()

if __name__ == "__main__":
    # Diese Werte können Sie anpassen
    SPI_BUS = 0  # 0 oder 1
    SPI_DEVICE = 0  # 0 oder 1
    RST_PIN = 25  # GPIO-Pin-Nummer für Reset

    print("Starte angepassten NFC-Modul-Test...")
    test_nfc(SPI_BUS, SPI_DEVICE, RST_PIN)