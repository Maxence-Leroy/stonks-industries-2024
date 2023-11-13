#include "destination.h"

Destination::Destination(double iX, double iY, Angle iTheta, bool iBackwards, bool iForcedAngle) 
{
    x = iX;
    y = iY;
    theta = iTheta;
    backwards = iBackwards;
    forcedAngle = iForcedAngle;
}

Destination::~Destination()
{

}