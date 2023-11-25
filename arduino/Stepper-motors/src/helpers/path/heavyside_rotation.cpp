#include <Arduino.h>
#include <math.h>

#include "../maths_helpers.h"
#include "heavyside_rotation.h"

HeavysideRotation::HeavysideRotation(double x, double y, Angle startTheta, Angle endTheta, double maxSpeed, double maxAcceleration):Path()
{
  mX = x;
  mY = y;
  mStartTheta = startTheta;
  mEndTheta = endTheta;
  mMaxSpeed = maxSpeed;
  mMaxAcceleration = maxAcceleration;

  if((mEndTheta-mStartTheta).toDouble()<0)
    mDirection = A_TRIGO_DIRECTION;
  else
    mDirection = TRIGO_DIRECTION;

  mExpectedDuration = 1;
}

HeavysideRotation::~HeavysideRotation(){}

String HeavysideRotation::debugString() 
{
  return String("Heavyside rotation");
}

double HeavysideRotation::positionError(double x, double y, Angle theta, long time)
{
  double vector[2] = {cos(theta.toDouble()), sin(theta.toDouble())};
  double projectedX = (mX-x)*vector[X]+(mY-y)*vector[Y];
  return projectedX;
}

double HeavysideRotation::rotationError(double x, double y, Angle theta, long time)
{
  long ellapsedTime = time - mStartTime;
  if(ellapsedTime < 0)
  {
    return (mStartTheta-theta).toDouble();
  }
  else
  {
    return (mEndTheta-theta).toDouble();
  }
}



