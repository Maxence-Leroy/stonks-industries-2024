#ifndef ENSLAVEMENT_H
#define ENSLAVEMENT_H

#include "../helpers/angle.h"
#include "../helpers/path/path.h"

void setInitialPosition(double x, double y, Angle theta);
void setCurrentPath(Path* path);
void enslave(long time);

#endif