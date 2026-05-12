#include <Servo.h>

// ---- Servo objects ----
Servo servo1;   // Box 1  (e.g. Painkiller)
Servo servo2;   // Box 2  (e.g. Paracetamol / Dolo)
Servo servo3;   // Box 3
Servo servo4;   // Box 4

// ---- Serial buffer ----
String inputString = "";
bool stringComplete = false;

// ---- Pin mapping (change if needed) ----
// Use PWM pins for servos
const int servoPin1 = 9;
const int ledPin1   = 10;

const int servoPin2 = 6;
const int ledPin2   = 11;

const int servoPin3 = 5;
const int ledPin3   = 12;

const int servoPin4 = 3;
const int ledPin4   = 13;

void setup() {
  Serial.begin(9600);

  servo1.attach(servoPin1);
  pinMode(ledPin1, OUTPUT);

  servo2.attach(servoPin2);
  pinMode(ledPin2, OUTPUT);

  servo3.attach(servoPin3);
  pinMode(ledPin3, OUTPUT);

  servo4.attach(servoPin4);
  pinMode(ledPin4, OUTPUT);

  // Initial position & LEDs OFF
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);

  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);
  digitalWrite(ledPin4, LOW);

  inputString.reserve(50);
}

void loop() {
  // Read incoming serial characters
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
    inputString = "";
    stringComplete = false;
  }
}

// ---- Handle commands from PC ----
// Accepted strings (case-insensitive):
// "painkiller" or "box1"  -> Servo 1
// "paracetamol", "dolo" or "box2" -> Servo 2
// "box3" -> Servo 3
// "box4" -> Servo 4
void processCommand(String cmd) {
  cmd.trim();
  cmd.toLowerCase();

  if (cmd == "painkiller" || cmd == "box1") {
    handleAction(servo1, ledPin1);
    Serial.println("OK: BOX1");
  }
  else if (cmd == "paracetamol" || cmd == "dolo" || cmd == "box2") {
    handleAction(servo2, ledPin2);
    Serial.println("OK: BOX2");
  }
  else if (cmd == "box3") {
    handleAction(servo3, ledPin3);
    Serial.println("OK: BOX3");
  }
  else if (cmd == "box4") {
    handleAction(servo4, ledPin4);
    Serial.println("OK: BOX4");
  }
  else {
    Serial.print("Unknown command: ");
    Serial.println(cmd);
  }
}

// Common action for all servos
void handleAction(Servo &servoMotor, int ledPin) {
  servoMotor.write(90);       // open
  digitalWrite(ledPin, HIGH); // LED ON
  delay(3000);                // wait 3 sec
  servoMotor.write(0);        // close
  digitalWrite(ledPin, LOW);  // LED OFF
}
