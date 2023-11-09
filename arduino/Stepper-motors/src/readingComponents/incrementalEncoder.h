#ifndef INCREMENTAL_ENCODER_H
#define INCREMENTAL_ENCODER_H

#include <stdint.h>

void setupIncrementalEncoders();
const int32_t getIncrementalEncoderLeftValue();
const int32_t getIncrementalEncoderRightValue();

#endif

