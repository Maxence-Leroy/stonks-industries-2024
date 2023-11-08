#include <math.h>

#include "line.h"

Line::Line(double xStart, double yStart, double xEnd, double yEnd,  double maxSpeed, double maxAcceleration):Path()
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

    double distance = sqrt(
        pow(mStart[X]-mEnd[X], 2) + 
        pow(mStart[Y]-mEnd[Y], 2)
    );

    double accelerationTime = mMaxSpeed / mMaxAcceleration;
    double accelerationDistance =  0.5 * pow(accelerationTime, 2) * mMaxAcceleration;

    if(distance == 0)
    {
        mVector[X]=1;
        mVector[Y]=0;
        mTheta = 0;
    }
    else
    {
        mVector[X] = (mEnd[X]-mStart[X]) / distance;
        mVector[Y] = (mEnd[Y]-mStart[Y]) / distance;

        mTheta = acos(mVector[X]);

        if(mVector[Y]<0)
            mTheta = -mTheta.toDouble()+2* M_PI;

        if(2 * accelerationDistance > distance)
        {
            // Short distance, we don't have time to reach full speed
            mDistanceForAcceleration = distance / 2;
            mDistanceWithConstantSpeed = 0;
            accelerationTime = sqrt(2 * mDistanceForAcceleration / mMaxAcceleration);

            mEndAccelerationTime = accelerationTime * SEC_TO_MICROS_MULTIPLICATOR;
            mStartDeccelerationTime = mEndAccelerationTime + 0;
            mExpectedDuration = 2 * mEndAccelerationTime;
        }
        else
        {
            // Long distance, we will reach full speed
            mDistanceForAcceleration = accelerationDistance;
            mDistanceWithConstantSpeed = distance - 2 * accelerationDistance;

            mEndAccelerationTime =  accelerationTime * SEC_TO_MICROS_MULTIPLICATOR;
            mStartDeccelerationTime = mEndAccelerationTime + mDistanceWithConstantSpeed / mMaxSpeed * SEC_TO_MICROS_MULTIPLICATOR;
            mExpectedDuration = mStartDeccelerationTime + accelerationTime * SEC_TO_MICROS_MULTIPLICATOR;
        }
  }
}

Line::~Line(){}

double Line::positionError(double x, double y, Angle theta, long time)
{
  long ellapsedTime = time - mStartTime;

  // We use a base where vector X is colinear to the path
  double projectedX = (x-mStart[X])*mVector[X]+(y-mStart[Y])*mVector[Y];

  if(ellapsedTime < 0)
  {
    double vectorX = cos(theta.toDouble());
    double vectorY = sin(theta.toDouble());
    projectedX = (mStart[X]-x) * vectorX + (mStart[Y]-y) * vectorY;
    return projectedX;
  }
  else if(0 < ellapsedTime && ellapsedTime < mEndAccelerationTime)
  {
    double x = 0.5*mMaxAcceleration*pow((ellapsedTime) * MICROS_TO_SEC_MULTIPLICATOR, 2);
    return x-projectedX;
  }
  else if(mEndAccelerationTime < ellapsedTime && ellapsedTime < mStartDeccelerationTime)
  {
    double x = mDistanceForAcceleration + (ellapsedTime- mEndAccelerationTime)* MICROS_TO_SEC_MULTIPLICATOR * mMaxSpeed;
    return x-projectedX;
  }
  else if(mStartDeccelerationTime < ellapsedTime && ellapsedTime < mExpectedDuration)
  {
    double x = 2 * mDistanceForAcceleration
        + mDistanceWithConstantSpeed 
        - 0.5 * mMaxAcceleration *pow((mExpectedDuration-ellapsedTime)* MICROS_TO_SEC_MULTIPLICATOR, 2);

    return x-projectedX;
  }
  else
  {
    double vectorX = cos(theta.toDouble());
    double vectorY = sin(theta.toDouble());
    projectedX = (mEnd[X]-x)*vectorX+(mEnd[Y]-y)*vectorY;
    return projectedX;
  }
}

double Line::rotationError(double x, double y, Angle theta, long time)
{
  long ellaspedTime = time - mStartTime;
  // We project on the path line
  double projectedY = -(x-mStart[X])*mVector[Y]+(y-mStart[Y])*mVector[X];

  if(ellaspedTime < 0)
  {
    return (mTheta-theta).toDouble();
  }
  else if(0 < ellaspedTime && ellaspedTime < mEndAccelerationTime)
  {
    return (Angle(-projectedY)-(theta-mTheta)).toDouble()*ellaspedTime* MICROS_TO_SEC_MULTIPLICATOR * mMaxAcceleration * 10;
  }
  else if(mEndAccelerationTime < ellaspedTime && ellaspedTime < mStartDeccelerationTime)
  {
    return (Angle(-projectedY)-(theta-mTheta)).toDouble()* mMaxSpeed * 10;
  }
  else if(mStartDeccelerationTime < ellaspedTime && ellaspedTime < mExpectedDuration)
  {
    return (Angle(-projectedY)-(theta-mTheta)).toDouble()*SEC_TO_MICROS_MULTIPLICATOR*(mExpectedDuration-ellaspedTime)*mMaxAcceleration*10;
  }
  else
  {
    return (mTheta-theta).toDouble();
  }
}