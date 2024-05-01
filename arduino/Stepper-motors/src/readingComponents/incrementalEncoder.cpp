#include <Arduino.h>

#include "incrementalEncoder.h"
#include "AS5048A.h"
#include "../helpers/robotConfig.h"

int64_t leftValue = 0;
int64_t rightValue = 0;

int16_t previousLeftAngle = 0;
int16_t previousRightAngle = 0;

AS5048A rightEncoder(INCREMENTAL_ENCODER_RIGHT_PIN, false);
AS5048A leftEncoder(INCREMENTAL_ENCODER_LEFT_PIN, false);

const int64_t getIncrementalEncoderLeftValue() {
    return leftValue;
}

const int64_t getIncrementalEncoderRightValue() 
{
    return rightValue;
}

void updateIncrementalEncodersValue() {
    int16_t leftAngle = leftEncoder.getRotation();

    if(previousLeftAngle < -AS5048A_MAX_VALUE / 2 && leftAngle > AS5048A_MAX_VALUE / 2) {
        // The new rotation should be negative
        leftValue -= leftAngle - 2 * AS5048A_MAX_VALUE - previousLeftAngle;
    } else if(previousLeftAngle > AS5048A_MAX_VALUE / 2 && leftAngle < - AS5048A_MAX_VALUE / 2) {
        // The new rotation should be positive
        leftValue -= leftAngle + 2 * AS5048A_MAX_VALUE - previousLeftAngle;
    } else {
        leftValue -= leftAngle - previousLeftAngle;
    }

    previousLeftAngle = leftAngle;


    int16_t rightAngle = rightEncoder.getRotation();

    if(previousRightAngle < -AS5048A_MAX_VALUE / 2 && rightAngle > AS5048A_MAX_VALUE / 2) {
        // The new rotation should be negative
        rightValue += rightAngle - 2 * AS5048A_MAX_VALUE - previousRightAngle;
    } else if(previousRightAngle > AS5048A_MAX_VALUE / 2 && rightAngle < - AS5048A_MAX_VALUE / 2) {
        // The new rotation should be positive
        rightValue += rightAngle + 2 * AS5048A_MAX_VALUE - previousRightAngle;
    } else {
        rightValue += rightAngle - previousRightAngle;
    }

    previousRightAngle = rightAngle;
}

void setupIncrementalEncoders()
{
    rightEncoder.begin();
    leftEncoder.begin();

    resetEncoders();
}

void resetEncoders() {
    previousRightAngle = rightEncoder.getRotation();
    previousLeftAngle = leftEncoder.getRotation();
}