/*
  Tank code
  Handles connecting the the probe bluetooth signal and sending it to the server
*/


//----------------------------------------------------------------------------------------------------------------------
// WiFi
//----------------------------------------------------------------------------------------------------------------------

//Bluetooth Wifi Setup
//----------------------------------------------------------------------------------------------------------------------




//For Ultrasonic
int sensorLoop = 0;
const int trigPin = 2;
const int echoPin = 3;
long duration;
int distance;

int moistureCutoff = 2775;
int delayTime = 10;

//----------------------------------------------------------------------------------------------------------------------
// App
//----------------------------------------------------------------------------------------------------------------------


int pumpPin = 8;              //TODO: Change pumpPin to what the pumpPin will be
int pumpActiveLength = 2;    //in seconds
int pumpActiveTimeRemaining;    //This is our timer for our pump to always reference how much time is left to run, no multithreading no r/w problems (dub)


//----------------------------------------------------------------------------------------------------------------------
// I/O
//----------------------------------------------------------------------------------------------------------------------

void setup()
{
  delay(2000);
  Serial.begin( 9600 );
  delay(2000);

  Serial.println( "Tank Code Setup" );

  pinMode(pumpPin, OUTPUT);

  Serial.println( "Tank Code Starting" );
}


void loop()
{
  Serial.println( "Delay for Pump" );
  delay(20000);
  
  Serial.println( "Pump On" );
                             //TODO: uncomment this block text, change pumpPin into the pumpPin ammount, maybe change for loop amount
  pumpEnable(10);
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
      Serial.println( "Pump Low" );
      digitalWrite(pumpPin, LOW);
      delayMicroseconds(1000 - dutyCycle);
      pumpActiveTimeRemaining--;
    }
}

