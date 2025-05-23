#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED display settings
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Ultrasonic sensor pins
const int trigPin = 7;
const int echoPin = 6;

// LED pins
const int redLED = 12;
const int greenLED = 13;

// Buzzer pin
const int buzzerPin = 8;

bool objectDetected = false;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  Serial.begin(9600);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    for (;;);  // Loop forever if display fails
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("System Starting...");
  display.display();
  delay(2000);
  display.clearDisplay();
  display.display();
}

void loop() {
  // Trigger ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read echo
  long duration = pulseIn(echoPin, HIGH, 30000);
  float distance = duration * 0.034 / 2;

  // Determine current state
  bool isDetected = (duration != 0 && distance > 0 && distance <= 30);

  // Only send if the state changes
  if (isDetected != objectDetected) {
    objectDetected = isDetected;
    if (objectDetected) {
      Serial.println("CAPTURE");
    } else {
      Serial.println("CLEAR");
    }
  }

  // Display on OLED
  display.clearDisplay();
  display.setCursor(0, 0);

  if (objectDetected) {
    display.println("Object Detected");
    digitalWrite(redLED, HIGH);
    digitalWrite(greenLED, LOW);
    digitalWrite(buzzerPin, HIGH);
  } else {
    display.println("No Object Found");
    digitalWrite(redLED, LOW);
    digitalWrite(greenLED, HIGH);
    digitalWrite(buzzerPin, LOW);
  }

  display.setCursor(0, 20);
  display.print("Distance: ");
  display.print(distance);
  display.println(" cm");
  display.display();

  delay(500);
}
