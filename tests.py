#script de test pour le raspberry Pi

import spidev
import time 
import logging
from gpiozero import LED
import serial

from CAN_RPI import CAN_driver
from MCP23017 import MCP23017
from PCA850073ADP import PCA850073ADP
from MAX11625EEG import MAX11625EEG
from MCP23017 import MCP23017
from MCP3008_IP import MCP3008_IP
from thermistance import thermistance_NTC

def init_SPI(bus,CS,max_speed):
	spi = spidev.SpiDev()
	spi.open(bus,CS)
	spi.max_speed_hz = max_speed
	return spi

def main():
	spi = init_SPI(0,1,2000000) # mettre le bus, le CS et le max speed
	#CAN_BUS = CAN_driver('can0',250000)
	led = LED(24)
	led.on()
	RTC_timer = PCA850073ADP()
	RTC_timer.write_datetime(23,12,1,31,23,59,58)
	#ADC = MAX11625EEG(3.3,2,spi)
	IO_Exp = MCP23017()
	Thermistance = thermistance_NTC(3.3,2,spi)
	IO_Exp.write_all_pin(0b11111111,0b11111111)
	#IO_Exp.write_all_pin(0b00000000,0b00000000)
	#true_ADC = MCP3008_IP(5,1)
	while(True): 
		print(RTC_timer.read_datetime())
		#print(Thermistance.get_all_temperature())
		#print(ADC.read_adc_SE(1,spi))
		#CAN_BUS.send_can_data_frame(0x123,[1,2])
		#CAN_BUS.send_remote_frame(0x00000123)
		#time.sleep(1)
		#IO_Exp.write_all_pin(0b01001000,0b00010010)
		#(ADC.read_all_channel())
		#print(ADC.read_adc_SE(0,spi))
		#ADC.reset_ADC()
		#print(IO_Exp.read_all_pin())
		#print(true_ADC.read_adc_SE(0,spi))
		#print("XD")
		
		#if x == '1':
		IO_Exp.write_all_pin(0b11111111,0b11111111)
		time.sleep(5)
		#else:
		#led.off()
		IO_Exp.write_all_pin(0b00000000,0b00000000)
		
		time.sleep(5)
		#led.on()
		#IO_Exp.write_all_pin(0b00000000,0b00000000)
		#time.sleep(5)
		#IO_Exp.write_all_pin(0b00000001,0b00000000)
		
		#time.sleep(0.1)
		#IO_Exp.write_all_pin(0b00000010,0b00000000)
		
		#time.sleep(0.1)
		#IO_Exp.write_all_pin(0b00000100,0b00000000)
		
		#time.sleep(0.1)
		#IO_Exp.write_all_pin(0b00000010,0b00000000)
		#time.sleep(1) 
		#IO_Exp.write_all_pin(0b00000001,0b00000000)
		
		
if __name__ == "__main__":
	main()

