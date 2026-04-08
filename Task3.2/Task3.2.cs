#include <WiFiNINA.h>
#include <PubSubClient.h>

// WiFi
char wifiName[] = "Nomi";
char wifiPass[] = "elina13841384%%";

// MQTT
char broker[] = "broker.emqx.io";

WiFiClient net;
PubSubClient mqtt(net);

// Pins
const int trig = 2;
const int echoPin = 3;
const int ledA = 4;
const int ledB = 5;

// Variables
volatile unsigned long startTime = 0;
volatile unsigned long endTime = 0;
volatile bool newData = false;

int dist = 0;
unsigned long prevTime = 0;

// WiFi connection
void connectWiFi() {
  WiFi.begin(wifiName, wifiPass);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

// MQTT message callback
void onMessage(char* topic, byte* payload, unsigned int len) {
  String msg = "";
  for (int i = 0; i < len; i++) msg += (char)payload[i];

  if (String(topic) == "ES/Wave") {
    digitalWrite(ledA, HIGH);
    digitalWrite(ledB, HIGH);
  }
  if (String(topic) == "ES/Pat") {
    digitalWrite(ledA, LOW);
    digitalWrite(ledB, LOW);
  }
}

// MQTT reconnect
void connectMQTT() {
  while (!mqtt.connected()) {
    if (mqtt.connect("clientElina")) {
      mqtt.subscribe("ES/Wave");
      mqtt.subscribe("ES/Pat");
    } else delay(2000);
  }
}

// ISR for echo pin
void echoISR() {
  if (digitalRead(echoPin)) startTime = micros();
  else {
    endTime = micros();
    newData = true;
  }
}

// Trigger ultrasonic
void triggerUltrasonic() {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
}

// Get distance if available
int getDistance() {
  if (newData) {
    newData = false;
    return (endTime - startTime) * 0.034 / 2;
  }
  return -1;
}

void setup() {
  Serial.begin(9600);
  pinMode(trig, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledA, OUTPUT);
  pinMode(ledB, OUTPUT);

  connectWiFi();
  mqtt.setServer(broker, 1883);
  mqtt.setCallback(onMessage);

  attachInterrupt(digitalPinToInterrupt(echoPin), echoISR, CHANGE);
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  triggerUltrasonic();

  int d = getDistance();
  if (d != -1) {
    dist = d;
    Serial.println(dist);

    if (millis() - prevTime > 2000) {
      if (dist > 0 && dist < 10) {
        mqtt.publish("ES/Wave", "Elina");
        prevTime = millis();
      } else if (dist >= 10 && dist < 20) {
        mqtt.publish("ES/Pat", "Elina");
        prevTime = millis();
      }
    }
  }

  delay(200);
}
