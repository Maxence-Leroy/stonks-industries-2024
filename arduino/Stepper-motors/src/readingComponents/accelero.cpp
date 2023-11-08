#include <Wire.h>

#include "accelero.h"

const int I2C_ADDRESS = 0x68;

void setupAccelero() {
    Wire.begin();
    Wire.beginTransmission(I2C_ADDRESS);
    Wire.write(0x6B); // Wake up the device
    Wire.write(0);    
    Wire.endTransmission(true);
}

AcceleroData getAcceleroData() {
    Wire.beginTransmission(I2C_ADDRESS);
    Wire.write(0x3B); // Ask to read data
    Wire.endTransmission(false);
    Wire.requestFrom(I2C_ADDRESS,7*2,true);

    AcceleroData answer;

    // Wire.read() << 8 | Wire.read() allows us to put in the same variable the high and low bytes
    answer.accX = Wire.read() << 8 | Wire.read();
    answer.accY = Wire.read() << 8 | Wire.read();  
    answer.accZ = Wire.read() << 8 | Wire.read();
    int16_t temperature = Wire.read() << 8 | Wire.read(); // Unused data
    answer.gyroX = Wire.read() << 8 | Wire.read();  
    answer.gyroY = Wire.read() << 8 | Wire.read();  
    answer.gyroZ = Wire.read() << 8 | Wire.read(); 

    return answer;
}