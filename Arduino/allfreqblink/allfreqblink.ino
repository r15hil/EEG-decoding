#include <ezOutput.h> // ezOutput library

ezOutput led7(7);  // create ezOutput object that attach to pin 7;
ezOutput led8(8);  // create ezOutput object that attach to pin 8;
ezOutput led9(9);  // create ezOutput object that attach to pin 9;

void setup() {
  led7.blink(71, 71); // 500 milliseconds ON, 250 milliseconds OFF
  led8.blink(50, 50); // 250 milliseconds ON, 250 milliseconds OFF
  led9.blink(42, 42); // 100 milliseconds ON, 100 milliseconds OFF
}

void loop() {
  led7.loop(); // MUST call the led1.loop() function in loop()
  led8.loop(); // MUST call the led2.loop() function in loop()
  led9.loop(); // MUST call the led3.loop() function in loop()
}
