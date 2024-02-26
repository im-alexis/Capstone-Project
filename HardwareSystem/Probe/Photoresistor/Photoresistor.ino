//int ledPin = 2;

void setup() {
    Serial.begin(9600);
    //pinMode(ledPin,  OUTPUT);
}

void loop() {
    int value = analogRead(A0);

    Serial.println("Analog  Value: ");
    Serial.println(value);
    
    if (value > 1000) {
        Serial.println("Light Level High");
    } else {
        Serial.println("Light Level Low");
    }
    
    delay(250);
}
