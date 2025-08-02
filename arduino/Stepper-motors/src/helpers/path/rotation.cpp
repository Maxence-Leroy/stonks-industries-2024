#include <Arduino.h>
#include <math.h>

#include "../maths_helpers.h"
#include "rotation.h"

Rotation::Rotation(double x, double y, Angle startTheta, Angle endTheta, double maxSpeed, double maxAcceleration, bool precision):Path()
{
  mX = x;
  mY = y;
  mStartTheta = startTheta;
  mEndTheta = endTheta;
  mMaxSpeed = maxSpeed;
  mMaxAcceleration = maxAcceleration;
  mPrecision = precision;

  if((mEndTheta-mStartTheta).toDouble()<0)
    mDirection = A_TRIGO_DIRECTION;
  else
    mDirection = TRIGO_DIRECTION;

  double accelerationDuration = mMaxSpeed / mMaxAcceleration;
  double accelerationAngle = 0.5*mMaxAcceleration*pow(accelerationDuration, 2);
  double totalAngle = fabs((mEndTheta-mStartTheta).toDouble());

  Serial.print("accelerationDuration ");
  Serial.print(accelerationDuration);
  Serial.print(" accelerationAngle ");
  Serial.print(accelerationAngle);
  Serial.print(" total angle ");
  Serial.println(totalAngle);

  if(2* accelerationAngle >totalAngle)
  {
    // Small rotation, we don't have time to reach max speed
    accelerationAngle = totalAngle / 2;
    accelerationDuration = sqrt(2*accelerationAngle/mMaxAcceleration);

    mAngleForAcceleration = accelerationAngle;
    mAngleWithConstantSpeed = 0;
    mEndAccelerationTime = accelerationDuration * SEC_TO_MICROS_MULTIPLICATOR;
    mStartDeccelerationTime = mEndAccelerationTime;
    mExpectedDuration = mStartDeccelerationTime + accelerationDuration * SEC_TO_MICROS_MULTIPLICATOR;
    Serial.print("Small rotation");
    Serial.print("expectedDuration ");
    Serial.println(mExpectedDuration);
  }
  else
  {
    // Big rotation. We will reach max speed
    mAngleForAcceleration = accelerationAngle;
    mAngleWithConstantSpeed = totalAngle-2 * mAngleForAcceleration;
    mEndAccelerationTime = accelerationDuration * SEC_TO_MICROS_MULTIPLICATOR;
    mStartDeccelerationTime = mEndAccelerationTime + SEC_TO_MICROS_MULTIPLICATOR * mAngleWithConstantSpeed / mMaxSpeed;
    mExpectedDuration = mStartDeccelerationTime + accelerationDuration * SEC_TO_MICROS_MULTIPLICATOR;
    Serial.print("Big rotation");
    Serial.print("expectedDuration ");
    Serial.println(mExpectedDuration);
  }
}

Rotation::~Rotation(){}

String Rotation::debugString() 
{
  String startTheta = String(mStartTheta.toDouble(), 4);
  String endTheta = String(mEndTheta.toDouble(), 4);
  return String("Rotation from " + startTheta + " to " + endTheta);
}

double Rotation::positionError(double x, double y, Angle theta, long time)
{
  double vector[2] = {cos(theta.toDouble()), sin(theta.toDouble())};
  double projectedX = (mX-x)*vector[X]+(mY-y)*vector[Y];
  return projectedX;
}

double Rotation::rotationError(double x, double y, Angle theta, long time)
{
  Serial.print("time ");
  Serial.print(time);
  Serial.print(" startTime ");
  Serial.print(mStartTime);
  Serial.print(" ");

  long ellapsedTime = time - mStartTime;
  if(ellapsedTime < 0)
  {
    Serial.print(" 1 ");
    return (mStartTheta-theta).toDouble();
  }
  else if(0 < ellapsedTime && ellapsedTime < mEndAccelerationTime)
  {
    Serial.print(" 2 ");
    Angle expectedTheta = mStartTheta + 0.5* mDirection * mMaxAcceleration *pow((ellapsedTime) * MICROS_TO_SEC_MULTIPLICATOR, 2);
    return (expectedTheta-theta).toDouble();
  }
  else if(mEndAccelerationTime < ellapsedTime && ellapsedTime < mStartDeccelerationTime)
  {
    Serial.print(" 3 ");
    Angle expectedTheta = mStartTheta + mDirection *(mAngleForAcceleration + (ellapsedTime-mEndAccelerationTime)*MICROS_TO_SEC_MULTIPLICATOR * mMaxSpeed);
    return (expectedTheta-theta).toDouble();
  }
  else if(mStartDeccelerationTime < ellapsedTime && ellapsedTime < mExpectedDuration)
  {
    Serial.print(" 4 ");
    Angle expectedTheta = mEndTheta - 0.5*mDirection*mMaxAcceleration*pow((mExpectedDuration-ellapsedTime)* MICROS_TO_SEC_MULTIPLICATOR, 2);
    return (expectedTheta-theta).toDouble();
  }
  else
  {
    Serial.print(" 5 ");
    return (mEndTheta-theta).toDouble();
  }
  Serial.println(" ");
}

bool Rotation::needsPrecision() const {
  return mPrecision;
}

