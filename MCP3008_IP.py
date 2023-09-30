import spidev
from gpiozero import LED # pour le CS, marche mieux que les autres!
import time

# not use anymore, test how the SPI works on the Pi

class MCP3008_IP:
	
#public 

	def __init__(self,New_Vref,CS_pin):
		self.Vref = New_Vref
		self.CS = CS_pin
		self.led = LED(self.CS)
		
	def read_adc_SE(self,channel,spi):
		
		if (channel >= 8 or channel < 0):
			raise ValueError("Choisiser une channel valide")
		self.__CS_LOW()		
		mask1 = 0b10000000
		mask2 = channel*16
		
		val = spi.xfer2([1,mask1 | mask2 ,0])
		data = (((val[1]&3) << 8) + val[2])
		self.__CS_HIGH()
		return self.__convert_bit_to_analog(data)
	
	
	def read_adc_DE(self,channel1,channel2,spi):
		self.__CS_LOW()
		#marche moyen lol, plus simle faire 2 lectures
		if abs(channel1-channel2) != 1:
			raise ValueError("Choisier deux channels compatible")
		
		bit_serie = 16*channel1
		val = spi.xfer2([1, bit_serie,0])
		print(val)
		data = (((val[1]&3) << 8) + val[2]) 
		print(data)
		self.__CS_HIGH()
		
		return self.__convert_bit_to_analog(data)
		
#private

	def __convert_bit_to_analog(self,data):
		return data*self.Vref/1024

	def __CS_LOW(self): # sert de CS
		self.led.off()

	def __CS_HIGH(self):# sert de CS
		self.led.on()
