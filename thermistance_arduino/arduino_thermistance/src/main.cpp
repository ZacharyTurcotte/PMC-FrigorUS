#include <Arduino.h>
#include "mcp2515.h"

struct can_frame canMsg;
MCP2515 mcp2515(53);
int n;

void setup() {
  
  Serial.begin(115200);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_125KBPS);
  mcp2515.setNormalMode();
  
  //Serial.println("------- CAN Ready ----------");
  //Serial.println("ID  DLC   DATA");
  //Serial.print("#1 #2 #3 #4 #5 \n");
  n = 0;
}

void loop() {

  Serial.print(n);
  Serial.print(",");
  Serial.print(n+1);
  Serial.print(",");
  Serial.print(n+2);
  Serial.print(",");
  Serial.print(n+3);
  Serial.print(",");
  Serial.print(n+4);
  Serial.print(",");
  Serial.print(n+5);
  Serial.print("\n");
  n++;
  delay(500);
/*
  if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
    Serial.print(canMsg.can_id, HEX); // print ID
    Serial.print(" "); 
    Serial.print(canMsg.can_dlc, HEX); // print DLC
    Serial.print(" ");
    
    for (int i = 0; i<canMsg.can_dlc; i++)  {  // print the data
      Serial.print(canMsg.data[i],HEX);
      Serial.print(" ");
    }

    Serial.println();      
  }*/

}