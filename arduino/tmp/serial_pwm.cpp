#include <Arduino.h>

String receivedString;

void setup()

{
  pinMode(11, OUTPUT); // OC1A
  pinMode(12, OUTPUT); // OC1B

  // See documentation Atmel ATmega640 page 128
  // Set WGM1 to 101 (bit default values are 0, and bits 0 and 2 are set to 1) -> mode is now PWM, Phase Correct, with TOP value OCRA, page 128
  // Set COM1A to 10 -> Clear OC1A on Compare Match when up-counting. Set OC1A on Compare Match when down-counting, page 127
  // Set COM1B to 10 -> Set OC1A when counter value is below OCR1B, page 128
  // Set CS1 to 101 -> Clock prescalar is 1024, page 130

  TCCR1A = _BV(COM1A0) | _BV(COM1B1) | _BV(WGM10);
  TCCR1B = _BV(WGM13) | _BV(CS11);
  OCR1A = 255 * 2 * 2 * 2 * 2;
  OCR1B = 100;

  pinMode(2, OUTPUT); // OC3B
  pinMode(5, OUTPUT); // OC3A
  TCCR3A = _BV(COM3A0) | _BV(COM3B1) | _BV(WGM30);
  TCCR3B = _BV(WGM33) | _BV(CS32) | _BV(CS30);
  OCR3A = 255 * 2 * 2 * 2 * 2;
  OCR3B = 255 * 2;

  Serial.begin(115200, SERIAL_8N1);
}

void loop()

{
  if (Serial.available() > 0){
    receivedString = Serial.readStringUntil('\n');
    unsigned recievedNumber = receivedString.toInt();
    OCR1A = recievedNumber;
    Serial.println(recievedNumber);
  }
  digitalWrite(23, HIGH);
}