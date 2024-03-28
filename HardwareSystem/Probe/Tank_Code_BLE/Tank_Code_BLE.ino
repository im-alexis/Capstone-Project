/**
 * A BLE client example that is rich in capabilities.
 * There is a lot new capabilities implemented.
 * author unknown
 * updated by chegewara
 */

#include "BLEDevice.h"
//#include "BLEScan.h"

// The remote service we wish to connect to.
static BLEUUID serviceUUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b");
// The characteristic of the remote service we are interested in.
static BLEUUID    charUUID("beb5483e-36e1-4688-b7f5-ea07361b26a8");
static BLEUUID    charMoistUUID("fb6cf981-31cc-4f36-af06-1f2f3e919840");// use the same UUID as on the server
static BLEUUID    charTempUUID("35b17f66-73d1-4c92-92f6-9032ef1987d3");
static BLEUUID    charLightUUID("3cab9341-e65b-46e9-83ed-c8a7f2f841c2");
static BLEUUID    charHumUUID("f3b857d0-1e8a-4dff-a941-9ea9a3594275");
//#define CHARACTERISTIC_ACC_UUID 
static boolean doConnect = false;
static boolean connected = false;
static boolean doScan = false;
static BLERemoteCharacteristic* pRemoteCharacteristic;
static BLERemoteCharacteristic* pRemoteCharacteristicMoist;
static BLERemoteCharacteristic* pRemoteCharacteristicTemp;
static BLERemoteCharacteristic* pRemoteCharacteristicLight;
static BLERemoteCharacteristic* pRemoteCharacteristicHum;
static BLEAdvertisedDevice* myDevice;

int moisture, temp, light, humidity;

static void notifyCallback(
  BLERemoteCharacteristic* pBLERemoteCharacteristic,
  uint8_t* pData,
  size_t length,
  bool isNotify) {
    Serial.print("Notify callback for characteristic ");
    Serial.print(pBLERemoteCharacteristic->getUUID().toString().c_str());
    Serial.print(" of data length ");
    Serial.println(length);
    Serial.print("data: ");
    Serial.println((char*)pData);
}

class MyClientCallback : public BLEClientCallbacks {
  void onConnect(BLEClient* pclient) {
  }

  void onDisconnect(BLEClient* pclient) {
    connected = false;
    Serial.println("onDisconnect");
  }
};

bool connectToServer() {
    Serial.print("Forming a connection to ");
    Serial.println(myDevice->getAddress().toString().c_str());

    BLEClient*  pClient  = BLEDevice::createClient();
    Serial.println(" - Created client");

    pClient->setClientCallbacks(new MyClientCallback());

    // Connect to the remove BLE Server.
    pClient->connect(myDevice);  // if you pass BLEAdvertisedDevice instead of address, it will be recognized type of peer device address (public or private)
    Serial.println(" - Connected to server");
    pClient->setMTU(517); //set client to request maximum MTU from server (default is 23 otherwise)

    // Obtain a reference to the service we are after in the remote BLE server.
    BLERemoteService* pRemoteService = pClient->getService(serviceUUID);
    if (pRemoteService == nullptr) {
      Serial.print("Failed to find our service UUID: ");
      Serial.println(serviceUUID.toString().c_str());
      pClient->disconnect();
      return false;
    }
    Serial.println(" - Found our service");

    // Obtain a reference to the characteristic in the service of the remote BLE server.
    pRemoteCharacteristic = pRemoteService->getCharacteristic(charUUID);
    if (pRemoteCharacteristic == nullptr) {
      Serial.print("Failed to find our characteristic UUID: ");
      Serial.println(charUUID.toString().c_str());
      pClient->disconnect();
      return false;
    }
    Serial.println(" - Found our characteristic");
    //Moisture Obtain a reference to the characteristic in the service of the remote BLE server.
    pRemoteCharacteristicMoist = pRemoteService->getCharacteristic(charMoistUUID);
    if (pRemoteCharacteristicMoist == nullptr) {
      Serial.print("Failed to find our characteristic Moisture: ");
      Serial.println(charMoistUUID.toString().c_str());
      pClient->disconnect();
      return false;
    }
    Serial.println(" - Found Moisture");
 //Temp Obtain a reference to the characteristic in the service of the remote BLE server.
    pRemoteCharacteristicTemp = pRemoteService->getCharacteristic(charTempUUID);
    if (pRemoteCharacteristicTemp == nullptr) {
      Serial.print("Failed to find our characteristic Temp: ");
      Serial.println(charTempUUID.toString().c_str());
      pClient->disconnect();
      return false;
    }
    Serial.println(" - Found Temperature");
     //Light Obtain a reference to the characteristic in the service of the remote BLE server.
    pRemoteCharacteristicLight = pRemoteService->getCharacteristic(charLightUUID);
    if (pRemoteCharacteristicLight == nullptr) {
      Serial.print("Failed to find our characteristic Light: ");
      Serial.println(charLightUUID.toString().c_str());
      pClient->disconnect();
      return false;
    }
    Serial.println(" - Found Light");

    pRemoteCharacteristicHum = pRemoteService->getCharacteristic(charHumUUID);
    if (pRemoteCharacteristicHum == nullptr) {
      Serial.print("Failed to find our characteristic Humidity: ");
      Serial.println(charHumUUID.toString().c_str());
      pClient->disconnect();
      return false;
    }
    Serial.println(" - Found Humidity");

    // Read the value of the characteristic.
    if(pRemoteCharacteristic->canRead()) {
      std::string value = pRemoteCharacteristic->readValue();
      Serial.print("The characteristic value was: ");
      Serial.println(value.c_str());
    }

    if(pRemoteCharacteristic->canNotify())
      pRemoteCharacteristic->registerForNotify(notifyCallback);

    connected = true;
    return true;
}
/**
 * Scan for BLE servers and find the first one that advertises the service we are looking for.
 */
class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
 /**
   * Called for each advertising BLE server.
   */
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    Serial.print("BLE Advertised Device found: ");
    Serial.println(advertisedDevice.toString().c_str());

    // We have found a device, let us now see if it contains the service we are looking for.
    if (advertisedDevice.haveServiceUUID() && advertisedDevice.isAdvertisingService(serviceUUID)) {

      BLEDevice::getScan()->stop();
      myDevice = new BLEAdvertisedDevice(advertisedDevice);
      doConnect = true;
      doScan = true;

    } // Found our server
  } // onResult
}; // MyAdvertisedDeviceCallbacks


void setup() {
  Serial.begin(115200);
  Serial.println("Starting Arduino BLE Client application...");
  BLEDevice::init("");

  // Retrieve a Scanner and set the callback we want to use to be informed when we
  // have detected a new device.  Specify that we want active scanning and start the
  // scan to run for 5 seconds.
  BLEScan* pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setInterval(1349);
  pBLEScan->setWindow(449);
  pBLEScan->setActiveScan(true);
  pBLEScan->start(5, false);
} // End of setup.


// This is the Arduino main loop function.
void loop() {

  // If the flag "doConnect" is true then we have scanned for and found the desired
  // BLE Server with which we wish to connect.  Now we connect to it.  Once we are 
  // connected we set the connected flag to be true.
  if (doConnect == true) {
    if (connectToServer()) {
      Serial.println("We are now connected to the BLE Server.");
    } else {
      Serial.println("We have failed to connect to the server; there is nothin more we will do.");
    }
    doConnect = false;
  }

  // If we are connected to a peer BLE Server, update the characteristic each time we are reached
  // with the current time since boot.
  if (connected) {
    String newValue = "Time since boot: " + String(millis()/1000);
    //Serial.println("Setting new characteristic value to \"" + newValue + "\"");

    // Set the characteristic's value to be the array of bytes that is actually a string.
   // pRemoteCharacteristic->writeValue(newValue.c_str(), newValue.length());//***********JKO
  }else if(doScan){
    BLEDevice::getScan()->start(0);  // this is just example to start scan after disconnect, most likely there is better way to do it in arduino
  }


// read the Characteristics and store them in a variable
// This also makes the print command do float handling
moisture = pRemoteCharacteristicMoist->readUInt32();
temp = pRemoteCharacteristicTemp->readUInt32();
light = pRemoteCharacteristicLight->readUInt32();
humidity = pRemoteCharacteristicHum->readUInt32();
Serial.print(moisture);
Serial.print("\t");
Serial.print(temp);
Serial.print("\t");
Serial.println(light);
Serial.print("\t");
Serial.println(humidity);

delay(100); // Delay a 100 ms between loops. 
} // End of loop
