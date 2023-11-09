#include <Arduino.h>

#include "helpers/path/line.h"
#include "helpers/path/rotation.h"
#include "readingComponents/accelero.h"
#include "readingComponents/incrementalEncoder.h"
#include "movingComponents/enslavement.h"
#include "movingComponents/stepperMotors.h"

Path* path;

void setup()
{
  setupMotors();
  setupAccelero();
  setupIncrementalEncoders();
  setInitialPosition(0, 0, Angle(0));
  // path = new Rotation(0, 0, Angle(0), Angle(M_PI / 2), 100, 100);
  path = new Line(0, 0, 100, 0, 10, 1);
  setCurrentPath(path);
  path->start();
}

void loop()
{
  enslave(micros());
}