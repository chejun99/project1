void setup() {
Serial.begin(9600);
pinMode(10,INPUT);
}

void loop() {
int i = digitalRead(10);
//Serial.print('a');
Serial.println(i);

delay(1000);
}
