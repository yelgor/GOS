#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  servo1.attach(9);
  servo2.attach(10);
  Serial.begin(9600);
}

void loop() {
  for (int angle = -90; angle <= 270; angle++) {
    servo1.write(map(angle, -90, 270, 0, 180));
    servo2.write(map(angle, -90, 270, 90, 180));
    delay(15);
  }

  delay(500);


  for (int angle = 270; angle >= -90; angle--) {
    servo1.write(map(angle, -90, 270, 0, 180));
    servo2.write(map(angle, -90, 270, 90, 180));
    delay(15);
  }

  delay(500);
}
