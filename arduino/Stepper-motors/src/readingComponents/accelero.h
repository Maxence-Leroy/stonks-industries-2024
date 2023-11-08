#ifndef ACCELERO_H
#define ACCELERO_H

#include <stdint.h>

struct AcceleroData {
    int16_t accX;
    int16_t accY;
    int16_t accZ;
    int16_t gyroX;
    int16_t gyroY;
    int16_t gyroZ;
};

void setupAccelero();
AcceleroData getAcceleroData();

#endif