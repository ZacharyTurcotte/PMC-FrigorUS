import serial
import time


class uart_com:

    def __init__(self,port):

        self.ser = serial.Serial(
            port=port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.5,
            xonxoff=False,
            writeTimeout=0.5)
        self.soc_voltage_current_com = 0x90
        self.min_voltage_com = 0x91
        self.temperature_com = 0x92
        self.mos_status_com = 0x93
        self.status_info_com = 0x94
        self.cell_voltage_com = 0x95
        self.failure_com = 0x98

    def _calc_crc(self,message_bytes):
        crc = sum(message_bytes) & 0xFF
        return crc

    def _check_crc(self,message_bytes):
        crc = sum(message_bytes[0:12]) & 0xFF
        return crc

    def _format_message(self,command, extra=""):

        message = [0xa5,0x40,command,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        message.append(self._calc_crc(message))
        #message_bytes = bytearray.fromhex(str(message))

        return message

    def _get_data(self,command):

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        message = self._format_message(command)
        print(message)
        self.ser.write(message)
        answer = self.ser.read(13)
        print(answer)
        return answer

    def get_temperature(self):
        temp = self._get_data(self.temperature_com)
        
        if temp[-1] == self._check_crc(temp):
            return temp[4]-40.0 # return la température de la thermistance
        else:
            raise TypeError("Check sum fail Temp")


    def get_SoC_Voltage_Current(self):
        data = self._get_data(self.soc_voltage_current_com)

        if len(data) == 0:
            print("Data vide")
        else:
            voltage = (data[4] << 8 | data[5])/10.0
            current = (data[8] << 8 | data[9] - 30000)/10.0
            soc = (data[10] << 8 | data[11])/10.0

            if data[-1] == self._check_crc(data):
                return [voltage,current,soc]
                print("check sum OK")
            else:
                print("Check sum fail SOC")

    def decode_error(self):
        failure = self._get_data(self.failure_com)
        error = []

        byte0 = bin(failure[0])
        byte1 = bin(failure[1])
        byte2 = bin(failure[2])
        byte3 = bin(failure[3])
        byte4 = bin(failure[4])
        byte5 = bin(failure[5])
        byte6 = bin(failure[6])
        byte7 = bin(failure[7])

        if byte0[2]: error.append("Temp to high 1")
        if byte0[3]: error.append("Temp to high 2")
        if byte0[4]: error.append("Temp to low 1")
        if byte0[5]: error.append("Temp to low 2")
        if byte0[6]: error.append("Temp to high 1")
        if byte0[7]: error.append("Temp to high 2")
        if byte0[8]: error.append("Temp to low 1")
        if byte0[9]: error.append("Temp to low 2")

        if byte1[2]: error.append("Over Current 1")
        if byte1[3]: error.append("Over current 2")
        if byte1[4]: error.append("Over Current 1")
        if byte1[5]: error.append("Over Current 2")
        if byte1[6]: error.append("Soc to high 1")
        if byte1[7]: error.append("Soc to high 2")
        if byte1[8]: error.append("Soc to low 1")
        if byte1[9]: error.append("Soc to low 2")

        if byte2[2]: error.append("cell overvoltage 1")
        if byte2[3]: error.append("cell overvoltage 1")
        if byte2[4]: error.append("cell overvoltage 1")
        if byte2[5]: error.append("cell overvoltage 2")
        if byte2[6]: error.append("Total Overvoltage 1")
        if byte2[7]: error.append("Total Overvoltage 2")
        if byte2[8]: error.append("Total undervoltage 1")
        if byte2[9]: error.append("Total undervoltage 2")

        if byte3[2]: error.append("Cell diff voltage high 1")
        if byte3[3]: error.append("Cell diff voltage high 2")

        if byte4[2]: error.append("cell overvoltage 1")
        if byte4[3]: error.append("cell overvoltage 1")
        if byte4[4]: error.append("cell overvoltage 1")
        if byte4[5]: error.append("cell overvoltage 2")
        if byte4[6]: error.append("Total Overvoltage 1")
        if byte4[7]: error.append("Total Overvoltage 2")
        if byte4[8]: error.append("Total undervoltage 1")
        if byte4[9]: error.append("Total undervoltage 1")

        if byte5[2]: error.append("cell overvoltage 1")
        if byte5[3]: error.append("cell overvoltage 1")
        if byte5[4]: error.append("cell overvoltage 1")
        if byte5[5]: error.append("cell overvoltage 2")
        if byte5[6]: error.append("Total Overvoltage 1")
        if byte5[7]: error.append("Total Overvoltage 2")
        if byte5[8]: error.append("Total undervoltage 1")
        if byte5[9]: error.append("Total undervoltage 1")

        if byte6[2]: error.append("cell overvoltage 1")
        if byte6[3]: error.append("cell overvoltage 1")
        if byte6[4]: error.append("cell overvoltage 1")
        if byte6[5]: error.append("cell overvoltage 2")
        if byte6[6]: error.append("Total Overvoltage 1")
        if byte6[7]: error.append("Total Overvoltage 2")
        if byte6[8]: error.append("Total undervoltage 1")
        if byte6[9]: error.append("Total undervoltage 1")

        if byte7[2]: error.append("cell overvoltage 1")
        if byte7[3]: error.append("cell overvoltage 1")
        if byte7[4]: error.append("cell overvoltage 1")
        if byte7[5]: error.append("cell overvoltage 2")
        if byte7[6]: error.append("Total Overvoltage 1")
        if byte7[7]: error.append("Total Overvoltage 2")
        if byte7[8]: error.append("Total undervoltage 1")
        if byte7[9]: error.append("Total undervoltage 1")


    def get_cell_voltage(self):
        print("Todo XD")
        # on doit read 4 fois

#ser = serial.Serial(port=serial_name,
#                    stopbits=1,
#                   timeout=0)

uart = uart_com("/dev/ttyUSB0")
#uart.get_SoC_Voltage_Current()
while 1:
    time.sleep(1)
    xd = uart.get_SoC_Voltage_Current()
    print(xd)
    print(uart.get_temperature())
