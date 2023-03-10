#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg1;
struct can_frame canMsg2;
MCP2515 mcp2515(10);


void setup() {
  canMsg1.can_id  = 0x0F6; //CAN ID
  canMsg1.can_dlc = 8; // Longeur du message 
  canMsg1.data[0] = 0x8E; // message
  canMsg1.data[1] = 0x87;
  canMsg1.data[2] = 0x32;
  canMsg1.data[3] = 0xFA;
  canMsg1.data[4] = 0x26;
  canMsg1.data[5] = 0x8E;
  canMsg1.data[6] = 0xBE;
  canMsg1.data[7] = 0x86;
  
  canMsg2.can_id  = 0x036;
  canMsg2.can_dlc = 8;
  canMsg2.data[0] = 0x0E;
  canMsg2.data[1] = 0x00;
  canMsg2.data[2] = 0x00;
  canMsg2.data[3] = 0x08;
  canMsg2.data[4] = 0x01;
  canMsg2.data[5] = 0x00;
  canMsg2.data[6] = 0x00;
  canMsg2.data[7] = 0xA0;
  
  while (!Serial);
  Serial.begin(115200);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS);
  mcp2515.setNormalMode();
  
  Serial.println("°º¤ø,,ø¤º°`°º¤ø,,ø¤°º¤ø,,ø¤º°`°º¤ø CAN NODE °º¤ø,,ø¤º°`°º¤ø,,ø¤°º¤ø,,ø¤º°`°º¤ø");
}

void loop() {
  if (mcp2515.sendMessage(&canMsg1) == 0) 
  {
    Serial.println("Messages sent");
  }
  mcp2515.sendMessage(&canMsg1);
  mcp2515.sendMessage(&canMsg2);

  
  
  delay(100);
}