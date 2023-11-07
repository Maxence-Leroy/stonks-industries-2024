void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial2.begin(115200);
  Serial.println("Start");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0) {
    String res = Serial.readStringUntil('\n');
    Serial2.print(res + "\n");
  }

    if(Serial2.available() > 0) {
    String res = Serial2.readStringUntil('\n');
    Serial.println(res);
  }
}
