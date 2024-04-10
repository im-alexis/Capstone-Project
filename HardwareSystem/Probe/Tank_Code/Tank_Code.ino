/*
  Tank code
  Handles connecting the the probe bluetooth signal and sending it to the server
*/

#include <SPI.h>
#include <ArduinoBLE.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "MAX17043.h"

//----------------------------------------------------------------------------------------------------------------------
// WiFi
//----------------------------------------------------------------------------------------------------------------------

///////TODO: Put Wifi Username and Password
char ssid[32] = "Ours 2 GHz"; //Need to be 2 GHz
char pass[32] = ""; //INSERT WIFI PASSWORD;         //Change wifi password

//----------------------------------------------------------------------------------------------------------------------
// Wifi Server
//----------------------------------------------------------------------------------------------------------------------

//TODO: Update serverName
const char* serverName = "http://192.168.1.104:5000/data";   //"http://IP_ADDRESS:5000/data"

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
int Ultraloop = 0;
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

String httpRequestData = "";
WiFiClient client;
HTTPClient http;

//----------------------------------------------------------------------------------------------------------------------
// I/O
//----------------------------------------------------------------------------------------------------------------------

void setup()
{
  Serial.println( "Setup begin" );
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

  /* Still need testgin

  if(WiFisetup == false){
    setupWifi();
    WiFisetup == true;
  }
  */

  bleTask();

  if(ble_plant_health.moisture < 12000 && updated == true){
    updated = false;
    /*                          //TODO: uncomment this block text, change pumpPin into the pumpPin ammount, maybe change for loop amount
    for(int i = 1; i < 10; i++){
      digitalWrite(pumpPin, HIGH);
      delayMicroseconds(1000/2);
      digitalWrite(pumpPin, LOW);
      delayMicroseconds(1000 - 100);
    }
    */
  }

  if(Ultraloop == 0){
    PeriodicUpdate();
  }
  Ultraloop = (Ultraloop + 1) % 5;

  wifiTask();

  delay(1000);

}


void wifiTask( void )
{
  enum WIFI_STATE_TYPE { WIFI_STATE_OFF,
                         WIFI_STATE_CONNECT,
                         WIFI_STATE_SEND,
                         WIFI_STATE_END,
                         WIFI_STATE_RESTART = 255
                       };

  static int state = WIFI_STATE_OFF;
  static int wifiConnectTry = 0;
  static int wifiStatus = WL_IDLE_STATUS;
  static int httpResponseCode = 0;
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


      /*//Testing w/ Alexis
      http.begin(client, "http://:5000/data");
      Serial.println(WiFi.localIP());
      */

      //orginal: comment out if testing
      http.begin(client, serverName);


      
      http.addHeader("Content-Type", "application/json");
      httpResponseCode = http.POST("{\"systemID\":\"a2h87hd1\",\"tank_level\":60.5,\"probes\":[{\"moisture\":" + String(ble_plant_health.moisture) + ",\"temp\":" + String(ble_plant_health.temp) + ",\"light\":" + String(ble_plant_health.light) + ",\"humidity\":" + String(ble_plant_health.humidity) + "}]}");

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

void bleTask()
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
  BLE.setDeviceName("Wifi Setup");
  BLE.begin();
  BLEService SetupWiFiService("19B10000-E8F2-537E-4F6C-D104768A1214");
  pCharacteristicSSID.setValue("Set SSID");
  pCharacteristicPass.setValue("Set Pass");
  char done[] = "0";
  pCharacteristicDone.setValue(done);
  SetupWiFiService.addCharacteristic(pCharacteristicSSID);
  SetupWiFiService.addCharacteristic(pCharacteristicPass);
  SetupWiFiService.addCharacteristic(pCharacteristicDone);
  BLE.addService(SetupWiFiService);
  BLE.advertise();
  Serial.println( "Advertising " );
  while(done[0] == char(0)){
    pCharacteristicDone.readValue(done, 1);
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
