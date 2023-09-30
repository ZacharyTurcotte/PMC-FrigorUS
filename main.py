import spidev

import MCP3008_IP
import time
import CAN_RPI
import thermistance

from gpiozero import LED
import tkinter as tk
from PIL import ImageTk, Image
import random 

def init_SPI(bus,CS,max_speed):
	spi = spidev.SpiDev()
	spi.open(bus,CS)
	spi.max_speed_hz = max_speed
	return spi

def draw_temp(pos_x,pos_y,temp): #r is the row and col is the col
	nb_case = 31
	height = 400
	width = 100
	w = tk.Canvas(window,width=width+100, height=height+20,)
	delta_t = 5
	delta_t_pixel = int(height/15)
	#temp = thermistance_ntc.get_single_temperature(0)
	
	
	
	w.create_rectangle(0,0,width+100, height+20,fill="light blue",outline="black")
	if temp > 0:
		
		x0 = 0+10
		y0 = 0+10
		x1 = width+10
		y1 = delta_t_pixel+10
		
		nb_red_square = int(temp/delta_t)
		
		nb_green_square = ((nb_case-1)/2) - nb_red_square
		
		for x in range(int(nb_green_square)):
			w.create_rectangle(x0+35,y0,x1+35,y1,fill="azure",outline="black")
			y0 = y1
			y1 = y1+delta_t_pixel
			 
		for x in range(nb_red_square):
			w.create_rectangle(x0+35,y0,x1+35,y1,fill="red",outline="black")
			y0 = y1
			y1 = y1+delta_t_pixel
		
		
	label0 = tk.Label(window,text="0C", bg = "light blue")
	label1 = tk.Label(window,text="5C", bg = "light blue")
	label2 = tk.Label(window,text="10C", bg = "light blue")
	label3 = tk.Label(window,text="15C", bg = "light blue")
	label4 = tk.Label(window,text="20C", bg = "light blue")
	label5 = tk.Label(window,text="25C", bg = "light blue")
	label6 = tk.Label(window,text="30C", bg = "light blue")
	label7 = tk.Label(window,text="35C", bg = "light blue")
	label8 = tk.Label(window,text="40C", bg = "light blue")
	
	label0.place(x=pos_x,y=pos_y+390)
	label1.place(x=pos_x,y=pos_y+365)
	label2.place(x=pos_x,y=pos_y+340)
	label3.place(x=pos_x,y=pos_y+315)
	label4.place(x=pos_x,y=pos_y+290)
	label5.place(x=pos_x,y=pos_y+260)
	
	w.place(x=pos_x,y=pos_y)

def draw_autonomie(autonomie):
	label_autonomie = tk.Label(canvas_autonomie,text = autonomie,bg="light blue",font= ("Helvetica",20,"bold"))

def draw_SoC(SoC,pos_x,pos_y):
	nb_case = 10
	height = 400
	width = 100
	w = tk.Canvas(window,width=width+50, height=height+20)
	delta_SoC = 10
	delta_SoC_pixel = 40
	#temp = thermistance_ntc.get_single_temperature(0)
	SoC = 55
	
	
	w.create_rectangle(0,0,width+50, height+20,fill="light blue",outline="light blue")
	
		
	x0 = 0+10
	y0 = 0+10
	x1 = width+10
	y1 = delta_SoC_pixel+10
		
	nb_red_square = int(SoC/delta_SoC)
	
	nb_green_square = ((nb_case)) - nb_red_square
		
	for x in range(int(nb_green_square)):
		w.create_rectangle(x0+10,y0,x1+10,y1,fill="azure",outline="black")
		y0 = y1
		y1 = y1+delta_SoC_pixel
			
	for x in range(nb_red_square):
		w.create_rectangle(x0+10,y0,x1+10,y1,fill="red",outline="black")
		y0 = y1
		y1 = y1+delta_SoC_pixel
		
		
	label0 = tk.Label(window,text="10%", bg = "light blue")
	label1 = tk.Label(window,text="20%", bg = "light blue")
	label2 = tk.Label(window,text="30%", bg = "light blue")
	label3 = tk.Label(window,text="40%", bg = "light blue")
	label4 = tk.Label(window,text="50%", bg = "light blue")
	label5 = tk.Label(window,text="60%", bg = "light blue")
	label6 = tk.Label(window,text="70%", bg = "light blue")
	label7 = tk.Label(window,text="80%", bg = "light blue")
	label8 = tk.Label(window,text="90%", bg = "light blue")
	label9 = tk.Label(window,text="100%", bg = "light blue")
	label10 = tk.Label(window,text="0%", bg = "light blue")

	label0.place(x=pos_x-15,y=pos_y+380)
	label1.place(x=pos_x-15,y=pos_y+340)
	label2.place(x=pos_x-15,y=pos_y+300)
	label3.place(x=pos_x-15,y=pos_y+265)
	label4.place(x=pos_x-15,y=pos_y+215)
	label5.place(x=pos_x-15,y=pos_y+180)
	label6.place(x=pos_x-15,y=pos_y+140)
	label7.place(x=pos_x-15,y=pos_y+100)
	label8.place(x=pos_x-15,y=pos_y+60)
	label9.place(x=pos_x-25,y=pos_y+20)
	label10.place(x=pos_x-15,y=pos_y+400)
	
	w.place(x=pos_x,y=pos_y)
	
	
def do_stuff():
	led.on()
	temp = thermistance_ntc.get_single_temperature(1)
	#temp = thermistance_ntc.thermistance_ntc(7)
	#print(thermistance_ntc.get_single_temperature(7))
	title0.config(text="Temperature du pack : " + str(int(temp)))
	draw_temp(30,60,temp)
	draw_SoC(50,210,60)
	draw_autonomie("12:00")
	#draw_square(150,15)
	title0.after(1000,do_stuff)
	led.off()

	
	
def main():
	
	global title0
	global title1
	global thermistance_ntc
	global temp 
	global window
	global led 
	global Font 
	global canvas_autonomie
	global label_autonomie
	global canvas_error
	
	
	Font = ("Helvetica",12,"bold")
	
	
	led = LED(24)
	
	spi = init_SPI(0,1,2000000)
	thermistance_ntc = thermistance.thermistance_NTC(5,22,spi)
	
	#init de la window de tkinter
	window = tk.Tk()
	window.configure(bg="steel blue")
	#window.geometry("1920x1080")
	window.geometry("960x540")
	window.overrideredirect(False) #permet d'enlever le contour
	window.wm_attributes('-fullscreen',False)
	window.wm_attributes('-zoomed',False)
	image_bg = Image.open("/home/zacharyt2301/Documents/image/blue.png")
	image_bg = ImageTk.PhotoImage(image_bg)
	
	canvas_bg = tk.Canvas(window,width=1920,height=1080)
	canvas_bg.create_image(0,0,image=image_bg,anchor="nw")
	canvas_bg.place(x=0,y=0)
	
	temp = 0
	#init des titles et la loop qui fait des choses
	title0 = tk.Label(window,text="Temperature du pack : " + str(temp), bg = "light blue",font=Font)
	title0.place(x=15,y=20)
	
	title1 = tk.Label(window,text="État de charge", bg = "light blue", font = Font)
	title1.place(x=240,y=20)
	
	#load image utisées
	#image = Image.open("/home/zacharyt2301/Documents/image/logo_transit.png")
	image_frigo = Image.open("/home/zacharyt2301/Documents/image/new_xd.png")
	
	
	#manipulation image transit et frigorUS
	#resize = image.resize((151,61))
	#img = ImageTk.PhotoImage(resize)
	resize = image_frigo.resize((509,240))
	image_frigo_resize = ImageTk.PhotoImage(resize)
	#image_frigo2 = ImageTk.PhotoImage(image_frigo_resize)
	#canvas_transit = tk.Canvas(window,width=,height=61)
	#canvas_transit.create_image(0,0,image = img,anchor='nw')
	#canvas_transit.place(x=500+309,y=200)
	
	canvas_frigo = tk.Canvas(window,bg="light blue",width=509,height=240,bd=0)
	canvas_frigo.create_image(0,0,image=image_frigo_resize,anchor='nw')
	canvas_frigo.place(x=420,y= 240)
	
	title_time = tk.Label(window,text="Autonomie de la batterie (temps)",bg="light blue",font=Font)
	title_error = tk.Label(window,text="Erreur/Problème",bg="light blue",font=Font)
	
	title_time.place(x=420,y=20)
	title_error.place(x=780,y=20)
	
	canvas_autonomie = tk.Canvas(window,bg="light blue",width = 250,height=150)
	canvas_autonomie.place(x=420,y=60)
	
	label_autonomie = tk.Label(canvas_autonomie,text="12:00",fg="red",bg="light blue",font= ("Courier",60,"bold"))
	label_autonomie.place(x=5,y=45)
	
	canvas_error = tk.Canvas(window,bg="light blue",width=130,height=150,bd=0)
	canvas_error.place(x=780,y=60)
	#360 on est colle sur les carre blue
	#panel = tk.Label(window, image = img)
	#panel.grid(row=2,column=2)
	#panel.place(x=500,y=500)
	led.on()
	print(led)
	#time.sleep(10)
	window.after(1,do_stuff)
	
	#draw_square()
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

