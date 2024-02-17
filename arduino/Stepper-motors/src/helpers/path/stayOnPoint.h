#ifndef STAY_ON_POINT_H
#define STAY_ON_POINT_H

#include "../angle.h"
#include "path.h"

class StayOnPoint : public Path
{
  private:
    double mX, mY;
    Angle mTheta;

  public:
    StayOnPoint(double x, double y, Angle theta);
    virtual ~StayOnPoint();

    double positionError(double x, double y, Angle theta, long time);
    double rotationError(double x, double y, Angle theta, long time);
    String debugString();

    bool sendDone() const;
};

#endif