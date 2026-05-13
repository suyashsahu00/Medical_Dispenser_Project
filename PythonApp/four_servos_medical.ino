#include <Servo.h>

// Servo objects
Servo servo1;  // Box 1 - Pin 5
Servo servo2;  // Box 2 - Pin 6
Servo servo3;  // Box 3 - Pin 9
Servo servo4;  // Box 4 - Pin 10

// LED pins
const int led1 = 4;   // Box 1
const int led2 = 7;   // Box 2
const int led3 = 8;   // Box 3
const int led4 = 11;  // Box 4

void setup() {
  Serial.begin(115200);
  
  // Attach servos
  servo1.attach(5);
  servo2.attach(6);
  servo3.attach(9);
  servo4.attach(10);
  
  // Set LED pins as output
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  
  // Initial position: all servos at 0 degrees, LEDs OFF
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
  
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  digitalWrite(led4, LOW);
  
  Serial.println("Servo & LED Control Ready! Send 1,2,3 or 4");
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();
    
    switch(input) {
      case '1':
        activateBox(1, servo1, led1);
        break;
        
      case '2':
        activateBox(2, servo2, led2);
        break;
        
      case '3':
        activateBox(3, servo3, led3);
        break;
        
      case '4':
        activateBox(4, servo4, led4);
        break;
        
      default:
        // Optional: echo unknown command
        if (isprint(input)) {
          Serial.print("Unknown command: ");
          Serial.println(input);
        }
        break;
    }
  }
}

// Function to move servo from 0 to 180 and turn on LED
void activateBox(int boxNum, Servo &servo, int ledPin) {
  Serial.print("Activating Box ");
  Serial.println(boxNum);
  
  // Turn ON LED
  digitalWrite(ledPin, HIGH);
  
  // Sweep servo from 0 to 180 degrees
  for (int pos = 0; pos <= 180; pos += 2) {  // Faster sweep
    servo.write(pos);
    delay(1);  // Adjust speed here (lower = faster)
  }
  
  // Optional: hold at 180 for a moment
  delay(5);
  
  // Sweep back to 0 (optional - remove if you want only one way)
  for (int pos = 180; pos >= 0; pos -= 2) {
    servo.write(pos);
    delay(1);
  }
  
  // Turn OFF LED after movement (optional)
  // digitalWrite(ledPin, LOW);
}