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

const double maxSpeedLine = 450;
const double maxAccelerationLine = 1100;
const double maxSpeedRotation = 3;
const double maxAccelerationRotation = 6;

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
    bool onTheSpot = nextDestination->onTheSpot;
    int maxSpeed = nextDestination->maxSpeed;
    int maxAcceleration = nextDestination->maxAcceleration;
    bool precision = nextDestination->precision;
    
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
        Serial.print(";");
        Serial.print(onTheSpot);
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

    if((fabs(x - currentX) > 5 || fabs(y - currentY) > 5) && !onTheSpot)
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
            queue->add(new Rotation(currentX, currentY, currentTheta, requiredTheta, maxSpeed / 100.0 * maxSpeedRotation, maxAcceleration / 100.0 * maxAccelerationRotation, precision));
        }
        if(LOGGING)
        {
            Serial.println("New line");
        }
        queue->add(new Line(currentX, currentY, x, y, maxSpeed / 100.0 * (backwards ? -maxSpeedLine : maxSpeedLine), maxAcceleration / 100.0 * maxAccelerationLine, precision));
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
        double xRotation, yRotation;
        if(onTheSpot) {
            xRotation = currentX;
            yRotation = currentY;
        } else {
            xRotation = x;
            yRotation = y;
        }
        queue->add(new Rotation(xRotation, yRotation, requiredTheta, theta, maxSpeed / 100.0 * maxSpeedRotation, maxAcceleration / 100.0 * maxAccelerationRotation, precision));
    }
    return true;
}

Path* getNextPath()
{
    return queue->pop();
}

void clearQueue() {
    while(!queue->isEmpty()) {
        queue->pop();
    }
}