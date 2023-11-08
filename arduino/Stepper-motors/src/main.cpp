#include <Arduino.h>

#include "readingComponents/accelero.h"
#include "movingComponents/stepperMotors.h"

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