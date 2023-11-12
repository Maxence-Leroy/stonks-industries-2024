#include <Arduino.h>
#include <math.h>
#include "../helpers/queue.h"
#include "../helpers/robotConfig.h"
#include "../helpers/path/line.h"
#include "../helpers/path/rotation.h"
#include "enslavement.h"

#include "pathQueue.h"

Queue<Path>* queue = new Queue<Path>();

const double maxSpeed = 500;
const double maxAcceleration = 500;
const double maxSpeedRotation = 2;
const double maxAccelerationRotation = 2;

void addDestination(double x, double y, Angle theta, bool backwards, bool forcedAngle)
{
    if(LOGGING)
    {
        Serial.print("Destination: (");
        Serial.print(x);
        Serial.print(";");
        Serial.print(y);
        Serial.print(";");
        Serial.print(theta.toDouble());
        Serial.print(";");
        Serial.print(backwards);
        Serial.print(";");
        Serial.print(forcedAngle);
        Serial.println(")");
    }
    double currentX = getCurrentX();
    double currentY = getCurrentY();
    Angle currentTheta = getCurrentTheta();

    Angle requiredTheta = currentTheta;

    if(fabs(x - currentX) > 0.5 || fabs(y - currentY) > 0.5) 
    {
        requiredTheta = Angle::computeAngle(currentX, currentY, x, y);
        if(backwards)
        {
            requiredTheta += M_PI;
        }
        if(fabs((requiredTheta - currentTheta).toDouble()))
        {
            if(LOGGING)
            {
                Serial.print("New rotation to ");
                Serial.println(requiredTheta.toDouble());
            }
            queue->add(new Rotation(currentX, currentY, currentTheta, requiredTheta, maxSpeedRotation, maxAccelerationRotation));
        }
        if(LOGGING)
        {
            Serial.println("New line");
        }
        queue->add(new Line(currentX, currentY, x, y, backwards ? -maxSpeed : maxSpeed, maxAcceleration));
        if(backwards)
        {
            requiredTheta -= M_PI;
        }
    }

    if(fabs((currentTheta - theta).toDouble()) > 0.05 && forcedAngle) 
    {
        if(LOGGING)
        {
            Serial.println("New rotation");
        }
        queue->add(new Rotation(x, y, requiredTheta, theta, maxSpeedRotation, maxAccelerationRotation));
    }
}

Path* getNextPath()
{
    return queue->pop();
}