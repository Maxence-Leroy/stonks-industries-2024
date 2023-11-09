#ifndef STEPPER_MOTORS_H
#define STEPPER_MOTORS_H

#include <stdint.h>

void setupMotors();
void setLeftMotorSpeed(double speed);
void setRightMotorSpeed(double speed);
void stopMotors();

#endif