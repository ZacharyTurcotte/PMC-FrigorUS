#include <Arduino.h>
#include "mcp2515.h"
#include "thermistance.h"

struct can_frame canMsg;
MCP2515 mcp2515(53);

int n;
float buff_temp[5];

Thermistance thermistance0;
Thermistance thermistance1;
Thermistance thermistance2;
Thermistance thermistance3;
Thermistance thermistance4;

void setup() {
  
  Serial.begin(115200);
  /*
  mcp2515.reset();
  mcp2515.setBitrate(CAN_125KBPS);
  mcp2515.setNormalMode();
  
  //Serial.println("------- CAN Ready ----------");
  //Serial.println("ID  DLC   DATA");
    //Serial.print("#1 #2 #3 #4 #5 \n");
  */
  n = 0;
  buff_temp[0] = 0;
  buff_temp[1] = 0;
  buff_temp[2] = 0;
  buff_temp[3] = 0;
  buff_temp[4] = 0;

  thermistance0.init_thermistance(A0);
  thermistance1.init_thermistance(A1);
  thermistance2.init_thermistance(A2);
  thermistance3.init_thermistance(A3);
  thermistance4.init_thermistance(A4);

}

void loop() {

  Serial.print(n);
  Serial.print(',');
  n++;
  buff_temp[0] = thermistance0.get_temperature();
  buff_temp[1] = thermistance1.get_temperature();
  buff_temp[2] = thermistance2.get_temperature();
  buff_temp[3] = thermistance3.get_temperature();
  buff_temp[4] = thermistance4.get_temperature();
  
  for(int i = 0;i<=4;i++)
  {

    Serial.print(buff_temp[i]);
    Serial.print(',');
  }
    Serial.print('\n');
    delay(500);

}