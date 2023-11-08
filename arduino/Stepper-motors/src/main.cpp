#include <Arduino.h>

#include "readingComponents/accelero.h"
#include "readingComponents/incrementalEncoder.h"
#include "movingComponents/stepperMotors.h"

void setup()

{
  setupMotors();
  setupAccelero();
  setupIncrementalEncoders();
  setLeftMotorSpeed(5000);
  setRightMotorSpeed(10000);
}

void loop()
{

}