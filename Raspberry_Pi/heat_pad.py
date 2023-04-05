from MAX11625EEG import MAX11625EEG
from MCP23017 import MCP23017
from thermistance import thermistance_NTC


class heat_pad:


    def __init__(self,temp_min, temp_max,spi,nb_thermistance):
        
        self.IO_Exp = MCP23017()
        self.Thermistance = thermistance_NTC(3.3,2,spi)
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.default_config_bank_a = 0b00000000
        self.default_config_bank_b = 0b00000000
        self.state_wait = 0
        self.bank = [0] * 2
        self.all_temp = [0] * nb_thermistance
        self.reach_max_temp = 0
   
    def update_heat_pad_state(self,bank):

        self.IO_Exp.write_all_pin(bank[0],bank[1])
    
    def check_temp(self):
        
        self.__get_all_temperature()

        if min(self.all_temp) <= self.temp_min | self.reach_max_temp == 0:
            
            self.reach_max_temp = 0            
            
            if min(self.all_temp) >= self.temp_max:
                self.reach_max_temp = 1
                self.bank = 0
                self.deactivate_heat_pad()

                return self.bank
                        
            out = 0b0000000000000000 # 16 bits

            for i in range(len(self.all_temp)):
                if self.all_temp[i] <= self.temp_min:
                    out = out | 1<<i 

            self.bank[0] = out & 0xff
            self.bank[1] = (out>>8) & 0xff
            
            self.update_heat_pad_state(self.bank)
        
        return self.bank

    def deactivate_heat_pad(self):

        self.IO_Exp.write_all_pin(self.default_config_bank_a,self.default_config_bank_b)

# private

    def __get_all_temperature(self):
        self.all_temp = self.Thermistance.get_all_temperature()

    def __get_heat_pad_state(self):
        return self.IO_Exp.read_all_pin()