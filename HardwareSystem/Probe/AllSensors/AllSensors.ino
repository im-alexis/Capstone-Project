/*
Creators: Evan LeBel, Ian Skillman, Jaime Sanchez, Rodrigo Romero
Date: 2/28/2024

FOR THIS CODE YOU NEED LIBRARY "Adafruit AHTX0"

Connectors:
Temp & Humid Sensor: Connect Vin to 3.3V, GND to GND, SCL to A5, SDA to A4
PhotoResistor: Connect A1 to voltage going from photoresistor to gnd. Circuit is from 3.3V to PhotoResistor to Resistor to GND
UltraSonic: Connect GND to GND, Echo to D10, Trig to D9, and VCC to VBUS
Soil: Connect A Pin connects to A0, + Pin connects to 3.3V, - Pin connects to GND
*/


#include <Adafruit_AHTX0.h>

Adafruit_AHTX0 aht;

#define wetSoil 2600   // Define max value we consider soil 'wet'
#define drySoil 2900   // Define min value we consider soil 'dry'

#define bright 1500

// Define analog input
#define MoisturePin A0
#define LightPin A1

const int trigPin = 9;
const int echoPin = 10;
long duration;
int distance;

void setup() {

  //Ultradonic Sensor setup:
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

  Serial.begin(9600);

  //Temp & Humidity Sensor setup:
  Serial.println("Adafruit AHT10/AHT20 demo!");
  if (! aht.begin()) {
    Serial.println("Could not find AHT? Check wiring");
    while (1) delay(10);  
  }
  Serial.println("AHT10 or AHT20 found");

}

void light(){
  int light = analogRead(LightPin);

  Serial.println("Light Value: ");
  Serial.println(light);

  if (light > bright) {
    Serial.println("Light Level High");
  } else {
    Serial.println("Light Level Low");
  }
}

void moisture(){
  int moisture = analogRead(MoisturePin);

  Serial.print("Moisture Value: ");
  Serial.println(moisture);

  if (moisture < wetSoil) {
    Serial.println("Status: Soil is too wet");
  } else if (moisture >= wetSoil && moisture < drySoil) {
    Serial.println("Status: Soil moisture is perfect");
  } else {
    Serial.println("Status: Soil is too dry - time to water!");
  }
}

void temp(){
  sensors_event_t humidity, temp;  
  aht.getEvent(&humidity, &temp);// populate temp and humidity objects with fresh data

  Serial.print("Temperature: "); 
  Serial.print(((temp.temperature * 9) + 3) / 5 + 32); //farenheight 
  Serial.println(" degrees F");  
  Serial.print(temp.temperature); //celcius
  Serial.println(" degrees C");
  Serial.print("Humidity: ");
  Serial.print(humidity.relative_humidity); 
  Serial.println("% rH");
}

void tank(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.println(distance);
}

void loop() {
  moisture();
  light();
  temp();
  tank();

  delay(1000);
}
