import serial.tools.list_ports
import time
import csv

def save_data(data,file_name,length):
    col_name = ['N','Thermistance 0','Thermistance 1','Thermistance 2','Thermistance 3','Thermistance 4']
    f = open(file_name,'w', encoding='UTF8',newline='\n')
    for i in range(length):
        print(data[i])
        f.write(data[i])
        f.write('\n')
    f.close()
    print("données sauvé!")

def init_serial_port(port,baudrate):
    serialInstance = serial.Serial()
    serialInstance.baudrate = baudrate
    serialInstance.port = port
    serialInstance.timeout = 1
    serialInstance.open()
    return serialInstance

def calculate_time(temps):
    return time.time() - temps

ports = serial.tools.list_ports.comports()
temps_passer = 0

for COM_port in ports:
    print(str(COM_port))
#nom_port = input("Choisie le port que tu veux")
#baudrate = input("Choisie le baudrate")
#acquisition_time = input("Combient de temps l'acquisition (secondes)")
#instance = init_serial_port("COM4","115200")
temps_ini = time.time()
n = 0
data = []
instance = init_serial_port("COM4", "115200")
instance.flushInput()
while temps_passer <= int(5):

    if instance.in_waiting:
        line = instance.read_until()
        data.append((line.decode('utf').strip('\n')))
        instance.flushInput()
        n = n+1
        print(line.decode('utf').strip('\n'))
        temps_passer = calculate_time(temps_ini)

save_data(data,"test_frigo.csv",n)

print("done")
