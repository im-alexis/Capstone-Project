/*
  Tank code
  Handles connecting the the probe bluetooth signal and sending it to the server
*/

#include <SPI.h>
#include <ArduinoBLE.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include "MAX17043.h"

//----------------------------------------------------------------------------------------------------------------------
// WiFi
//----------------------------------------------------------------------------------------------------------------------

///////TODO: Put Wifi Username and Password
char ssid[32] = "Ours 2 GHz"; //Need to be 2 GHz
char pass[32] = ""; //INSERT WIFI PASSWORD;         //Change wifi password
char* systemID = "a2h87hd1";

//TODO: Update serverName

const char* serverName = "http://192.168.1.104:5000/data";   //"http://IP_ADDRESS:5000/data"
const char* getServerName = strcat("http://192.168.1.104:5000/GetInstruction?SystemID=", systemID);

String sensorReadings;
int sensorReadingsArr[3];

//----------------------------------------------------------------------------------------------------------------------
// BLE UUIDs
//----------------------------------------------------------------------------------------------------------------------

// https://www.bluetooth.com/specifications/gatt/services/
// https://www.bluetooth.com/specifications/gatt/characteristics/

static String    serviceUUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b");
static String    charUUID("beb5483e-36e1-4688-b7f5-ea07361b26a8");
static char*    charMoistUUID("fb6cf981-31cc-4f36-af06-1f2f3e919840");
static char*    charTempUUID("35b17f66-73d1-4c92-92f6-9032ef1987d3");
static char*    charLightUUID("3cab9341-e65b-46e9-83ed-c8a7f2f841c2");
static char*    charHumUUID("f3b857d0-1e8a-4dff-a941-9ea9a3594275");

//----------------------------------------------------------------------------------------------------------------------
//Bluetooth Wifi Setup
//----------------------------------------------------------------------------------------------------------------------

#define CHARACTERISTIC_SSID_UUID "fb6cf981-31cc-4f36-af06-1f2f3e919840"
#define CHARACTERISTIC_Pass_UUID "35b17f66-73d1-4c92-92f6-9032ef1987d3"
#define CHARACTERISTIC_Done_UUID "3cab9341-e65b-46e9-83ed-c8a7f2f841c2"
static BLECharacteristic pCharacteristicSSID(CHARACTERISTIC_SSID_UUID, BLERead | BLEWrite, 32);
static BLECharacteristic pCharacteristicPass(CHARACTERISTIC_Pass_UUID, BLERead | BLEWrite, 32);
static BLECharacteristic pCharacteristicDone(CHARACTERISTIC_Done_UUID, BLERead | BLEWrite, 1);

typedef struct __attribute__( ( packed ) )
{
  uint32_t moisture;
  float temp;
  uint32_t light;
  float humidity;
} plant_health;

plant_health ble_plant_health;

int voltage;

//For Ultrasonic
int sensorLoop = 0;
const int trigPin = 9;
const int echoPin = 10;
long duration;
int distance;

//----------------------------------------------------------------------------------------------------------------------
// App
//----------------------------------------------------------------------------------------------------------------------

bool updateWeb = true;
bool updateHealth = true;
bool wifiActive = false;
bool bleActive = false;
bool updated = false;
bool WiFisetup = false;

#define pumpPin 2              //TODO: Change pumpPin to what the pumpPin will be
#define pumpActiveLength 10    //in seconds
int pumpActiveTimeRemaining = 0;    //This is our timer for our pump to always reference how much time is left to run, no multithreading no r/w problems (dub)

String httpRequestData = "";
WiFiClient client;
HTTPClient http;

//----------------------------------------------------------------------------------------------------------------------
// I/O
//----------------------------------------------------------------------------------------------------------------------

void setup()
{
  delay(2000);
  pinMode(pumpPin, OUTPUT);

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

  Serial.begin( 9600 );
  while ( !Serial );          //TODO: Delete such that it can run without Serial Monitor

  Serial.println( "Tank Code Starting" );

  if (FuelGauge.begin())
  {
    Serial.println("Resetting device...");
    FuelGauge.reset();
    delay(250);

    Serial.println("Initiating quickstart mode...");
    FuelGauge.quickstart();
    delay(125);
  }
  else
  {
    Serial.println("The MAX17043 device was NOT found.\n");
    while (true);
  }
}


void loop()
{
#define NTP_SYNC_INTERVAL 60 * 60 * 1000
#define TIME_UPDATE_INTERVAL 1000 // needs to be 1000 ms

  static unsigned long previousMillis = 0;
  static unsigned long ntpSyncPreviousMillis = 0;

  //  Still need testgin

  // if(WiFisetup == false){
  //   setupWifi();
  //   WiFisetup == true;
  // }
  

  bleTask();

  if((ble_plant_health.moisture < 12000) && (updated == true) && (pumpActiveTimeRemaining != 0)){
    updated = false;
    /*                          //TODO: uncomment this block text, change pumpPin into the pumpPin ammount, maybe change for loop amount
    pumpEnable(pumpActiveLength);
    */
  }

  if(sensorLoop == 0){
    PeriodicUpdate();
  }
  sensorLoop = (sensorLoop + 1) % 5;

  wifiTask();

  delay(1000);

}


//==================================================================
//Use This one for only enabling for burst amount of seconds at a time but will be reoccuring, meaning we will constantly come back until the clock expires
#define dutyCycle 1000/2   //50% duty cycle

void pumpEnable(int seconds)
{
  pumpActiveTimeRemaining += seconds;
  int burst = 5;  
  while( (burst != 0) && (pumpActiveTimeRemaining != 0) ){
      digitalWrite(pumpPin, HIGH);
      delayMicroseconds(dutyCycle);
      digitalWrite(pumpPin, LOW);
      delayMicroseconds(1000 - dutyCycle);
      burst--; pumpActiveTimeRemaining--;
    }
}
//==================================================================


//==================================================================
////Use this one for enabling for X amount of seconds
// #define dutyCycle 1000/2   //50% duty cycle

// void pumpEnable(int seconds)
// {
//   for(int i = 0; i < seconds; i++){
//       digitalWrite(pumpPin, HIGH);
//       delayMicroseconds(dutyCycle);
//       digitalWrite(pumpPin, LOW);
//       delayMicroseconds(1000 - dutyCycle);
//     }
// }
//==================================================================

void wifiTask( void )
{
  enum WIFI_STATE_TYPE { WIFI_STATE_OFF,
                         WIFI_STATE_CONNECT,
                         WIFI_STATE_SEND,
                         WIFI_STATE_RECIEVE,
                         WIFI_STATE_END,
                         WIFI_STATE_RESTART = 255
                       };

  static int state = WIFI_STATE_OFF;
  static int wifiConnectTry = 0;
  static int wifiStatus = WL_IDLE_STATUS;
  static unsigned long previousMillis = 0;

  switch ( state )
  {
    case WIFI_STATE_OFF:
      if ( updateWeb && ! bleActive )
      {
        wifiActive = true;
        updateWeb = false;
        Serial.println( "WiFi active" );
        state++;
        break;
      }
      break;
    case WIFI_STATE_CONNECT:
      if ( WiFi.isConnected() )
      {
        Serial.println( "WiFi connected" );
        state++;
        break;
      }
      if ( wifiConnectTry > 10 )
      {
        // could not connect, clear everything and try again later
        state = WIFI_STATE_RESTART;
        break;
      }
      WiFi.mode(WIFI_STA);
      wifiStatus = WiFi.begin( ssid, pass );
      delay(1000);
      wifiConnectTry++;
      Serial.print( "Try: " );
      Serial.print( wifiConnectTry );
      Serial.print( " Status: " );
      Serial.println( wifiStatus );
      break;
    case WIFI_STATE_SEND:
    {


      /*//Testing w/ Alexis
      http.begin(client, "http://:5000/data");
      Serial.println(WiFi.localIP());
      */

      //orginal: comment out if testing
      http.begin(client, serverName);

      
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST("{\"systemID\":\"" + String(systemID) + "\",\"tank_level\":" + String(distance) + ",\"battery_level\":" + String (voltage) + ",\"probes\":[{\"moisture\":" + String(ble_plant_health.moisture) + ",\"temp\":" + String(ble_plant_health.temp) + ",\"light\":" + String(ble_plant_health.light) + ",\"humidity\":" + String(ble_plant_health.humidity) + "}]}");

      //httpResponseCode = http.POST(httpRequestData);
      Serial.println( "http posted" );
      http.end();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      if(httpResponseCode == 500){
        //TODO: based on http Responses
        //Could do a fail to recieve and state = WIFI_STATE_SEND to try again, but then should have it only try 10 times
        state = WIFI_STATE_SEND;
        break;
      }
      state++;
      break;
    }
    case WIFI_STATE_RECIEVE:
    {
      // https://github.com/amcewen/HttpClient/blob/master/examples/SimpleHttpExample/SimpleHttpExample.ino
      http.begin(client, getServerName);
      int httpResponseCode = http.GET();
      String payload = "{}"; 
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        payload = http.getString();
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
        http.end();
        break;
      }
      // Free resources
      http.end();

      Serial.println(payload);
      JSONVar myObject = JSON.parse(payload);

      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        break;
      }
    
      Serial.print("JSON object = ");
      Serial.println(myObject);
    
      // myObject.keys() can be used to get an array of all the keys in the object
      JSONVar keys = myObject.keys();
    
      for (int i = 0; i < keys.length(); i++) {
        JSONVar value = myObject[keys[i]];
        Serial.print(keys[i]);
        Serial.print(" = ");
        Serial.println(value);
        sensorReadingsArr[i] = int(value);
      }
      Serial.print("1 = ");
      Serial.println(sensorReadingsArr[0]);
      Serial.print("2 = ");
      Serial.println(sensorReadingsArr[1]);
      Serial.print("3 = ");
      Serial.println(sensorReadingsArr[2]);
      break;
    }
    case WIFI_STATE_END:
      state = WIFI_STATE_OFF;
      wifiConnectTry = 0;
      wifiStatus = WL_IDLE_STATUS;
      WiFi.disconnect();
      wifiActive = false;
      updateHealth = true;
      Serial.println( "WiFi end" );
      break;
    default:
      state = WIFI_STATE_CONNECT;
      wifiConnectTry = 0;
      wifiStatus = WL_IDLE_STATUS;
      WiFi.disconnect();
      Serial.println( "WiFi restart" );
      break;
  }
}

void bleTask( void )
{
  enum BLE_STATE_TYPE { BLE_STATE_OFF,
                        BLE_STATE_BEGIN,
                        BLE_STATE_START_SCAN,
                        BLE_STATE_SCAN,
                        BLE_STATE_STOP_SCAN,
                        BLE_STATE_PERIPHERAL_CONNECT,
                        BLE_STATE_PERIPHERAL_DISCOVER,
                        BLE_STATE_PERIPHERAL_READ,
                        BLE_STATE_END,
                        BLE_STATE_RESTART = 255
                      };

#define BLE_SCAN_TIMEOUT 10000

  static int state = BLE_STATE_OFF;
  static unsigned long previousMillis = 0;
  static BLEDevice peripheral;

  switch ( state )
  {
    case BLE_STATE_OFF:
      if ( updateHealth && ! wifiActive )
      {
        bleActive = true;
        updateHealth = false;
        Serial.println( "BLE active" );
        state++;
        break;
      }
      break;
    case BLE_STATE_BEGIN:
      if ( !BLE.begin() )
      {
        Serial.println( "Starting BLE failed!" );
        break;
      }
      state++;
      break;
    case BLE_STATE_START_SCAN:
      BLE.scanForUuid( serviceUUID );
      Serial.println( "BLE_STATE_START_SCAN" );
      state++;
      break;
    case BLE_STATE_SCAN:
      peripheral = BLE.available();
      if ( !peripheral )
      {
        Serial.println( "no peripheral found" );
        break;
      }
      if ( peripheral.localName() != "SP10Server" )
      {
        Serial.println( "SP10Server not found" );
        break;
      }
      state++;
      Serial.println( "SP10Server found" );
      break;
    case BLE_STATE_STOP_SCAN:
      BLE.stopScan();
      state++;
      break;
    case BLE_STATE_PERIPHERAL_CONNECT:
      if ( !peripheral.connect() )
      {
        state = BLE_STATE_START_SCAN;
      }
      state++;
      break;
    case BLE_STATE_PERIPHERAL_DISCOVER:
      if ( !peripheral.discoverAttributes() )
      {
        peripheral.disconnect();
        state = BLE_STATE_START_SCAN;
      }
      state++;
      break;
    case BLE_STATE_PERIPHERAL_READ:
      {
        BLECharacteristic CharacteristicMoist = peripheral.characteristic( charMoistUUID );
        if ( CharacteristicMoist.readValue(&ble_plant_health.moisture, 16) == 0 )             //TODO: Characteristics data is not being acurately read, but is accurate when looking at bluetooth through other devices
        {
          Serial.println("Failed to find our characteristic Moisture UUID");
          break;
        }
        Serial.println("Found our characteristic Moisture UUID");

        BLECharacteristic CharacteristicLight = peripheral.characteristic( charLightUUID );
        if ( CharacteristicLight.readValue(&ble_plant_health.light, 16) == 0 )
        {
          Serial.println("Failed to find our characteristic Light UUID");
          break;
        }
        Serial.println("Found our characteristic Ligh UUID");

        BLECharacteristic CharacteristicHum = peripheral.characteristic( charHumUUID );
        if ( CharacteristicHum.readValue(&ble_plant_health.humidity, 16) == 0 )
        {
          Serial.println("Failed to find our characteristic Humidity UUID");
          break;
        }
        Serial.println("Found our characteristic Humidity UUID");

        BLECharacteristic CharacteristicTemp = peripheral.characteristic( charTempUUID );
        if ( CharacteristicTemp.readValue(&ble_plant_health.temp, 16) == 0 )
        {
          Serial.println("Failed to find our characteristic Temperature UUID");
          break;
        }
        Serial.println("Found our characteristic Temperature UUID");

        Serial.print("Humidity:");
        Serial.println(ble_plant_health.humidity);
        Serial.print("Light:");
        Serial.println(ble_plant_health.light);
        Serial.print("Moisture:");
        Serial.println(ble_plant_health.moisture);
        Serial.print("Temperature:");
        Serial.println(ble_plant_health.temp);
        updated = true;
      }
      state++;
      break;
    case BLE_STATE_END:
      state = BLE_STATE_OFF;
      BLE.end();
      bleActive = false;
      updateWeb = true;
      Serial.println( "BLE end" );
      break;
    default:
      state = BLE_STATE_OFF;
      BLE.end();
      bleActive = false;
      Serial.println( "BLE end" );
      break;
  }
}

void setupWifi ( void ){
  Serial.println("Setting WIFI");
  if (!BLE.begin()) {
    Serial.println("starting Bluetooth® Low Energy module failed!");

    while (1);
  }
  BLE.setDeviceName("Wifi Setup");
  BLE.setLocalName("SP10 Wifi Setup");
  BLEService SetupWiFiService("19B10000-E8F2-537E-4F6C-D104768A1214");
  pCharacteristicSSID.setValue("Set SSID");
  pCharacteristicPass.setValue("Set Pass");
  char done = (char) 0;
  pCharacteristicDone.setValue(&done);
  SetupWiFiService.addCharacteristic(pCharacteristicSSID);
  SetupWiFiService.addCharacteristic(pCharacteristicPass);
  SetupWiFiService.addCharacteristic(pCharacteristicDone);
  BLE.setAdvertisedService(SetupWiFiService);
  BLE.addService(SetupWiFiService);
  BLE.advertise();
  Serial.println( "Advertising " );
  BLEDevice central = BLE.central();
  while (central.connected()) {}
  while(done == (char) 0){
    pCharacteristicDone.readValue(&done, 1);
  }
  Serial.println( "Done Advertising " );
  pCharacteristicSSID.readValue(ssid, 32);
  pCharacteristicPass.readValue(pass, 32);
  BLE.stopAdvertise();
  BLE.end();
}

void sleepMode()
{
  if (!FuelGauge.isSleeping())
  {
    FuelGauge.sleep();

    if (FuelGauge.isSleeping())
    {
      Serial.println("Fuel Gauge put in sleep mode.");
    }
    else
    {
      Serial.println("Fuel Gauge failed to be put in sleep mode.");
    }
  }
  else
  {
    Serial.println("Fuel Gauge is already in sleep mode.");
  }
}

void wakeMode()
{
  if (FuelGauge.isSleeping())
  {
    FuelGauge.wake();

    if (!FuelGauge.isSleeping())
    {
      Serial.println("Fuel Gauge is now awake.");
    }
    else
    {
      Serial.println("Failed to wake Fuel Gauge.");
    }
  }
  else
  {
    Serial.println("Fuel Gauge is already awake.");
  }
}

void reset()
{
  FuelGauge.reset();
  Serial.println("Fuel Gauge has been reset/rebooted.");
}

void quickStart()
{
  FuelGauge.quickstart();
  Serial.println("Quick start has been initiated on the Fuel Gauge.");
}

void PeriodicUpdate(){
  wakeMode();
  voltage = FuelGauge.voltage();
  sleepMode();
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
