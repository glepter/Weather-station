#include <SoftwareSerial.h>
#include "DHT.h"


#define DHTTYPE DHT11 

SoftwareSerial mySerial(10, 11); // RX, TX
DHT dht1(5, DHTTYPE);
DHT dht2(6, DHTTYPE);
DHT dht3(7, DHTTYPE);
DHT dht4(8, DHTTYPE);

int count = 0;

void setup() {
  Serial.begin(115200);
  mySerial.begin(115200);  
  dht1.begin();
  dht2.begin();
  dht3.begin();
  dht4.begin();


//wait for authentication request to be received via serial
  while(true){
    if (Serial.available() > 0){
      int lect = Serial.read();
      mySerial.print(lect);
    //test reading for authentication request, answers if found, returns otherwise
      if (lect == 'O'){ 
        while(Serial.available() > 0){
          Serial.readString();
          }
        Serial.write('K');
        delay(150);
        break;
      }
      }
      //clear serial buffer
      while(Serial.available() > 0){
        Serial.readString();
      }   
    }
  }
  
  


void loop() {
  /*TODO:
   * Make route to wait for request and collect and send data over serial upon request
   * 
   */
   delay(100);
   count ++;
   
   float a[4]={dht1.readHumidity(),dht2.readHumidity(),dht3.readHumidity(),dht4.readHumidity()};
   
   while(Serial.available() < 0){
    return;
   }
   int Order = Serial.read();
   mySerial.print(Order);
   switch(Order){
    case 'R':
        Serial.write("E");
        
        delay(200);
        for(int o=0; o<4; o++){
          int bytesSent = Serial.println(a[o]);
          delay(100);
        }
        break;
    case 'O':
        Serial.write("K");
        delay(100);
        break;
    
   }
   //clear serial buffer
        while(Serial.available() > 0){
          Serial.readString();
        }
}
