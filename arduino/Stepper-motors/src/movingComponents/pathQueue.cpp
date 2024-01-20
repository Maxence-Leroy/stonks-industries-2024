#include <Arduino.h>
#include <math.h>
#include "../helpers/queue.h"
#include "../helpers/robotConfig.h"
#include "../helpers/path/line.h"
#include "../helpers/path/rotation.h"
#include "enslavement.h"

#include "pathQueue.h"

Queue<Path>* queue = new Queue<Path>();
Queue<Destination>* destinationQueue = new Queue<Destination>();

const double maxSpeed = 375;
const double maxAcceleration = 250;
const double maxSpeedRotation = 2;
const double maxAccelerationRotation = 2;

void addDestination(Destination* destination)
{
    destinationQueue->add(destination);
    if(LOGGING)
    {
        Serial.println("Add destination");
    }
}

bool extractNextDestination()
{
    Destination* nextDestination = destinationQueue->pop();
    if(!nextDestination) {
        return false;
    }
    double x = nextDestination->x;
    double y = nextDestination->y;
    Angle theta = nextDestination->theta;
    bool backwards = nextDestination->backwards;
    bool forcedAngle = nextDestination->forcedAngle;
    
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

    if(LOGGING)
    {
        Serial.print("Current position: (");
        Serial.print(currentX);
        Serial.print(";");
        Serial.print(currentY);
        Serial.print(";");
        Serial.print(currentTheta.toDouble());
        Serial.println(")");
    }

    Angle requiredTheta = currentTheta;

    if(fabs(x - currentX) > 5 || fabs(y - currentY) > 5) 
    {
        requiredTheta = Angle::computeAngle(currentX, currentY, x, y);
        if(backwards)
        {
            requiredTheta += M_PI;
        }
        if(fabs((requiredTheta - currentTheta).toDouble()) > 0.1)
        {
            if(LOGGING)
            {
                Serial.print("New rotation from ");
                Serial.print(currentTheta.toDouble());
                Serial.print(" to ");
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
    return true;
}

Path* getNextPath()
{
    return queue->pop();
}