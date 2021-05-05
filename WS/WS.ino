/*
 * This is the Arduino sketch for the Weather station project.
 * 
 * find more at: https://github.com/glepter/Weather-station
 * 
 */
int count = 0;
 
void setup() {
  Serial.begin(115200);
 // Serial1.begin(115200);

//wait for authentication request to be received via serial
  while(true){
    if (Serial.available() > 0){
      int lect = Serial.read();
    //  Serial1.print(lect);
    //test reading for authentication request, answers if found, returns otherwise
      if (lect == 'O'){ 
        while(Serial.available() > 0){
          Serial.readString();
          }
        Serial.write('K');
        delay(350);
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
   delay(300);
   count ++;
   float a[4]={5.2,40.1,3.009,2.32};
   
   while(Serial.available() < 0){
    return;
   }
   int Order = Serial.read();

   switch(Order){
    case 'R':
        Serial.write("E");
        delay(200);
        for(int o=0; o<4; o++){
          int bytesSent = Serial.println(a[o]+count*0.2*a[2]);
          delay(120);
        }
        break;
    case 'O':
        Serial.write("K");
        delay(200);
        break;
    
   }
   //clear serial buffer
        while(Serial.available() > 0){
          Serial.readString();
        }
}
