#ifndef INCREMENTAL_ENCODER_H
#define INCREMENTAL_ENCODER_H

#include <stdint.h>

void setupIncrementalEncoders();
const uint32_t getIncrementalEncoderLeftValue();
const uint32_t getIncrementalEncoderRightValue();

#endif

