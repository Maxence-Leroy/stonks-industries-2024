#include <Arduino.h>
#include "detector.h"
#include "helpers/robotConfig.h"

bool detection = false;
long previousSerial = 0;

void startLaserDetection() {
    detection = true;
}

void laserDetect() {
    if(detection) {
        long currentTime = micros();
        if(currentTime - previousSerial > 1000 /* us */) {
            previousSerial = currentTime;
            int left = analogRead(LASER_LEFT_PIN);
            int mid = analogRead(LASER_MID_PIN);
            int right = analogRead(LASER_RIGHT_PIN);

            Serial2.print("LL");
            Serial2.print(left);
            Serial2.print(";LM");
            Serial2.print(mid);
            Serial2.print(";LR");
            Serial2.println(right);
        }
    }
}

void stopLaserDetection() {
    detection = false;
}