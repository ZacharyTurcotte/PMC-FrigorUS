import smbus
import numpy as np
import time
#ressource : https://www.nxp.com/products/peripherals-and-logic/signal-chain/real-time-clocks/automotive-rtcs/automotive-tiny-real-time-clock-calendar-with-alarm-function-and-ic-bus:PCA85073A
#datasheet : https://www.nxp.com/docs/en/data-sheet/PCA85073A.pdf


class PCA850073ADP:
        def __init__(self, bus_num=1): 

                self.rtc_address = 0x51
                self.rtc_timer_register = 0x10
                self.bus = smbus.SMBus(bus_num)
                control_1 = 0x00 #default
                control_2 = 0b00001000 #bit 3e bit a 1 pour int de timer pas d'alerme
                timer_mode = 0b00011110 # seter le registre de timer 
                self.bus.write_byte_data(self.rtc_address,0x00,control_1)
                time.sleep(1/1000)
                self.bus.write_byte_data(self.rtc_address,0x01,control_2)
                time.sleep(1/1000)
                self.bus.write_byte_data(self.rtc_address,0x10,timer_mode)
                time.sleep(1/1000)
        def read_date(self):
                
                print(self.bus.read_byte_data(self.rtc_address,0x07))
                
                
        def read_datetime(self): # version simple qui devrais marcher mais on sais jamais car datasheet sus
                
                rtc_data = [0] * 7
                rtc_data = self.bus.read_i2c_block_data(self.rtc_address,0x04,7)
        
                seconds = self.__bcd_to_decimal(rtc_data[0])
                minutes = self.__bcd_to_decimal(rtc_data[1])
                hours = self.__bcd_to_decimal(rtc_data[2])
                date = self.__bcd_to_decimal(rtc_data[3])
                day = self.__bcd_to_decimal(rtc_data[4])
                month = self.__bcd_to_decimal(rtc_data[5])
                year = self.__bcd_to_decimal(rtc_data[6])


                return (year, month, date, day, hours, minutes, seconds)
        

        def write_datetime(self, year, month, day, date, hours, minutes, seconds):
                
                if day > 7:
                        raise ValueError("day no good")
                        
                if date > 32:
                        raise ValueError("date no good")
                
                if month > 13:
                        raise ValueError("Month no good")
                
                if hours > 60:
                        raise ValueError("hours no good")
                
                if seconds > 60:
                        raise ValueError("Seconds no good")
                
                if minutes > 61:
                        raise ValueError("Minutes no good")
                
                
                rtc_data = [0] * 7
                              
                rtc_data[0] = self.__decimal_to_bcd(seconds)
                rtc_data[1] = self.__decimal_to_bcd(minutes)
                rtc_data[2] = self.__decimal_to_bcd(hours)
                rtc_data[3] = self.__decimal_to_bcd(date)
                rtc_data[4] = self.__decimal_to_bcd(day) #0 est dimanche et 6 est samedi
                rtc_data[5] = self.__decimal_to_bcd(month)
                rtc_data[6] = self.__decimal_to_bcd(year)

                self.bus.write_i2c_block_data(self.rtc_address, 0x04, rtc_data)
        
        def set_timer(self,count_down):
                
                if count_down*60 > 255:
                        raise ValueError("Countn down invalide")
                
                self.bus.write_byte_data(self.rtc_address, self.rtc_timer_register, count_down)
                
        def __bcd_to_decimal(self, bcd):
                return (bcd & 0x0F) + ((bcd >> 4) * 10)
    
        def __decimal_to_bcd(self, decimal):
                return ((int(decimal/10)<<4)|decimal%10)
