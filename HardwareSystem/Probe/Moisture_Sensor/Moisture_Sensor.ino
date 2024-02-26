/* APWS-HW-Probe-Moisture SP10
Jaime Sanchez, Rogrigo Romero, Evan LeBel, Ian Skillman
*/


/* Change these values based on your observations */
#define wetSoil 2600   // Define max value we consider soil 'wet'
#define drySoil 2900   // Define min value we consider soil 'dry'

// Define analog input
#define sensorPin A0


void setup() {
  Serial.begin(9600);

}


void loop() {
  // Read the Analog Input and print it
  int moisture = analogRead(sensorPin);
  Serial.print("Analog output: ");
  Serial.println(moisture);
  
  // Determine status of our soil
  if (moisture < wetSoil) {
    Serial.println("Status: Soil is too wet");
  } else if (moisture >= wetSoil && moisture < drySoil) {
    Serial.println("Status: Soil moisture is perfect");
  } else {
    Serial.println("Status: Soil is too dry - time to water!");
  }
  Serial.println();
  
  // Take a reading every second
  delay(1000);
}