#include <Arduino.h>
#include <math.h>

#include "enslavement.h"
#include "../readingComponents/incrementalEncoder.h"
#include "../helpers/robotConfig.h"
#include "../helpers/maths_helpers.h"
#include "stepperMotors.h"

double currentX = 0, currentY = 0;
Angle currentTheta = Angle(0);
int32_t incrementalCounterLeft = 0, incrementalCounterRight = 0;
long int previousTime = 0, previousPositionPrint = 0;

double rotationError[3] = {0, 0, 0};
double positionError[3] = {0, 0, 0};

Path* currentPath;

void setInitialPosition(double x, double y, Angle theta) {
    currentX = x;
    currentY = y;
    currentTheta = theta;

    rotationError[D] = 0;
    rotationError[P] = 0;
    rotationError[I] = 0;

    positionError[D] = 0;
    positionError[P] = 0;
    positionError[I] = 0;
}

void setCurrentPath(Path* path) {
    currentPath = path;
}

void enslave(long time) {
    int32_t newIncrementalLeft = getIncrementalEncoderLeftValue();
    int32_t newIncrementalRight = getIncrementalEncoderRightValue(); 

    currentX += cos(currentTheta.toDouble())*(newIncrementalRight+newIncrementalLeft-incrementalCounterLeft-incrementalCounterRight)*K_INC/2;
    currentY += sin(currentTheta.toDouble())*(newIncrementalRight+newIncrementalLeft-incrementalCounterLeft-incrementalCounterRight)*K_INC/2;
    currentTheta = Angle(currentTheta.toDouble() + atan((newIncrementalRight-newIncrementalLeft-incrementalCounterRight+incrementalCounterLeft)*K_INC/WIDTH));
    incrementalCounterLeft = newIncrementalLeft;
    incrementalCounterRight = newIncrementalRight;

    if(time - previousPositionPrint > 0.5 * SEC_TO_MICROS_MULTIPLICATOR)
    {
        Serial2.print("(");
        Serial2.print(currentX);
        Serial2.print(";");
        Serial2.print(currentY);
        Serial2.print(";");
        Serial2.print(currentTheta.toDouble());
        Serial2.println(")");
        previousPositionPrint = time;
    }

    if(currentPath->isGoingBackwards())
    {
        currentTheta = currentTheta +Angle(M_PI);
    }

    double currentPositionError = currentPath->positionError(currentX, currentY, currentTheta, time);
    double currentRotationError = currentPath->rotationError(currentX, currentY, currentTheta, time);

    double elapsedTimeInS = (time - previousTime) * MICROS_TO_SEC_MULTIPLICATOR;

    // Compute PID
    positionError[D] = (currentPositionError-positionError[P])/elapsedTimeInS;
    positionError[P] = currentPositionError;
    positionError[I] += positionError[P]*elapsedTimeInS;
    if(fabs(positionError[I])>KI_POS_SAT)
        positionError[I]=KI_POS_SAT*fabs(positionError[I])/positionError[I];

    rotationError[D] = (currentRotationError-rotationError[P])/elapsedTimeInS;
    rotationError[P] = currentRotationError;
    rotationError[I] += rotationError[P]*elapsedTimeInS;
    if(fabs(rotationError[I])>KI_ROT_SAT)
        rotationError[I]=KI_ROT_SAT*fabs(rotationError[I])/rotationError[I];

    // Then we enslave
    int orderR = rotationError[P] * P_ROTATION_ERROR_COEFFICIENT
                + rotationError[I] * I_ROTATION_ERROR_COEFFICIENT
                + rotationError[D] * D_ROTATION_ERROR_COEFFICIENT;

    int orderP = positionError[P] * P_POSITION_ERROR_COEFFICIENT
                + positionError[I] * I_POSITION_ERROR_COEFFICIENT
                + positionError[D] * D_POSITION_ERROR_COEFFICIENT;
 
    if(!currentPath->isGoingBackwards())
    {
        setLeftMotorSpeed(+orderP - orderR);
        setRightMotorSpeed(+orderP + orderR);
    }
    else
    {
        setLeftMotorSpeed(-orderP - orderR);
        setRightMotorSpeed(-orderP + orderR);
        currentTheta = currentTheta+Angle(M_PI);
    }

    previousTime=time;

}

const double getCurrentX()
{
    return currentX;
}

const double getCurrentY()
{
    return currentY;
}

const Angle getCurrentTheta()
{
    return currentTheta;
}

const Path* getCurrentPath() {
    return currentPath;
}