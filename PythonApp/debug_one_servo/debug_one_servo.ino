// ================================================================
// debug_one_servo.ino
// Minimal debug sketch — ONLY Servo 1 (Box 1, Pin 9)
// Upload this with Arduino IDE, then run debug_one_servo_python.py
// ================================================================

#include <Servo.h>

Servo servo1;             // Only servo being tested

const int servoPin1 = 9;  // PWM pin for Servo 1
const int ledPin1   = 10; // LED indicator for Box 1

String inputString   = "";
bool stringComplete  = false;

void setup() {
  Serial.begin(9600);

  servo1.attach(servoPin1);
  pinMode(ledPin1, OUTPUT);

  servo1.write(0);            // Start at closed (0 degrees)
  digitalWrite(ledPin1, LOW); // LED off

  inputString.reserve(50);

  Serial.println("DEBUG MODE: Single Servo (Box 1) Ready");
  Serial.println("Send 'box1' or 'painkiller' to test.");
}

void loop() {
  // Buffer serial input until newline
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }

  if (stringComplete) {
    processCommand(inputString);
    inputString     = "";
    stringComplete  = false;
  }
}

void processCommand(String cmd) {
  cmd.trim();
  cmd.toLowerCase();

  Serial.print("Received command: [");
  Serial.print(cmd);
  Serial.println("]");

  if (cmd == "box1" || cmd == "painkiller") {
    Serial.println("Opening BOX 1...");

    servo1.write(90);           // Open position
    digitalWrite(ledPin1, HIGH);
    delay(3000);                // Hold open for 3 seconds

    Serial.println("Closing BOX 1");
    servo1.write(0);            // Close position
    digitalWrite(ledPin1, LOW);

    Serial.println("OK: BOX1 DONE");
  }
  else {
    Serial.print("Unknown command: [");
    Serial.print(cmd);
    Serial.println("] — expected 'box1' or 'painkiller'");
  }
}
