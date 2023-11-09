#include <Arduino.h>
#include <math.h>
#include "../helpers/queue.h"
#include "../helpers/path/line.h"
#include "../helpers/path/rotation.h"
#include "enslavement.h"

#include "pathQueue.h"

Queue<Path>* queue = new Queue<Path>();

const double maxSpeed = 500;
const double maxAcceleration = 500;

void addDestination(double x, double y, Angle theta, bool backwards)
{
    double currentX = getCurrentX();
    double currentY = getCurrentY();
    Angle currentTheta = getCurrentTheta();

    if(fabs(x - currentX) > 0.5 || fabs(y - currentY) > 0.5) 
    {
        Serial.println("New line");
        queue->add(new Line(currentX, currentY, x, y, backwards ? -maxSpeed : maxSpeed, maxAcceleration));
    }

    if(fabs((currentTheta - theta).toDouble() > 0.05)) 
    {
        queue->add(new Rotation(x, y, currentTheta, theta, maxSpeed, maxAcceleration));
    }
}

Path* getNextPath()
{
    return queue->pop();
}