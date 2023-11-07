#include <Arduino.h>

#include "stepperMotors.h"

void setup()

{
  setupMotors();
  setLeftMotorSpeed(5000);
  setRightMotorSpeed(10000);
}

void loop()
{

}