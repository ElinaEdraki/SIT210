import speech_recognition as sr
import asyncio
from bleak import BleakClient
import time

ARDUINO_ADDRESS = "B0:B2:1C:56:1D:56"
CHAR_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

r = sr.Recognizer()

def listen_for_command():
    with sr.Microphone() as source:
        print("Listening... say a command")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio).lower()
            print("You said: " + text)
            return text
        except sr.WaitTimeoutError:
            print("No speech detected")
            return ""
        except sr.UnknownValueError:
            print("Could not understand")
            return ""
        except sr.RequestError as e:
            print("Network error: " + str(e))
            return ""

async def send_command(command):
    try:
        async with BleakClient(ARDUINO_ADDRESS) as client:
            await client.write_gatt_char(CHAR_UUID, command.encode())
            print("Sent: " + command)
    except Exception as e:
        print("Bluetooth error: " + str(e))

print("Voice control started. Speak your command!")
print("Commands: lights on, lights off, fan on, fan off")

while True:
    command = listen_for_command()

    if "lights on" in command or "turn on" in command:
        asyncio.run(send_command("LIGHTS_ON"))
    elif "lights off" in command or "turn off" in command:
        asyncio.run(send_command("LIGHTS_OFF"))
    elif "fan on" in command:
        asyncio.run(send_command("FAN_ON"))
    elif "fan off" in command:
        asyncio.run(send_command("FAN_OFF"))
    else:
        if command:
            print("Command not recognised, try again")

    time.sleep(0.5)
