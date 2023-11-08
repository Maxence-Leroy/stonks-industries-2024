#include <Arduino.h>

#include "../helpers/robotConfig.h"
#include "incrementalEncoder.h"

volatile uint32_t leftValue = 0;
volatile uint32_t rightValue = 0;

const uint32_t getIncrementalEncoderLeftValue() {
    return leftValue;
}

const uint32_t getIncrementalEncoderRightValue() {
    return rightValue;
}

void increase1Left() {
    if(PINE & (1 << PE5))
        leftValue += 1;
    else
        leftValue -= 1;
}

void increase2Left() {
    if(PINE & (1 << PE4))
        leftValue -= 1;
    else
        leftValue += 1;
}

void increase1Right() {
    if(PIND & (1 << PD3))
        rightValue += 1;
    else
        rightValue -= 1;
}
void increase2Right() {
    if(PIND & (1 << PD2))
        rightValue -= 1;
    else
        rightValue += 1;
}

void setupIncrementalEncoders()
{
  pinMode(INCREMENTAL_ENCODER_LEFT_PIN_1, INPUT);
  pinMode(INCREMENTAL_ENCODER_LEFT_PIN_2, INPUT);
  pinMode(INCREMENTAL_ENCODER_RIGHT_PIN_1, INPUT);
  pinMode(INCREMENTAL_ENCODER_RIGHT_PIN_2, INPUT);
  attachInterrupt(digitalPinToInterrupt(INCREMENTAL_ENCODER_LEFT_PIN_1), increase1Left, RISING);
  attachInterrupt(digitalPinToInterrupt(INCREMENTAL_ENCODER_LEFT_PIN_2), increase2Left, RISING);
  attachInterrupt(digitalPinToInterrupt(INCREMENTAL_ENCODER_RIGHT_PIN_1), increase1Right, RISING);
  attachInterrupt(digitalPinToInterrupt(INCREMENTAL_ENCODER_RIGHT_PIN_2), increase2Right, RISING);
}