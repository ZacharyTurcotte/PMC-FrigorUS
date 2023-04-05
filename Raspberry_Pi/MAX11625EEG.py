import spidev
from gpiozero import LED # pour le CS, marche mieux que les autres!
import time

class MAX11625EEG:
	
#public 

	def __init__(self,New_Vref,CS_pin,spi):

		self.Vref = New_Vref
		self.Cs_pin = CS_pin #Si on utilise un chip select non officiel. 
		self.spi = spi # on assigne le spi qu'on a unit dans le main.
		self.Nb_channel = 16
		spi.xfer2([0b00011000]) # clear FIFO
		spi.writebytes([0b00100000]) # config averager
		spi.writebytes([0b01100100]) # config setup bit 5 et 4 10
		

	def read_adc_SE(self,channel):
		
		if (channel >= 16 or channel < 0):
			raise ValueError("Choisiser une channel valide")
		#self.__CS_LOW()		
		mask1 = 0b10000110
		mask2 = channel*16
		#spi.writebytes([mask1])
		#val = spi.readbytes(2)
		val = self.spi.xfer2([1,mask1,0])
		data = (val[0] << 6)|val[1]>>2

		return self.__convert_bit_to_analog(data)
	
	
	def read_adc_DE(self,channel1,channel2,spi):
		self.__CS_LOW()
		#marche moyen lol, plus simle faire 2 lectures
		if abs(channel1-channel2) != 1:
			raise ValueError("Choisier deux channels compatible")
		
		bit_serie = 16*channel1
		val = spi.xfer3([1, bit_serie,0])
		print(val)
		data = (((val[1]&3) << 8) + val[2]) 
		print(data)
		self.__CS_HIGH()
		
		return self.__convert_bit_to_analog(data)
	

	def read_all_channel(self):

		out = [0]*16
		mask0 = 0b10000110
		
		for i in range(15):
			
			mask1 = i<<3
			val = self.spi.xfer2([1,mask0|mask1,0])
			out[i] = self.__convert_bit_to_analog((val[0] << 6)|(val[1] >> 2))
			
		return out
		

	def reset_ADC(self):

		self.spi.writebytes([0b00010000]) # reset config of the ADC
#private


	def __convert_bit_to_analog(self,data):

		return data*self.Vref/1024


	def __CS_LOW(self): # sert de CS

		self.led.off()


	def __CS_HIGH(self):# sert de CS

		self.led.on()


