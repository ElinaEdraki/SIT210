#include "thingProperties.h"

#define PIN_LIVING_ROOM  5
#define PIN_BATHROOM     3
#define PIN_CLOSET       4

void setup() {
  Serial.begin(9600);
  delay(1500);

  pinMode(PIN_LIVING_ROOM, OUTPUT);
  pinMode(PIN_BATHROOM,    OUTPUT);
  pinMode(PIN_CLOSET,      OUTPUT);

  digitalWrite(PIN_LIVING_ROOM, LOW);
  digitalWrite(PIN_BATHROOM,    LOW);
  digitalWrite(PIN_CLOSET,      LOW);

  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();
}

void onLivingRoomOnChange() {
  toggleLight("living room");
}

void onBathroomOnChange() {
  toggleLight("bathroom");
}

void onClosetOnChange() {
  toggleLight("closet");
}

void toggleLight(String roomName) {
  roomName.toLowerCase();
  roomName.trim();

  if (roomName == "living room") {
    digitalWrite(PIN_LIVING_ROOM, livingRoomOn ? HIGH : LOW);
    Serial.println("Living Room: " + String(livingRoomOn ? "ON" : "OFF"));

  } else if (roomName == "bathroom") {
    digitalWrite(PIN_BATHROOM, bathroomOn ? HIGH : LOW);
    Serial.println("Bathroom: " + String(bathroomOn ? "ON" : "OFF"));

  } else if (roomName == "closet") {
    digitalWrite(PIN_CLOSET, closetOn ? HIGH : LOW);
    Serial.println("Closet: " + String(closetOn ? "ON" : "OFF"));
  }
}
