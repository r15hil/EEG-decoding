#include <ezOutput.h> // ezOutput library

ezOutput led(9);  // create ezOutput object that attach to pin 9;

void setup() {
 
}

void loop() {
  led.loop(); // MUST call the led.loop() function in loop()

  led.blink(50, 50); // 500 milliseconds ON, 500 milliseconds OFF
}
