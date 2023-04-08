import serial

class uart_com:
    
    def __init__(self, COM_port):
        self.start_flag = 0xA5
        self.master_address = 0x80 # pas clair
        self.module_address = 0x01
        self.SoC_Vtot = 0x90 # ID du SoC et Voltage total
        self.Vmin = 0x91
        self.Temp_min = 0x92
        self.Mos_status = 0x93
        self.status_info = 0x94
        self.Cell_voltage = 0x95
        self.check_faillure = 0x98

        self.port = serial.Serial(COM_port, 9600, timeout=3,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)

    #def get_data(self):

        