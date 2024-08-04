import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

# Die Befehle als Byte-Arrays
battery_on = b'\x50\x50\x50\x50'
closed = b'\x4B\x4D\x4B\x4D'
inserted_opened = b'\x41\x4E\x41\x44'
opened = b'\x59\x52\x52\x48'

def write_block(data):
    try:
        reader.write(data)
        print(f"Daten erfolgreich geschrieben: {data}")
        return True
    except Exception as e:
        print(f"Fehler beim Schreiben: {e}")
        return False

try:
    while True:
        print("Bitte NFC-Tag auflegen...")
        id, text = reader.read()
        print(f"Tag erkannt mit ID: {id}")
        
        if write_block(closed):
            print("'Closed' Befehl geschrieben.")
        else:
            print("Fehler beim Schreiben des 'Closed' Befehls.")
        
        time.sleep(1)
        
        if write_block(battery_on):
            print("'Battery On' Befehl geschrieben.")
        else:
            print("Fehler beim Schreiben des 'Battery On' Befehls.")
        
        time.sleep(5)

except KeyboardInterrupt:
    print("Programm durch Benutzer beendet")

finally:
    GPIO.cleanup()