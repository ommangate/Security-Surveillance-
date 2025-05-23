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

// Push Button Pin
const int buttonPin = 9; // Use internal pull-up

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); // Active LOW button

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
  // Emergency stop
  if (digitalRead(buttonPin) == LOW) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("EMERGENCY STOP");
    display.display();

    digitalWrite(redLED, LOW);
    digitalWrite(greenLED, LOW);
    digitalWrite(buzzerPin, LOW);

    // Wait until button is released
    while (digitalRead(buttonPin) == LOW) {
      delay(10);
    }

    display.setCursor(0, 20);
    display.println("Press again to resume");
    display.display();

    // Wait for user to press again
    while (digitalRead(buttonPin) == HIGH) {
      delay(10);
    }

    // Wait for release again
    while (digitalRead(buttonPin) == LOW) {
      delay(10);
    }

    display.clearDisplay();
    display.display();
    return;
  }

  // Ultrasonic sensor reading
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  float distance = duration * 0.034 / 2;

  Serial.print("Duration: ");
  Serial.print(duration);
  Serial.print(" µs, Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Display and buzzer/LED logic
  display.clearDisplay();
  display.setCursor(0, 0);

  if (duration == 0 || distance <= 0 || distance > 30) {
    display.println("No Object Found");
    digitalWrite(redLED, LOW);
    digitalWrite(greenLED, HIGH);
    digitalWrite(buzzerPin, LOW);
  } else {
    display.println("Object Detected");
    digitalWrite(redLED, HIGH);
    digitalWrite(greenLED, LOW);
    digitalWrite(buzzerPin, HIGH);
    Serial.println("CAPTURE");
  }

  display.setCursor(0, 20);
  display.print("Distance: ");
  display.print(distance);
  display.println(" cm");
  display.display();

  delay(500);
}
