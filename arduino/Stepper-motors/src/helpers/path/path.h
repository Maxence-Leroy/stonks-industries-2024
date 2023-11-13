#ifndef PATH_H
#define PATH_H

#include <Arduino.h>
#include "../angle.h"

class Path
{
    protected:
        long int mStartTime, mExpectedDuration, mEndAccelerationTime, mStartDeccelerationTime;
        bool mGoingBackwards = false;

  public:
    Path();
    virtual ~Path();

    virtual double positionError(double x, double y, Angle theta, long time);
    virtual double rotationError(double x, double y, Angle theta, long time);
    virtual String debugString();

    void start();
    bool isOver(long time) const;

    bool isGoingBackwards() const;
};


#endif