#include "handleSerial.h"
#include "../movingComponents/stepperMotors.h"
#include "../movingComponents/enslavement.h"
#include "../movingComponents/pathQueue.h"

void extractCoordinates(String command, String coordinates[3]) {
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
    command = command.substring(5); // Starts after "INIT "
    String coordinates[3];
    extractCoordinates(command, coordinates);
    setInitialPosition(coordinates[0].toDouble(), coordinates[1].toDouble(), Angle(coordinates[2].toDouble()));
}

void handleMoveCommand(String command)
{
    String coordinates[3];
    extractCoordinates(command, coordinates);
    addDestination(coordinates[0].toDouble(), coordinates[1].toDouble(), Angle(coordinates[2].toDouble()));
}

void handleStopCommand()
{
    stopMotors();
}