import smbus
import RPi.GPIO as GPIO
import time

class PN7150:
    def __init__(self, bus_number, address, irq_pin, ven_pin):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        self.irq_pin = irq_pin
        self.ven_pin = ven_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.irq_pin, GPIO.IN)
        GPIO.setup(self.ven_pin, GPIO.OUT)
        self.reset()

    def reset(self):
        GPIO.output(self.ven_pin, GPIO.LOW)
        time.sleep(0.5)  # Wartezeit erhöhen
        GPIO.output(self.ven_pin, GPIO.HIGH)
        time.sleep(0.5)  # Wartezeit erhöhen

    def read_register(self, reg):
        try:
            result = self.bus.read_byte_data(self.address, reg)
            print(f"Register 0x{reg:02X} gelesen: 0x{result:02X}")
            return result
        except Exception as e:
            print(f"Fehler beim Lesen des Registers 0x{reg:02X}: {e}")
            return None

    def write_register(self, reg, value):
        try:
            self.bus.write_byte_data(self.address, reg, value)
            print(f"Register 0x{reg:02X} geschrieben: 0x{value:02X}")
        except Exception as e:
            print(f"Fehler beim Schreiben in das Register 0x{reg:02X}: {e}")

    def test_communication(self):
        # Beispiel: Lese ein bekanntes Register, z.B. Product ID
        try:
            product_id = self.read_register(0x00)
            if product_id is not None:
                print(f"Kommunikation erfolgreich. Produkt-ID: 0x{product_id:02X}")
                return True
            else:
                print("Produkt-ID konnte nicht gelesen werden.")
                return False
        except Exception as e:
            print(f"Kommunikation fehlgeschlagen: {e}")
            return False

    def close(self):
        self.bus.close()
        GPIO.cleanup()

def test_nfc(bus_number, address, irq_pin, ven_pin):
    reader = PN7150(bus_number, address, irq_pin, ven_pin)
    try:
        if reader.test_communication():
            print("NFC-Modul funktioniert korrekt.")
        else:
            print("Problem mit dem NFC-Modul erkannt.")
    finally:
        reader.close()

if __name__ == "__main__":
    # Diese Werte können Sie anpassen
    I2C_BUS = 1  # I2C-Bus Nummer
    I2C_ADDRESS = 0x2b  # I2C-Adresse des PN7150
    IRQ_PIN = 24  # GPIO-Pin für IRQ
    VEN_PIN = 18  # GPIO-Pin für VEN

    print("Starte angepassten NFC-Modul-Test...")
    test_nfc(I2C_BUS, I2C_ADDRESS, IRQ_PIN, VEN_PIN)
