#ifndef HEAVYSIDE_POSITION_H
#define HEAVYSIDE_POSITION_H

#include <Arduino.h>
#include "path.h"
#include "../maths_helpers.h"

class HeavysidePosition : public Path
{
  private:
    double mMaxSpeed, mMaxAcceleration;
    Angle mTheta;
    double mStart[2];
    double mEnd[2];

  public:
    HeavysidePosition(double xStart, double yStart, double xEnd, double yEnd, double maxSpeed, double maxAcceleration);
    virtual ~HeavysidePosition();

    double positionError(double x, double y, Angle theta, long time);
    double rotationError(double x, double y, Angle theta, long time);
    String debugString();

    inline double getEndX(){return mEnd[X];}
    inline double getEndY(){return mEnd[Y];}
};

#endif