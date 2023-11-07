#ifndef STEPPER_MOTORS_H
#define STEPPER_MOTORS_H

#include <stdint.h>

void setupMotors();
void setLeftMotorSpeed(int32_t speed);
void setRightMotorSpeed(int32_t speed);

#endif