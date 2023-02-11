import serial.tools.list_ports
import time


def save_data(data, file_name, length):
    col_name = ['N', 'Thermistor 0', 'Thermistor 1', 'Thermistor 2', 'Thermistor 3', 'Thermistor 4']
    length2 = length
    f = open(file_name, 'w', encoding='UTF8', newline='\n')
    if data[0][:1] != '0':
        data.pop(0)
        length2 = length2 - 1
    for j in range(len(col_name)):
        f.write(col_name[j])
        f.write(',')
    f.write('\n')
    for i in range(length2):
        #print(data[i])
        f.write(data[i])
        f.write('\n')
    f.close()
    print("Data saved!")


def init_serial_port(port, baudrate):
    serial_instance = serial.Serial()
    serial_instance.baudrate = baudrate
    serial_instance.port = port
    serial_instance.timeout = 1
    serial_instance.open()
    return serial_instance


def calculate_time(temps):
    return time.time() - temps


# code starts here!!! :)


ports = serial.tools.list_ports.comports()
temps_passer = 0

for COM_port in ports:
    print(str(COM_port))


nom_port = input("Choisie le port que tu veux")
baudrate = input("Choisie le baudrate (recommender 115200)")
acquisition_time = input("Combient de temps l'acquisition (secondes)")

temps_ini = time.time()
n = 0
data = []

instance = init_serial_port(nom_port, baudrate)
instance.flushInput()
instance.flushOutput()
while temps_passer <= int(acquisition_time):

    if instance.in_waiting:
        line = instance.read_until()
        data.append((line.decode('utf').strip('\n')))
        instance.flushInput()
        instance.flushOutput()
        n = n+1
        print(line.decode('utf').strip('\n'))
        temps_passer = calculate_time(temps_ini)
        instance.flushInput()
        instance.flushOutput()
instance.close()
save_data(data, "test_frigo.csv", n)

print("done :) !")
