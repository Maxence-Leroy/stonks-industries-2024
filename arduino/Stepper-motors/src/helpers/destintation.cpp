#include "destination.h"

Destination::Destination(double iX, double iY, Angle iTheta, bool iBackwards, bool iForcedAngle, bool iOnTheSpot, int iMaxSpeed, int iMaxAcceleration, bool iPrecision) 
{
    x = iX;
    y = iY;
    theta = iTheta;
    backwards = iBackwards;
    forcedAngle = iForcedAngle;
    onTheSpot = iOnTheSpot;
    maxSpeed = iMaxSpeed;
    maxAcceleration = iMaxAcceleration;
    precision = iPrecision;
}

Destination::~Destination()
{

}