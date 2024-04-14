/*
Creators: Evan LeBel, Ian Skillman, Jaime Sanchez, Rodrigo Romero
Date: 3/25/2024

FOR THIS CODE YOU NEED LIBRARY "Adafruit AHTX0"

Connectors:
Temp & Humid Sensor: Connect Vin to 3.3V, GND to GND, SCL to A5, SDA to A4
PhotoResistor: Connect A1 to voltage going from photoresistor to gnd. Circuit is from 3.3V to PhotoResistor to Resistor to GND
UltraSonic: Connect GND to GND, Echo to D10, Trig to D9, and VCC to VBUS
Soil: Connect A Pin connects to A0, + Pin connects to 3.3V, - Pin connects to GND
*/

#include <Adafruit_AHTX0.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Wire.h>

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_MOIST_UUID "fb6cf981-31cc-4f36-af06-1f2f3e919840"
#define CHARACTERISTIC_TEMP_UUID "35b17f66-73d1-4c92-92f6-9032ef1987d3"
#define CHARACTERISTIC_LIGHT_UUID "3cab9341-e65b-46e9-83ed-c8a7f2f841c2"
#define CHARACTERISTIC_HUM_UUID "f3b857d0-1e8a-4dff-a941-9ea9a3594275"

#define wetSoil 2600   // Define max value we consider soil 'wet'
#define drySoil 2900   // Define min value we consider soil 'dry'
#define bright 1500

// Define analog input
#define MoisturePin A0
#define LightPin A1

// makes the chracteristic globlal
static BLECharacteristic *pCharacteristicMoist;
static BLECharacteristic *pCharacteristicTemp;
static BLECharacteristic *pCharacteristicHum;
static BLECharacteristic *pCharacteristicLight;
BLEServer* pServer = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
sensors_event_t humidity, temp;  
uint32_t moisture, light;

Adafruit_AHTX0 aht;

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      BLEDevice::startAdvertising();
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

void setup() {
  delay(2000);

  Serial.begin(115200);

  delay(2000);

  //Temp & Humidity Sensor setup:
  
  Serial.println("Adafruit AHT10/AHT20 demo!");
  if (! aht.begin()) {
    Serial.println("Could not find AHT? Check wiring");
    while (1) delay(10);  
  }
  Serial.println("AHT10 or AHT20 found");
  

  Serial.println("Starting BLE work!");

  BLEDevice::init("SP10Server");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristicMoist = pService->createCharacteristic(
                                         CHARACTERISTIC_MOIST_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  pCharacteristicTemp = pService->createCharacteristic(
                                         CHARACTERISTIC_TEMP_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  pCharacteristicLight = pService->createCharacteristic(
                                         CHARACTERISTIC_LIGHT_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  pCharacteristicHum = pService->createCharacteristic(
                                         CHARACTERISTIC_HUM_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE
                                       );
  pService->start();
  // BLEAdvertising *pAdvertising = pServer->getAdvertising();  // this still is working for backward compatibility
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined!");
}

void ReadLight(){
  light = analogRead(LightPin);
  //light = 0;

  Serial.println("Light Value: ");
  Serial.println(light);

  if (light > bright) {
    Serial.println("Light Level High");
  } else {
    Serial.println("Light Level Low");
  }
}

void ReadMoisture(){
  moisture = analogRead(MoisturePin);

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

void ReadTemp(){

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

void loop() {
  Serial.print("================================="); 
  ReadMoisture();
  ReadLight();
  ReadTemp();

  if (deviceConnected) {
    pCharacteristicMoist->setValue(moisture);//setValue takes uint8_t, uint16_t, uint32_t, int, float, double and string
    pCharacteristicTemp->setValue(temp.temperature);
    pCharacteristicLight->setValue(light);
    pCharacteristicHum->setValue(humidity.relative_humidity);
  }
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    delay(500); // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising(); // restart advertising
    Serial.println("start advertising");
    oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    oldDeviceConnected = deviceConnected;
  }

  delay(3 * 1000 * 60);     //delay 3 minutes
  //delay(30000);
}
