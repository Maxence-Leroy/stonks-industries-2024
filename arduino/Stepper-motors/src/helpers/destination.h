#ifndef DESTINATION_H
#define DESTINATION_H

#include "angle.h"

class Destination
{
    public:
        Destination(double iX, double iY, Angle iTheta, bool iBackwards, bool iForcedAngle, bool iOnTheSpot, int iMaxSpeed, int iMaxAcceleration, bool iPrecision);
        ~Destination();
        double x;
        double y;
        Angle theta;
        bool backwards;
        bool forcedAngle;
        bool onTheSpot;
        int maxSpeed;
        int maxAcceleration;
        bool precision;
};


#endif