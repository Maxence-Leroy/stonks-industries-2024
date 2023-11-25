#ifndef HEAVYSIDE_ROTATION_H
#define HEAVYSIDE_ROTATION_H

#include "../angle.h"
#include "path.h"

class HeavysideRotation : public Path
{
  private:
    double mMaxSpeed, mMaxAcceleration, mDirection;
    double mX, mY;
    Angle mStartTheta, mEndTheta;

  public:
    HeavysideRotation(double x, double y, Angle startTheta, Angle endTheta, double maxSpeed, double maxAcceleration);
    virtual ~HeavysideRotation();

    double positionError(double x, double y, Angle theta, long time);
    double rotationError(double x, double y, Angle theta, long time);
    String debugString();
};

#endif