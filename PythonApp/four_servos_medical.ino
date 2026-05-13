#include <Servo.h>

// Servo objects
Servo servo1;  // Pin 5  - Box 1
Servo servo2;  // Pin 6  - Box 2
Servo servo3;  // Pin 9  - Box 3
Servo servo4;  // Pin 10 - Box 4

// LED pins
const int led1 = 4;   // Box 1
const int led2 = 7;   // Box 2
const int led3 = 8;   // Box 3
const int led4 = 11;  // Box 4

void setup() {
  Serial.begin(115200);
  
  servo1.attach(5);
  servo2.attach(6);
  servo3.attach(9);
  servo4.attach(10);
  
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  
  // Initial Position
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
  
  allLEDsOff();
  
  Serial.println("Fast Servo Control Ready!");
  Serial.println("Send 1, 2, 3 or 4");
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();
    
    switch(input) {
      case '1': activateBox(servo1, led1, 1); break;
      case '2': activateBox(servo2, led2, 2); break;
      case '3': activateBox(servo3, led3, 3); break;
      case '4': activateBox(servo4, led4, 4); break;
    }
  }
}

// Main Function - Fast Movement
void activateBox(Servo &servo, int ledPin, int boxNum) {
  Serial.print("Activating Box ");
  Serial.println(boxNum);
  
  digitalWrite(ledPin, HIGH);   // LED ON
  
  // Fast Move to 180°
  for (int pos = 0; pos <= 150; pos += 5) {
    servo.write(pos);
    delay(5);        // Very fast movement
  }
  
  delay(3000);       // Hold at 180° for 3 seconds
  
  // Fast Return to 0°
  for (int pos = 150; pos >= 0; pos -= 5) {
    servo.write(pos);
    delay(5);        // Very fast return
  }
  
  digitalWrite(ledPin, LOW);   // LED OFF after 3 seconds
  
  Serial.print("Box ");
  Serial.print(boxNum);
  Serial.println(" Done.");
}

void allLEDsOff() {
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  digitalWrite(led4, LOW);
}