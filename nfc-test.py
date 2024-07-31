import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

def test_nfc():
    reader = SimpleMFRC522()

    try:
        print("NFC-Modul initialisiert. Warte auf Tag...")
        id, text = reader.read()
        print(f"Tag erkannt! ID: {id}")
        print(f"Text auf dem Tag: {text}")
        return True
    except Exception as e:
        print(f"Fehler beim Lesen des NFC-Tags: {e}")
        return False
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    print("Starte NFC-Modul-Test...")
    success = test_nfc()
    
    if success:
        print("NFC-Modul funktioniert korrekt.")
    else:
        print("Es gab ein Problem mit dem NFC-Modul.")