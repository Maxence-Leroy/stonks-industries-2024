#include <Arduino.h>

#include "path.h"

Path::Path() 
{

}

Path::~Path()
{
    
}

double Path::positionError(double x, double y, Angle theta, long time) 
{
    return 0;
}

double Path::rotationError(double x, double y, Angle theta, long time) 
{
    return 0;
}

String Path::debugString() 
{
    return "";
}

bool Path::isGoingBackwards() const 
{
    return mGoingBackwards;
}

void Path::start()
{
	mStartTime=micros();
}

bool Path::isOver(long time) const
{
    long ellapsedTime = time - mStartTime;
    return (ellapsedTime > mExpectedDuration || mExpectedDuration == 0);
}

bool Path::sendDone() const {
    return true;
}