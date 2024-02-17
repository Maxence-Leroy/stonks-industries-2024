#include <Arduino.h>
#include <math.h>

#include "../maths_helpers.h"
#include "stayOnPoint.h"

StayOnPoint::StayOnPoint(double x, double y, Angle theta):Path()
{
  mX = x;
  mY = y;
  mTheta = theta;
  mExpectedDuration = 0;
}

StayOnPoint::~StayOnPoint(){}

bool StayOnPoint::sendDone() const {
    return false;
}

String StayOnPoint::debugString() 
{
  return String("Stay on currentPoint");
}

double StayOnPoint::positionError(double x, double y, Angle theta, long time)
{
  double vector[2] = {cos(theta.toDouble()), sin(theta.toDouble())};
  double projectedX = (mX-x)*vector[X]+(mY-y)*vector[Y];
  return projectedX;
}

double StayOnPoint::rotationError(double x, double y, Angle theta, long time)
{
    return (mTheta-theta).toDouble();
}



