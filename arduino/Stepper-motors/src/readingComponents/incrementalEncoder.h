#ifndef INCREMENTAL_ENCODER_H
#define INCREMENTAL_ENCODER_H

#include <stdint.h>

void setupIncrementalEncoders();
void updateIncrementalEncodersValue();
const int64_t getIncrementalEncoderLeftValue();
const int64_t getIncrementalEncoderRightValue();
void resetEncoders();

#endif

