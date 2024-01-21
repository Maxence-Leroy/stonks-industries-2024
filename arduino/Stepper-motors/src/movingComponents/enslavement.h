#ifndef ENSLAVEMENT_H
#define ENSLAVEMENT_H

#include "../helpers/angle.h"
#include "../helpers/path/path.h"

void setPRot(float newPRot);
void setIRot(float newIRot);
void setDRot(float newDRot);
void setPPos(float newPPos);
void setIPos(float newIPos);
void setDPos(float newDPos);

void setInitialPosition(double x, double y, Angle theta);
void setCurrentPath(Path* path);
void enslave(long time);
const double getCurrentX();
const double getCurrentY();
const Angle getCurrentTheta();
Path* getCurrentPath();

#endif