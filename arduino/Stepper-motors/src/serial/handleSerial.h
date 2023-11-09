#ifndef HANDLE_SERIAL_H
#define HANDLE_SERIAL_H

#include <Arduino.h>

void handleInitialPosition(String command);
void handleMoveCommand(String command);
void handleStopCommand();

#endif