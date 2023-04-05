import smbus
import time
# not use anymore, only to test and understand how I2C works on the Pi

class DS3231:
    def __init__(self, bus_num, dev_addr=0x68):

        self.bus = smbus.SMBus(bus_num)
        self.dev_addr = dev_addr
    

    def bcd_to_decimal(self, bcd):

        return (bcd & 0x0F) + ((bcd >> 4) * 10)
    

    def decimal_to_bcd(self, decimal):

        return ((decimal // 10) << 4) | (decimal % 10)
    

    def get_time(self):

        time_bytes = self.bus.read_i2c_block_data(self.dev_addr, 0x00, 7)

        seconds = self.bcd_to_decimal(time_bytes[0] & 0x7F)
        minutes = self.bcd_to_decimal(time_bytes[1])
        hours = self.bcd_to_decimal(time_bytes[2] & 0x3F)
        day = self.bcd_to_decimal(time_bytes[3])
        date = self.bcd_to_decimal(time_bytes[4])
        month = self.bcd_to_decimal(time_bytes[5] & 0x1F)
        year = self.bcd_to_decimal(time_bytes[6])
        

        return {'secondes': seconds, 'minutes': minutes, 'heures': hours, 'jour': day, 'date': date, 'mois': month, 'annee': year}
    

    def set_time(self, seconds, minutes, hours, day, date, month, year):
        
        seconds = self.decimal_to_bcd(seconds)
        minutes = self.decimal_to_bcd(minutes)
        hours = self.decimal_to_bcd(hours)
        day = self.decimal_to_bcd(day)
        date = self.decimal_to_bcd(date)
        month = self.decimal_to_bcd(month)
        year = self.decimal_to_bcd(year)
        

        self.bus.write_i2c_block_data(self.dev_addr, 0x00, [seconds, minutes, hours, day, date, month, year])
    

    def get_min(self):
            return self.bus.read_byte_data(self.dev_addr,0x00)
    

    def enable_sqw(self, freq):

        if freq == 1:
            self.bus.write_byte_data(self.dev_addr, 0x0E, 0x10)
        elif freq == 1024:
            self.bus.write_byte_data(self.dev_addr, 0x0E, 0x14)
        elif freq == 4096:
            self.bus.write_byte_data(self.dev_addr, 0x0E, 0x18)
        elif freq == 8192:
            self.bus.write_byte_data(self.dev_addr, 0x0E, 0x1C)
        else:
            raise ValueError("Invalid frequency value. Valid values are 1, 1024, 4096, or 8192.")
    

    def disable_sqw(self):

        self.bus.write_byte_data(self.dev_addr, 0x0E, 0x00)

rtc = DS3231(bus_num=1, dev_addr=0x68)
# test pour le RTC
rtc.set_time(1,1,14,1,1,1,2020)
while(True):
	time.sleep(1)
	print(rtc.get_min())
	
