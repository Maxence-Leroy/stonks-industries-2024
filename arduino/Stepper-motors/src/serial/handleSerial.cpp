#include "handleSerial.h"
#include "../movingComponents/stepperMotors.h"
#include "../movingComponents/enslavement.h"
#include "../movingComponents/pathQueue.h"

String* extractCoordinates(String command) {
    int coordinatesCount = 0;
    String coordinates[3];
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
    return coordinates;
}

void handleInitialPosition(String command)
{
    command = command.substring(5); // Starts after "INIT "

    String* coordinates = extractCoordinates(command);
    setInitialPosition(coordinates[0].toDouble(), coordinates[1].toDouble(), Angle(coordinates[2].toDouble()));
}

void handleMoveCommand(String command)
{
    String* coordinates = extractCoordinates(command);
    addDestination(coordinates[0].toDouble(), coordinates[1].toDouble(), Angle(coordinates[2].toDouble()));
}

void handleStopCommand()
{
    stopMotors();
}