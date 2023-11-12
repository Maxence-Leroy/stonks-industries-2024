#ifndef ENSLAVEMENT_H
#define ENSLAVEMENT_H

#include "../helpers/angle.h"

void setInitialPosition(double x, double y, Angle theta);
void enslave(double expectedX, double expectedY, Angle expectedTheta, bool backwards);

#endif