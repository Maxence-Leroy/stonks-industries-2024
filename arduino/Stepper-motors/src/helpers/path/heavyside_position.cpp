#include <math.h>

#include "heavyside_position.h"

HeavysidePosition::HeavysidePosition(double xStart, double yStart, double xEnd, double yEnd,  double maxSpeed, double maxAcceleration):Path()
{
    mStart[X] = xStart;
    mStart[Y] = yStart;

    mEnd[X] = xEnd;
    mEnd[Y] = yEnd;

    mMaxSpeed = maxSpeed;
    mMaxAcceleration =  maxAcceleration;

    if(mMaxSpeed < 0) {
        mMaxSpeed = -mMaxSpeed;
        mGoingBackwards = true;
    }
    mExpectedDuration = 1;
}

HeavysidePosition::~HeavysidePosition(){}

String HeavysidePosition::debugString() 
{
  return String("Heavyside position");
}

double HeavysidePosition::positionError(double x, double y, Angle theta, long time)
{
  long ellapsedTime = time - mStartTime;
  if(ellapsedTime < 0)
  {
    double vectorX = cos(theta.toDouble());
    double vectorY = sin(theta.toDouble());
    double projectedX = (mStart[X]-x) * vectorX + (mStart[Y]-y) * vectorY;
    return projectedX;
  }
  else
  {
    double vectorX = cos(theta.toDouble());
    double vectorY = sin(theta.toDouble());
    double projectedX = (mEnd[X]-x)*vectorX+(mEnd[Y]-y)*vectorY;
    return projectedX;
  }
}

double HeavysidePosition::rotationError(double x, double y, Angle theta, long time)
{
  return (mTheta-theta).toDouble();
}