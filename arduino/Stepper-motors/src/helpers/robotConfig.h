#ifndef ROBOT_CONFIG_H
#define ROBOT_CONFIG_H

#define LEFT_SIDE_PIN 8
#define RIGHT_SIDE_PIN 9
#define LEFT_SPEED_PIN 7
#define RIGHT_SPEED_PIN 12

#define ZERO_PACE 0
#define MAX_PACE 20000
#define MIN_PACE 500
#define DEFAULT_B_VALUE 100

#define I2C_ADDRESS 0x68

// TODO: right values
#define INCREMENTAL_ENCODER_LEFT_PIN_1 1
#define INCREMENTAL_ENCODER_LEFT_PIN_2 2
#define INCREMENTAL_ENCODER_RIGHT_PIN_1 3
#define INCREMENTAL_ENCODER_RIGHT_PIN_2 4

#define K_INC 0.000268
#define WIDTH 0.315

#define P_ROTATION_ERROR_COEFFICIENT 600
#define I_ROTATION_ERROR_COEFFICIENT 400
#define D_ROTATION_ERROR_COEFFICIENT 70

#define P_POSITION_ERROR_COEFFICIENT 5000
#define I_POSITION_ERROR_COEFFICIENT 1000
#define D_POSITION_ERROR_COEFFICIENT 600

#define KI_ROT_SAT 0.05
#define KI_POS_SAT 0.05

#endif