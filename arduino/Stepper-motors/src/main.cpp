#include <Arduino.h>

#include "accelero.h"
#include "stepperMotors.h"

void setup()

{
  setupMotors();
  setupAccelero();
  setLeftMotorSpeed(5000);
  setRightMotorSpeed(10000);
}

void loop()
{

}