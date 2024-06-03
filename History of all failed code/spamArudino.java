#include <Stepper.h>

const float STEPS_PER_REV = 32;
const float GEAR_RED = 64;
const int stepsPerRevolution = 25000;
bool prevRunning = false;

Stepper myStepperFORWARD(stepsPerRevolution, 8, 9);
Stepper myStepperLEFT(stepsPerRevolution, 6, 7);

float currTime = 0;
float nextTime = 0;

static unsigned long last_time_called=0;  //static is required here

void setup() {

myStepperFORWARD.setSpeed(60); //speed is in RPM;
myStepperLEFT.setSpeed(60);
Serial.begin(9600);
}

void serialFlushBuffer() {
  while (Serial.read() >= 0)
  ; // do nothing
}

void loop() {
  unsigned long now = millis();
  if (currTime > 0) {
    myStepperLEFT.step(-25000);
    currTime -= now - last_time_called;
    if (currTime < 0) {
      currTime = 0;
    }
  } else if (currTime < 0) {
    myStepperLEFT.step(25000);
    currTime += now - last_time_called;
    if (currTime > 0) {
      currTime = 0;
    }
  } else if (nextTime > 0) {
    myStepperFORWARD.step(-25000);
    nextTime -= now - last_time_called;
    if (nextTime < 0) {
      nextTime = 0;
    }
  } else if (nextTime < 0) {
    myStepperFORWARD.step(25000);
    nextTime += now - last_time_called;
    if (nextTime > 0) {
      nextTime = 0;
    }
  }

  if (Serial.available() > 0) {
    double angle = Serial.readStringUntil('\n').toDouble();
    float x = cos(angle);
    float y = sin(angle);
    prevRunning = true;
    currTime = x * 2000;
    nextTime = y * 2000;
    serialFlushBuffer();
  }

  if (currTime == 0 && nextTime == 0) {
    Serial.println("1");
  } else {
    Serial.println("2");
  }
  last_time_called = now;
}