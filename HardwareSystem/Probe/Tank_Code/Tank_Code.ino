/*
  Tank code
  Handles connecting the the probe bluetooth signal and sending it to the server
*/

#include <SPI.h>
#include <ArduinoBLE.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>

//----------------------------------------------------------------------------------------------------------------------
// WiFi
//----------------------------------------------------------------------------------------------------------------------

///////TODO: Put Wifi Username and Password
char ssid[32] = "SP10"; //Need to be 2 GHz
char pass[32] = "319valvano"; //INSERT WIFI PASSWORD;         //Change wifi password
char* systemID = "a2h87hd1";

//TODO: Update serverName

const char* IP = "http://192.168.137.7:5000";
char serverName[70];
char getServerName[70];


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
//Plant Data
//----------------------------------------------------------------------------------------------------------------------

typedef struct __attribute__( ( packed ) )
{
  uint32_t moisture;
  float temp;
  uint32_t light;
  float humidity;
} plant_health;

plant_health ble_plant_health;

//----------------------------------------------------------------------------------------------------------------------
//Sensor Data
//----------------------------------------------------------------------------------------------------------------------

#define batteryLevelPin A6
int batteryLevel;

//For Ultrasonic
int sensorLoop = 0;
const int trigPin = 2;
const int echoPin = 3;
long duration;
int tankLevel;

int moistureCutoff = 2780;
int delayTime = 10;

//----------------------------------------------------------------------------------------------------------------------
// App
//----------------------------------------------------------------------------------------------------------------------

bool updateWeb = true;
bool updateHealth = true;
bool wifiActive = false;
bool bleActive = false;
bool updated = false;
bool WiFisetup = false;
bool delayStart = false;

int pumpPin = 8;              //TODO: Change pumpPin to what the pumpPin will be
int pumpActiveLength = 2;    //in seconds
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
  

  Serial.begin( 9600 );
  delay(2000);

  Serial.println( "Tank Code Setup" );

  strcat(serverName, IP);
  strcat(serverName, "/data");

  strcat(getServerName, IP);
  strcat(getServerName, "/GetInstructions?systemID=");
  strcat(getServerName, systemID);
  
  pinMode(pumpPin, OUTPUT);

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

  Serial.println( "Tank Code Starting" );
}

void loop()
{  
  delayStart = false;

  bleTask();

  if((ble_plant_health.moisture > moistureCutoff) && (updated == true)){
    updated = false;
    Serial.println( "Pump On" );
    pumpEnable(pumpActiveLength);
  }

  if(sensorLoop == 0){
    Serial.println( "getting PeriodicUpdate" );
    PeriodicUpdate();
  }
  sensorLoop = (sensorLoop + 1) % 10;

  wifiTask();

  delay(1000);

  if(delayStart == true){
    delay(delayTime * 60 * 1000);
  }
}


//==================================================================
//Use This one for only enabling for burst amount of seconds at a time but will be reoccuring, meaning we will constantly come back until the clock expires
#define dutyCycle 1000/2   //50% duty cycle

void pumpEnable(int seconds)
{
  pumpActiveTimeRemaining = seconds * 1000;
  while((pumpActiveTimeRemaining != 0) ){
    Serial.println( "Pump High" );
    digitalWrite(pumpPin, HIGH);
    delayMicroseconds(dutyCycle);
    pumpActiveTimeRemaining--;
  }
  digitalWrite(pumpPin, LOW);
}

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
      http.begin(client, serverName);

      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST("{\"systemID\":\"" + String(systemID) + "\",\"tank_level\":" + String(tankLevel) + ",\"battery_level\":" + String (batteryLevel) + ",\"probes\":[{\"moisture\":" + String(ble_plant_health.moisture) + ",\"temp\":" + String(ble_plant_health.temp) + ",\"light\":" + String(ble_plant_health.light) + ",\"humidity\":" + String(ble_plant_health.humidity) + "}]}");

      //httpResponseCode = http.POST(httpRequestData);
      Serial.println( "http posted" );
      http.end();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      if(httpResponseCode == 500){
        state = WIFI_STATE_SEND;
        break;
      }
      state++;
      break;
    }
    case WIFI_STATE_RECIEVE:
    {
      http.begin(client, getServerName);
      //int httpResponseCode = http.POST("{\"systemID\":\"" + String(systemID) + "\}");
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
        state++;
        break;
      }
      // Free resources
      http.end();

      Serial.println(payload);
      JSONVar myObject = JSON.parse(payload);

      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        state++;
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
      if(sensorReadingsArr[0] == -1){
        Serial.println( "Device not registered by server" );
        state++;
        break;
      }
      delayTime = sensorReadingsArr[0];
      Serial.print("2 = ");
      Serial.println(sensorReadingsArr[1]);
      moistureCutoff = sensorReadingsArr[1];
      Serial.print("3 = ");
      Serial.println(sensorReadingsArr[2]);
      pumpActiveLength = sensorReadingsArr[2];
      Serial.print("4 = ");
      Serial.println(sensorReadingsArr[3]);
      pumpEnable(sensorReadingsArr[3]);
      state++;
      break;
    }
    case WIFI_STATE_END:
      state = WIFI_STATE_OFF;
      wifiConnectTry = 0;
      wifiStatus = WL_IDLE_STATUS;
      WiFi.disconnect();
      wifiActive = false;
      updateHealth = true;
      delayStart = true;
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

void PeriodicUpdate(){
  batteryLevel = analogRead(batteryLevelPin);
  Serial.print("Battery Level: ");
  Serial.println(batteryLevel);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  tankLevel = duration * 0.034 / 2;
  Serial.print("Tank Level: ");
  Serial.println(tankLevel);
}
