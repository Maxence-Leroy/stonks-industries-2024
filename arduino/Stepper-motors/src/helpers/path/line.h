#ifndef LINE_H
#define LINE_H

#include <Arduino.h>
#include "path.h"
#include "../maths_helpers.h"

class Line : public Path
{
  private:
    double mMaxSpeed, mMaxAcceleration;
    double mVector[2];
    double mDistanceForAcceleration, mDistanceWithConstantSpeed;
    Angle mTheta;
    double mStart[2];
    double mEnd[2];
    bool mPrecision;

  public:
    Line(double xStart, double yStart, double xEnd, double yEnd, double maxSpeed, double maxAcceleration, bool precision);
    virtual ~Line();

    double positionError(double x, double y, Angle theta, long time);
    double rotationError(double x, double y, Angle theta, long time);
    String debugString();

    inline double getEndX(){return mEnd[X];}
    inline double getEndY(){return mEnd[Y];}

    bool needsPrecision() const;
};

#endif