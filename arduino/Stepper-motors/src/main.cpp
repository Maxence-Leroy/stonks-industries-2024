#include <Arduino.h>

#include "helpers/robotConfig.h"
#include "helpers/path/line.h"
#include "helpers/path/rotation.h"
#include "helpers/path/stayOnPoint.h"
#include "readingComponents/incrementalEncoder.h"
#include "movingComponents/enslavement.h"
#include "movingComponents/pathQueue.h"
#include "movingComponents/stepperMotors.h"
#include "serial/handleSerial.h"

Path* path;
String command;

bool hasSentDone = false;
bool hasChangedPath = false;

void setup()
{
  Serial.begin(9600);
  if(LOGGING)
  {
    Serial.println("Setup robot");
  }
  Serial2.begin(115200); // Connection with the potato
  setupMotors();
  setupIncrementalEncoders();
  setInitialPosition(0, 0, Angle(0));
  setCurrentPath(new StayOnPoint(0, 0, 0));
  getCurrentPath()->start();
  setLeftMotorSpeed(0);
  setRightMotorSpeed(0);
  if(LOGGING)
  {
    Serial.println("End setup");
  }
}

void loop()
{
  if(Serial2.available() > 0) 
  {
    command = Serial2.readStringUntil('\n');
    if(LOGGING)
    {
      Serial.print("command: ");
      Serial.println(command);
    }
    if(command.startsWith("INIT")) 
    {
      handleInitialPosition(command);
    }
    else if(command.startsWith("PID"))
    {
      handlePIDCommand(command);
    }
    else if(command.startsWith("HS"))
    {
      handleHeavysideCommand(command);
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
  if(getCurrentPath())
  {
    enslave(currentTime);
  }

  Path* currentPath = getCurrentPath();
  double positionError = currentPath->positionError(getCurrentX(), getCurrentY(), getCurrentTheta(), currentTime);
  double rotationError = currentPath->rotationError(getCurrentX(), getCurrentY(), getCurrentTheta(), currentTime);
  if(currentPath->isOver(currentTime) && abs(positionError) < 3 && abs(rotationError) < 0.01)
  {
    Path* nextPath = getNextPath();
    if(nextPath)
    {
      if(LOGGING)
      {
        Serial.println("Use next path");
        Serial.println(nextPath->debugString());
      }
      nextPath->start();
      hasSentDone = false;
      setCurrentPath(nextPath);
    } 
    else if(getCurrentPath())
    {
      bool hasOtherPath = extractNextDestination();
      if(!hasOtherPath && !hasSentDone) {
        if(LOGGING)
        {
          Serial.println("Done moving");
        }
        if(currentPath->sendDone()) {
          Serial2.print("DONE\n");
        }
        hasSentDone = true;
      } 
    } else {
      extractNextDestination();
    }
  }
}