#script de test pour le raspberry Pi

import spidev
import time 

from CAN_RPI import CAN_driver
from MCP23017 import MCP23017
from PCA85073ADP import PCA85073ADP

def init_SPI(bus,CS,max_speed):
	spi = spidev.SpiDev()
	spi.open(bus,CS)
	spi.max_speed_hz = max_speed
	return spi


def main():
	spi = init_SPI(0,1,2000000) # mettre le bus, le CS et le max speed
	CAN_BUS = CAN_RPI.CAN_driver('can0',250000) 
    IO_expender = PCA85073ADP.__init__()
    
    
    
if __name__ == "__main__":
	main()
