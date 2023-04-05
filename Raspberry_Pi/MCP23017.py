import smbus
import numpy as np
import time 

		
import smbus

class MCP23017:
	
	def __init__(self, address=0x20, bus=1):
		self.bus = smbus.SMBus(bus)
		self.address = address
		self.config = 0x2A
		self.__setup()
		self.live_pinA = 0x00
		self.live_pinB = 0x00


	def set_pin_mode(self, pin, mode):
        # set the mode for a given pin 
		if mode == 1:
			reg_val = self.bus.read_byte_data(self.address, 0x0A)
			reg_val &= ~(1 << pin) # set bit to 0 for output
			self.bus.write_byte_data(self.address, 0x0A, reg_val)
		else:
			reg_val = self.bus.read_byte_data(self.address, 0x0A)
			reg_val |= (1 << pin) # set bit to 1 for input
			self.bus.write_byte_data(self.address, 0x0A, reg_val)


	def write_pin(self, pin, value):
        # set the output value for a given pin
		if value == 1:
			reg_val = self.bus.read_byte_data(self.address, 0x09)
			reg_val |= (1 << pin) # set bit to 1 for high
			self.bus.write_byte_data(self.address, 0x09, reg_val)
		else:
			reg_val = self.bus.read_byte_data(self.address, 0x09)
			reg_val &= ~(1 << pin) # set bit to 0 for low
			self.bus.write_byte_data(self.address, 0x09, reg_val)
	
	
	def write_all_pin(self, pinA,pinB):
		#will write a select pin 

		self.bus.write_byte_data(self.address, 0x0A, pinA)
		self.bus.write_byte_data(self.address, 0x1A, pinB)

	
	def read_pin(self, pin):
        # read the input value for a given pin 
		reg_val = self.bus.read_byte_data(self.address, 0x09)
		return (reg_val >> pin) & 0x01


	def read_all_pin(self):
		reg_val = self.bus.read_byte_data(self.address,0x09)
		return reg_val
	
	
	def read_interrupt_pin(self):
		#read the logic level of the interrup pin when the interrupt occurs
		reg_val = self.bus.read_byte_data(self.address,0x08)
		return reg_val

	def read_random(self):
		print(self.bus.read_byte_data(self.address,0x19))

	def __setup(self):
        # I set most register even defautl value because it is subjet to change and it will be quicker later
        
        #BANKA
		self.bus.write_byte_data(self.address, 0x05, 0xAA) # set control register, bank A and B are different to control GPIO bank A and B
		#time.sleep(5/1000)
		self.bus.write_byte_data(self.address, 0x00, 0x00) # set all pins as output
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x01, 0x00) # set bit reflet same logic state
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x02, 0x00) # set no interrupt on change pins
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x03, 0x00) # set default value of each pin to 0
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x04, 0xFF) # set control register to compare the defval not use
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x06, 0x06) # set pull up register to disable (no input pin)
		#write to address 0x07 will be ignored, read only register
		#write to address 0x08 will be ignored, read only register -- reflect GPIO port value when interrupt
		self.bus.write_byte_data(self.address, 0x09, 0xFF) # set to 0 (LOW) all output
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x0A, 0xFF) # set to 0 (LOW) all output latches
		
		#BANK B
		#self.bus.write_byte_data(self.address, 0x15, 0xAA) # set control register, bank A and B are different to control GPIO bank A and B
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x10, 0x00) # set all pins as output
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x11, 0x00) # set bit reflet same logic state
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x12, 0x00) # set no interrupt on change pins
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x13, 0x00) # set default value of each pin to 0
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x14, 0xFF) # set control register to compare the defval not use
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x16, 0x06) # set pull up register to disable (no input pin)
		#time.sleep(1/1000)
		#write to address 0x17 will be ignored, read only register
		#write to address 0x18 will be ignored, read only register -- reflect GPIO port value when interrupt
		#self.bus.write_byte_data(self.address, 0x19, 0xFF) # set to 0 all 
		#time.sleep(1/1000)
		#time.sleep(1/1000)
		self.bus.write_byte_data(self.address, 0x1A, 0xFF) # set to 0 (LOW) all output latches
	
		
		
		
