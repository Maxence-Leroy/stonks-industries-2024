#include <Arduino.h>

#include "helpers/path/line.h"
#include "helpers/path/rotation.h"
#include "readingComponents/accelero.h"
#include "readingComponents/incrementalEncoder.h"
#include "movingComponents/enslavement.h"
#include "movingComponents/pathQueue.h"
#include "movingComponents/stepperMotors.h"
#include "serial/handleSerial.h"

Path* path;
String command;

void setup()
{
  Serial2.begin(115200); // Connection with the potato

  setupMotors();
  setupAccelero();
  setupIncrementalEncoders();
  setInitialPosition(0, 0, Angle(0));
}

void loop()
{
  if(Serial2.available() > 0) 
  {
    command = Serial2.readStringUntil('\n');
    if(command.startsWith("INIT")) 
    {
      handleInitialPosition(command);
    }
    else if(command == "STOP") {
      handleStopCommand();
    }
    else 
    {
      handleMoveCommand(command);
    }
  }
  long currentTime = micros();
  enslave(currentTime);

  if(getCurrentPath()->isOver(currentTime))
  {
    Path* nextPath = getNextPath();
    if(!nextPath)
    {
      nextPath->start();
      setCurrentPath(nextPath);
    } else {
      Serial2.println("DONE");
    }
  }

}