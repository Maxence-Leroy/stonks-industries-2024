#include <Arduino.h>

int SPEED = 3000;

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
  OCR1A = SPEED;
  OCR1B = 100;

  pinMode(7, OUTPUT); // OC4B
  pinMode(6, OUTPUT); // OC4A
  TCCR4A = _BV(COM1A0) | _BV(COM1B1) | _BV(WGM10);
  TCCR4B = _BV(WGM13) | _BV(CS11);
  OCR4A = SPEED;
  OCR4B = 100;
}

void loop()
{

}