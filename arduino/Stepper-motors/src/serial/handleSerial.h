#ifndef HANDLE_SERIAL_H
#define HANDLE_SERIAL_H

#include <Arduino.h>

void extractCoordinates(String command, String coordinates[4]);
void handleInitialPosition(String command);
void handleStopCommand();

#endif