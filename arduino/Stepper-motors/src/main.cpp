#include <Arduino.h>

#include "helpers/robotConfig.h"
#include "readingComponents/accelero.h"
#include "readingComponents/incrementalEncoder.h"
#include "movingComponents/enslavement.h"
#include "movingComponents/stepperMotors.h"
#include "serial/handleSerial.h"

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
      String coordinates[4];
      extractCoordinates(command, coordinates);
      enslave(coordinates[0].toDouble(), coordinates[1].toDouble(), Angle(coordinates[2].toDouble()), coordinates[3].toInt() == 1);
    }
  }
}