#ifndef ROBOT_CONFIG_H
#define ROBOT_CONFIG_H

#define LEFT_SIDE_PIN 8
#define RIGHT_SIDE_PIN 9
#define LEFT_SPEED_PIN 7
#define RIGHT_SPEED_PIN 12

#define ZERO_PACE 0
#define MAX_PACE 6000000
#define MIN_PACE 500
#define DEFAULT_B_VALUE 100

#define I2C_ADDRESS 0x68

#define INCREMENTAL_ENCODER_LEFT_PIN_1 2
#define INCREMENTAL_ENCODER_LEFT_PIN_2 3
#define INCREMENTAL_ENCODER_RIGHT_PIN_1 19
#define INCREMENTAL_ENCODER_RIGHT_PIN_2 18

#define K_INC 0.26609898882
#define WIDTH 220

#define P_ROTATION_ERROR_COEFFICIENT 300
#define I_ROTATION_ERROR_COEFFICIENT 300
#define D_ROTATION_ERROR_COEFFICIENT 0

#define P_POSITION_ERROR_COEFFICIENT 3.2
#define I_POSITION_ERROR_COEFFICIENT 12.5
#define D_POSITION_ERROR_COEFFICIENT 0

#define KI_ROT_SAT 0.05
#define KI_POS_SAT 0.05

#define LOGGING true

#endif