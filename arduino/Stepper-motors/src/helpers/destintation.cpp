#include "destination.h"

Destination::Destination(double iX, double iY, Angle iTheta, bool iBackwards, bool iForcedAngle, bool iOnTheSpot) 
{
    x = iX;
    y = iY;
    theta = iTheta;
    backwards = iBackwards;
    forcedAngle = iForcedAngle;
    onTheSpot = iOnTheSpot;
}

Destination::~Destination()
{

}