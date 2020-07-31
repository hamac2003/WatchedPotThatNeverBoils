/*
  Author: Harrison McIntyre
  Last Updated: 7.31.2020
  Contact: hamac2003@gmail.com


  References / Credits:
  Below are links to some of the example code and/or libraries that I integrated into my project.

  [Raspberry Pi / Desktop - Arduino Serial Communication](https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/)
 */



String data = "";

int switchPin = 12;

void setup() {
  pinMode(switchPin, OUTPUT);
  digitalWrite(switchPin, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    Serial.println(data);
  }

  if (data.indexOf("2") > -1){
    digitalWrite(switchPin, HIGH);
  }else if (data.indexOf("1") > -1) {
    digitalWrite(switchPin, LOW);
  }
}
