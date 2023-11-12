#include <Arduino.h>

#include "helpers/robotConfig.h"
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

bool firstTime = true;

void setup()
{
  if(LOGGING)
  {
    Serial.begin(9600);
    Serial.println("Setup robot");
  }
  Serial2.begin(115200); // Connection with the potato

  setupMotors();
  setupAccelero();
  setupIncrementalEncoders();
  setInitialPosition(0, 0, Angle(0));
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

  if(!getCurrentPath() || getCurrentPath()->isOver(currentTime))
  {
    Path* nextPath = getNextPath();
    if(nextPath)
    {
      if(LOGGING)
      {
        Serial.println("Use next path");
      }
      nextPath->start();
      setCurrentPath(nextPath);
    } 
    else if(getCurrentPath())
    {
      stopMotors();
      setCurrentPath(nullptr);
      if(LOGGING)
      {
        Serial.println("Done moving");
      }
      Serial2.print("DONE\n");
    }
  }
}