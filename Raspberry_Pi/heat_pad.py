from MAX11625EEG import MAX11625EEG
from MCP23017 import MCP23017
from thermistance import thermistance_NTC


class heat_pad:


    def __init__(self,temp_min, temp_max,spi):
        
        self.IO_Exp = MCP23017()
        self.Thermistance = thermistance_NTC(3.3,2,spi)
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.config_bank_a = 0b00000000
        self.config_bank_b = 0b00000000

    def get_heat_pad_state(self):

        return self.IO_Exp.read_all_pin()

    
    def update_heat_pad_state(self,bank):

        self.IO_Exp.write_all_pin(bank[0],bank[1])

    
    def check_temp(self):

        bank = [0] * 2
        Temperature = self.Thermistance.get_all_temperature()
        out = 0b0000000000000000 # 16 bits

        for i in range(len(Temperature)):
            if Temperature[i] <= self.temp_min:
                out = out | 1<<i 

        bank[0] = out & 0xff
        bank[1] = (out>>8) & 0xff

        return bank

        