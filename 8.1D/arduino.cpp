#include <ArduinoBLE.h>

// Pin definitions
const int HALLWAY_LED = 2;
const int BATHROOM_LED = 3;
const int FAN_PIN = 4;
const int LIGHT_SENSOR = A0;

// If light reading is below this number, room is dark
const int DARK_THRESHOLD = 300;

BLEService lightService("19B10000-E8F2-537E-4F6C-D104768A1214");
BLEStringCharacteristic commandChar("19B10001-E8F2-537E-4F6C-D104768A1214", BLEWrite, 20);

void setup() {
  Serial.begin(9600);
  pinMode(HALLWAY_LED, OUTPUT);
  pinMode(BATHROOM_LED, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);

  if (!BLE.begin()) {
    Serial.println("BLE failed to start!");
    while (1);
  }

  BLE.setLocalName("ArduinoLights");
  BLE.setAdvertisedService(lightService);
  lightService.addCharacteristic(commandChar);

  
  BLE.addService(lightService);
  BLE.advertise();

  Serial.println("Arduino ready, waiting for commands...");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.println("RPi connected!");

    while (central.connected()) {
      if (commandChar.written()) {
        String cmd = commandChar.value();
        int lightLevel = analogRead(LIGHT_SENSOR);
        bool isDark = (lightLevel < DARK_THRESHOLD);

        Serial.print("Command received: ");
        Serial.println(cmd);
        Serial.print("Light level: ");
        Serial.println(lightLevel);

        if (cmd == "LIGHTS_ON") {
          if (isDark) {
            digitalWrite(HALLWAY_LED, HIGH);
            digitalWrite(BATHROOM_LED, HIGH);
            Serial.println("Lights turned ON - room was dark");
          } else {
            Serial.println("Room is bright enough, lights not needed");
          }
        }
        else if (cmd == "LIGHTS_OFF") {
          digitalWrite(HALLWAY_LED, LOW);
          digitalWrite(BATHROOM_LED, LOW);
          Serial.println("Lights turned OFF");
        }
        else if (cmd == "FAN_ON") {
          digitalWrite(FAN_PIN, HIGH);
          Serial.println("Fan turned ON");
        }
        else if (cmd == "FAN_OFF") {
          digitalWrite(FAN_PIN, LOW);
          Serial.println("Fan turned OFF");
        }
      }
    }
    Serial.println("RPi disconnected");
  }
}
