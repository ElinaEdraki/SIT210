#include <Wire.h>
#include <BH1750.h>
#include <WiFiNINA.h>
#include <DHT.h>

#define DHTPIN 3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

BH1750 lightMeter;

char ssid[] = "Nomi";
char pass[] = "elina13841384%%";

String IFTTT_Key = "bQjfHRisNozwj2DKpcl6Av";

WiFiClient client;

float tempThreshold = 35.0; 
int lightThreshold = 100;

bool sunlight = false;
bool tempAlertSent = false;

// Timing variables
unsigned long previousReadTime = 0;
const unsigned long readInterval = 5000; 

void setup() {
  Serial.begin(9600);
  Wire.begin();
  lightMeter.begin();
  dht.begin();

  // Connect to WiFi
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(1000);  // Only here we still need a short delay to avoid spamming WiFi
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  unsigned long currentTime = millis();

  // Check if is the time to read sensors
  if (currentTime - previousReadTime >= readInterval) {
    previousReadTime = currentTime;

    float light = lightMeter.readLightLevel();
    float temp = dht.readTemperature();

    Serial.print("Light: ");
    Serial.print(light);
    Serial.print("  -  Temp: ");
    Serial.println(temp);

    // Light sensor triggers
    if (light > lightThreshold && sunlight == false) {
      sunlight = true;
      sendIFTTT("sunlight_start");
    }
    if (light <= lightThreshold && sunlight == true) {
      sunlight = false;
      sendIFTTT("sunlight_stop");
    }

    // Temperature sensor triggers
    if (temp > tempThreshold && tempAlertSent == false) {
      tempAlertSent = true;
      sendIFTTT("high_temperature");
    }
    if (temp <= tempThreshold && tempAlertSent == true) {
      tempAlertSent = false;
    }
  }

}

void sendIFTTT(String event) {
  if (client.connect("maker.ifttt.com", 80)) {
    Serial.println("Connected to server");

    String PATH_NAME = "/trigger/" + event + "/with/key/" + IFTTT_Key;

    client.println("GET " + PATH_NAME + " HTTP/1.1");
    client.println("Host: maker.ifttt.com");
    client.println("Connection: close");
    client.println();

    Serial.println("Notification sent: " + event);
  }
  else {
    Serial.println("Connection failed");
  }
}
