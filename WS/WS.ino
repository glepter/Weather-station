/*
 * This is the Arduino sketch for the Weather station project.
 * 
 * find more at: https://github.com/glepter/Weather-station
 * 
 */

 
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
        Serial.readString(); 
        Serial.write('K');
        Serial.readString(); 
        break;
      }
      else{
        //clear serial buffer
        while(Serial.available() > 0){
          Serial.readString();
        }
      }
      //clear serial buffer
      while(Serial.available() > 0){
        Serial.readString();
      }   
    }
    delay(300);
  }
  
  
}

void loop() {
  /*TODO:
   * Make route to wait for request and collect and send data over serial upon request
   * 
   */
}
