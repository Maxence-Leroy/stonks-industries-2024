#ifndef ROTATION_H
#define ROTATION_H

#include "../angle.h"
#include "path.h"

class Rotation : public Path
{
  private:
    double mMaxSpeed, mMaxAcceleration, mDirection;
    double mAngleForAcceleration, mAngleWithConstantSpeed;

    bool mPrecision;

    double mX, mY;
    Angle mStartTheta, mEndTheta;

  public:
    Rotation(double x, double y, Angle startTheta, Angle endTheta, double maxSpeed, double maxAcceleration, bool precision);
    virtual ~Rotation();

    double positionError(double x, double y, Angle theta, long time);
    double rotationError(double x, double y, Angle theta, long time);
    String debugString();

    bool needsPrecision() const;
};

#endif