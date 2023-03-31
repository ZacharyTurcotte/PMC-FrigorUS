import spidev
import MCP3008_IP
import time
import CAN_RPI
import thermistance
from gpiozero import LED
import tkinter as tk
import random 
def init_SPI(bus,CS,max_speed):
	spi = spidev.SpiDev()
	spi.open(bus,CS)
	spi.max_speed_hz = max_speed
	return spi

def draw_square():
	nb_case = 65
	w = tk.Canvas(window,width=200, height=700,)
	temp = random.randint(0,65)
	nb_square = int(temp/(65/nb_case))
	gap = 700/nb_case
	print(nb_square)
	x0 = 0
	y0 = 0
	x1 = 200
	y1 = gap
	for x in range(nb_square):
		w.create_rectangle(x0, y0, x1, y1,fill="red",outline = "black")
		y0 = y1
		y1 = y1 + gap
		
		
	for x in range(nb_case -nb_square):
		w.create_rectangle(x0,y0,x1,y1,fill="green",outline= "black")
		y0 = y1
		y1 = y1 + gap
	w.grid(row=1,column=0)
	

def do_stuff():
	
	temp = thermistance_ntc.get_temperature(7)
	title0.config(text="temperature du pack : " + str(int(temp)))
	draw_square()
	title0.after(1000,do_stuff)
	
	
	
def main():
	
	global title0
	global thermistance_ntc
	global temp 
	global window
	temp = 0
	spi = init_SPI(0,1,2000000)
	thermistance_ntc = thermistance.thermistance_NTC(5,22,spi)
	

	window = tk.Tk()
	window.configure(bg="white")
	window.geometry("1920x1080")
	title0 = tk.Label(window,text="Temperature du pack : " + str(temp), bg = "white")
	title0.grid(row=0,column=0)
	
	window.after(1,do_stuff)
	draw_square()
	window.mainloop()

#MCP3008 = MCP3008_IP.MCP3008_IP(5,22) # mettre le Vref en input
#spi = init_SPI(0,1,2000000) # mettre le bus, le CS et le max speed
#thermistance_ntc = thermistance.thermistance_NTC(5,22,spi)
#led = LED(27)

if __name__ == "__main__":
	main()

		
#CAN_BUS = CAN_RPI.CAN_driver('can0',250000) 
#on vas voir ressource busy dans le terminal mais c'est pas grave
#car si le can bus est déja a high, yé pas content, faut reboot pour 
#enlever le message

#CAN_BUS.send_can_data_frame(0x123,[0,1,2,3,4,5,6,7])
#msg = CAN_BUS.send_remote_frame(0x123)

