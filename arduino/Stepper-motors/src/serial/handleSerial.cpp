#include "handleSerial.h"
#include "../helpers/robotConfig.h"
#include "../movingComponents/stepperMotors.h"
#include "../movingComponents/enslavement.h"
#include "../movingComponents/pathQueue.h"
#include "../readingComponents/incrementalEncoder.h"
#include "../helpers/path/heavyside_position.h"
#include "../helpers/path/heavyside_rotation.h"
#include "../helpers/path/rotation.h"
#include "../helpers/path/stayOnPoint.h"

void extractCoordinates(String command, String coordinates[9]) {
    int coordinatesCount = 0;
    command.replace('(', ' ');
    command.replace(')', ' ');
    command.trim();
    while (command.length() > 0)
    {
        int index = command.indexOf(';');
        if (index == -1) // No space found
        {
            coordinates[coordinatesCount++] = command;
            break;
        }
        else
        {
            coordinates[coordinatesCount++] = command.substring(0, index);
            command = command.substring(index+1);
        }
    }
}

void handleInitialPosition(String command)
{
    if(LOGGING)
    {
        Serial.println("Init command");
    }
    command = command.substring(5); // Starts after "INIT "
    String coordinates[5];
    extractCoordinates(command, coordinates);
    double x = coordinates[0].toDouble();
    double y = coordinates[1].toDouble();
    Angle theta = Angle(coordinates[2].toDouble());
    setInitialPosition(x, y, theta);
    resetEncoders();
    setCurrentPath(new StayOnPoint(x, y, theta));
    getCurrentPath()->start();
}

void handleDestination(String destinationString)
{
    if(LOGGING)
    {
        Serial.print("destination string ");
        Serial.println(destinationString);
    }
    String coordinates[9];
    extractCoordinates(destinationString, coordinates);
    Destination* destination = new Destination(
        coordinates[0].toDouble(),
        coordinates[1].toDouble(),
        Angle(coordinates[2].toDouble()),
        coordinates[3].toInt() == 1,
        coordinates[4].toInt() == 1,
        coordinates[5].toInt() == 1,
        coordinates[6].toInt(),
        coordinates[7].toInt(),
        coordinates[8].toInt() == 1
    );
    addDestination(destination);
}

void handleMoveCommand(String command)
{
    if(LOGGING)
    {
        Serial.println("Move command");
    }
    while (command.length() > 0)
    {
        int index = command.indexOf(',');
        if (index == -1) // No space found
        {
            handleDestination(command);
            break;
        }
        else
        {
            handleDestination(command.substring(0, index));
            command = command.substring(index+1);
        }
    }
}

void handleStopCommand()
{
    if(LOGGING)
    {
        Serial.println("Stop command");
    }
    stopMotors();
    clearQueue();
    setCurrentPath(new StayOnPoint(getCurrentX(), getCurrentY(), getCurrentTheta()));
}

void handlePIDCommand(String command)
{
    command = command.substring(4);
    float number = command.substring(6).toFloat();
    String variable = command.substring(0,5);
    if(variable.equals("P_POS")) 
    {
        setPPos(number);
    }
    else if(variable.equals("I_POS"))
    {
        setIPos(number);
    }
    else if(variable.equals("D_POS"))
    {
        setDPos(number);
    }
    else if(variable.equals("P_ROT"))
    {
        setPRot(number);
    }
    else if(variable.equals("I_ROT"))
    {
        setIRot(number);
    }
    else if(variable.equals("D_ROT"))
    {
        setDRot(number);
    }
    else
    {
        if(LOGGING)
        {
            Serial.println(variable);
            Serial.println("Can not parse PID command");
        }
    }
}

void handleHeavysideCommand(String command)
{
    command = command.substring(3);
    setInitialPosition(0, 0, 0);
    Path* path;
    if(command.equals("ROT"))
    {
        path = new HeavysideRotation(0, 0, 0, M_PI_4 / 2, 2, 2);
    }
    else if(command.equals("POS"))
    {
        path = new HeavysidePosition(0, 0, 100, 0, 750, 500);
    }
    else
    {
        if(LOGGING)
        {
            Serial.println("Can not parse HS command");
        }
    }
    path->start();
    setCurrentPath(path);
}