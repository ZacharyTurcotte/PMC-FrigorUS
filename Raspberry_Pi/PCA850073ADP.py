import smbus
import numpy as np

#ressource : https://www.nxp.com/products/peripherals-and-logic/signal-chain/real-time-clocks/automotive-rtcs/automotive-tiny-real-time-clock-calendar-with-alarm-function-and-ic-bus:PCA85073A
#datasheet : https://www.nxp.com/docs/en/data-sheet/PCA85073A.pdf


class PCA85073ADP:
        def __init__(self, bus_num=1): 

                self.rtc_address = 0xA2
                self.rtc_timer_register = 0x10
                self.bus = smbus.SMBus(bus_num)
                control_1 = 0b00000000 #default
                control_2 = 0b00001000 #bit 3e bit a 1 pour int de timer pas d'alerme
                timer_mode = 0b00011110 # seter le registre de timer 
                self.bus.write_byte_data(self.rtc_address,0x00,control_1)
                time.sleep(1/1000)
                self.bus.write_byte_data(self.rtc_address,0x00,control_2)
                time.sleep(1/1000)
                self.bus.write_byte_data(self.rtc_address,0x00,timer_mode)
                time.sleep(1/1000)
    
        def read_datetime(self): # version simple qui devrais marcher mais on sais jamais car datasheet sus
                
                rtc_data = [0] * 7
                rtc_data = self.bus.read_i2c_block_data(self.rtc_address,0x04,7)
        
                seconds = (rtc_data[0] & 0x0F) + ((rtc_data[0] >> 4) * 10)
                minutes = (rtc_data[1] & 0x0F) + ((rtc_data[0] >> 4) * 10)
                hours = (rtc_data[2] & 0x0F) + ((rtc_data[0] >> 4) * 10)
                date = (rtc_data[3] & 0x0F) + ((rtc_data[0] >> 4) * 10)
                day = (rtc_data[4])
                month = (rtc_data[5] & 0x0F) + ((rtc_data[0] >> 4) * 10)
                year = (rtc_data[6] & 0x0F) + ((rtc_data[0] >> 4) * 10)

                return (year, month, date, day, hours, minutes, seconds)
        

        def write_datetime(self, year, month, date, day, hours, minutes, seconds):
                rtc_data = np.zeros(7)
                
                rtc_data[0] = ((int(seconds/10)<<4)|seconds%10)
                rtc_data[1] = ((int(minutes/10)<<4)|minutes%10)
                rtc_data[2] = ((int(hours/10)<<4)|hours%10)
                rtc_data[3] = ((int(date/10)<<4)|date%10)
                rtc_data[4] = day #0 est dimanche et 6 est samedi
                rtc_data[5] = ((int(month/10)<<4)|month%10)
                rtc_data[6] = ((int(year/10)<<4)|year%10)

                self.bus.write_i2c_block_data(self.rtc_address, 0x02, rtc_data)
        
        def set_timer(self,count_down):
                
                if count_down*60 > 255:
                        raise ValueError("Countn down invalide")
                
                self.bus.write_byte_data(self.rtc_address, self.rtc_timer_register, count_down)
                
        def __bcd_to_decimal(self, bcd):
                return (bcd & 0x0F) + ((bcd >> 4) * 10)
    
        def __decimal_to_bcd(self, decimal):
                return ((int(decimal/10)<<4)|decimal%10)
