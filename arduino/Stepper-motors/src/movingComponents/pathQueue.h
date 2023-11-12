#ifndef PATH_QUEUE_H
#define PATH_QUEUE_H

#include "../helpers/angle.h"
#include "../helpers/path/path.h"

void addDestination(double x, double y, Angle theta, bool backwards);
Path* getNextPath();

#endif