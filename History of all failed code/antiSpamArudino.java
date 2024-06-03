#include <Stepper.h>

const float STEPS_PER_REV = 32;
const float GEAR_RED = 64;
const int stepsPerRevolution = 25000;
bool sentBefore = false;
bool prevState = 1; // If the previous state was that it wasn't moving: 1; If the previous state was that it was moving: 2

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

void loop() {
  unsigned long now = millis();
  // CONTROLLING MOTORS CODE
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
  // READ FROM INPUT BUFFER
  if (Serial.available() > 0) {
    double angle = Serial.readStringUntil('\n').toDouble();
    float x = cos(angle);
    float y = sin(angle);
    currTime = x * 2000;
    nextTime = y * 2000;
  }

  if (currTime == 0 && nextTime == 0 && sentBefore == false) {
    Serial.println("1"); // Tell Raspberry pi we are ready to get sent another angle.
    sentBefore = true;   // Ok, we sent a message now we should stop sending messages
    prevState = 1;       // In order to know when we switch states, we document that we were avaiable for awhile.
  } 
  if (currTime != 0 || nextTime != 0 && sentBefore == false) {
      Serial.println("2"); // Tell Raspberry pi we are now busy.
      sentBefore = true;   // Ok, we sent a message now we should stop sending messages
      prevState = 2;       // In order to know when we switch states, we document that we were busy for awhile.
  }
  if ((prevState == 1 && currTime != 0 || nextTime != 0) || (prevState == 2 && currTime == 0 && nextTime == 0)) {
      sentBefore = false; // When we switch stages, we are able to send another message.
  }
  last_time_called = now;
}