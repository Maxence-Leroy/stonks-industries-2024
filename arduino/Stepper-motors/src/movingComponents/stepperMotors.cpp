#include <Arduino.h>

#include "../helpers/robotConfig.h"
#include "stepperMotors.h"

void setupMotors() {
    pinMode(LEFT_SIDE_PIN, OUTPUT);
    pinMode(RIGHT_SIDE_PIN, OUTPUT);

    pinMode(LEFT_SPEED_PIN, OUTPUT);
    pinMode(RIGHT_SPEED_PIN, OUTPUT);

    // TODO: Comments may be outdated, check it

    // See documentation Atmel ATmega640 page 128
    // Set WGM1 to 101 (bit default values are 0, and bits 0 and 2 are set to 1) -> mode is now PWM, Phase Correct, with TOP value OCRA, page 128
    // Set COM1A to 10 -> Clear OC1A on Compare Match when up-counting. Set OC1A on Compare Match when down-counting, page 127
    // Set COM1B to 10 -> Set OC1A when counter value is below OCR1B, page 128
    // Set CS1 to 1 -> Clock prescalar is 0, page 130

    TCCR1A = _BV(COM1A0) | _BV(COM1B1) | _BV(WGM10);
    TCCR1B = _BV(WGM13) | _BV(CS10);
    OCR1A = ZERO_PACE;
    OCR1B = DEFAULT_B_VALUE;

    TCCR4A = _BV(COM4A0) | _BV(COM4B1) | _BV(WGM40);
    TCCR4B = _BV(WGM43) | _BV(CS40);
    OCR4A = ZERO_PACE;
    OCR4B = DEFAULT_B_VALUE;
}

void restartMotors(){
}

uint16_t speedToPace(double speed) {
    if(speed == 0) {
        return ZERO_PACE;
    } else {
        return (uint16_t) (320666 / speed);
    }
}

void setLeftMotorSpeed(double speed) {
    double unsignedSpeed;
    if (speed < 0) {
        unsignedSpeed = -speed;
        digitalWrite(LEFT_SIDE_PIN, HIGH);
    } else {
        unsignedSpeed = speed;
        digitalWrite(LEFT_SIDE_PIN, LOW);
    }
    uint16_t unsignedPace = speedToPace(unsignedSpeed);
    unsignedPace = unsignedPace < MIN_PACE && unsignedPace != 0 ? MIN_PACE : unsignedPace;
    unsignedPace = unsignedPace > MAX_PACE ? ZERO_PACE : unsignedPace;
    OCR4A = unsignedPace;
}

void setRightMotorSpeed(double speed) {
    double unsignedSpeed;
    if (speed < 0) {
        unsignedSpeed = -speed;
        digitalWrite(RIGHT_SIDE_PIN, HIGH);
    } else {
        unsignedSpeed = speed;
        digitalWrite(RIGHT_SIDE_PIN, LOW);
    }
    uint16_t unsignedPace = speedToPace(unsignedSpeed);
    unsignedPace = unsignedPace < MIN_PACE && unsignedPace != 0 ? MIN_PACE : unsignedPace;
    unsignedPace = unsignedPace > MAX_PACE ? ZERO_PACE : unsignedPace;
    OCR1A = unsignedPace;
}

void stopMotors() {
    setLeftMotorSpeed(0);
    setRightMotorSpeed(0);
}