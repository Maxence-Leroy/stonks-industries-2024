#ifndef PATH_QUEUE_H
#define PATH_QUEUE_H

#include "../helpers/destination.h"
#include "../helpers/path/path.h"

void addDestination(Destination* destination);
bool extractNextDestination();
Path* getNextPath();
void clearQueue();

#endif