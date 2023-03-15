import smbus
import time

#Addresses
#Control_1 00h
#Control_2 01h
#Offset 02h
#RAM_byte 03h
#Seconds 04h
#Minutes 05h
#Hours 06h
#Days 07h
#Weekdays 08h
#Months 09h
#Years 0Ah

#ressource https://www.nxp.com/products/peripherals-and-logic/signal-chain/real-time-clocks/automotive-rtcs/automotive-tiny-real-time-clock-calendar-with-alarm-function-and-ic-bus:PCA85073A



class PCA85073ADP:
    def __init__(self, bus_num=1, rtc_READ_address=0xA3,rtc_WRITE_address=0xA2): 
        self.rtc_write_address = rtc_WRITE_address
        self.rtc_read_address = rtc_READ_address
        self.bus = smbus.SMBus(bus_num)
        control_1 = 0b10000000 # a changer
        control_2 = 0b00000000 #bit 0 a 0 aucun interupts d'alarme
        self.bus.write_i2c_block_data(self.rtc_address,0x00,control_1)
        self.bus.write_i2c_block_data(self.rtc_address,0x00,control_2)
    
    def read_datetime(self):
        rtc_data = self.bus.write_i2c_block_data(self.rtc_write_address, 0x04)

        seconds = (rtc_data[0] & 0x7f) + (rtc_data[6] & 0x80)
        minutes = rtc_data[1] & 0x7f
        hours = rtc_data[2] & 0x3f
        day = rtc_data[3] & 0x3f
        date = rtc_data[4] & 0x3f
        month = rtc_data[5] & 0x1f
        year = rtc_data[6] & 0x7f

        return (year, month, date, day, hours, minutes, seconds)

    def write_datetime(self, year, month, date, day, hours, minutes, seconds):
        rtc_data = [0] * 7
        rtc_data[0] = (seconds % 60) | 0x80
        rtc_data[1] = minutes % 60
        rtc_data[2] = hours % 24
        rtc_data[3] = day % 8
        rtc_data[4] = date % 32
        rtc_data[5] = month % 13
        rtc_data[6] = year % 100

        self.bus.write_i2c_block_data(self.rtc_address, 0x02, rtc_data)
