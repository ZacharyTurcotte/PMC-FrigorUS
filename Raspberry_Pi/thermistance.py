import MCP3008_IP
import numpy as np


class thermistance_NTC:

#public

	def __init__(self,ADC_Vref,ADC_CS,spi):
		self.coefA = 1.131e-3 # mettre les vrai coeff avec toutes les decs
		self.coefB = 2.3381e-4
		self.coefC = 0.89038e-7
		self.Vref = ADC_Vref
		self.CS = ADC_CS
		self.spi = spi
		self.Rref = 10e3
		self.ADC = MCP3008_IP.MCP3008_IP(ADC_Vref,ADC_CS) 
				
	def get_temperature(self,channel):
		Vout = self.ADC.read_adc_SE(channel,self.spi)
		Rth = self.Rref*(self.Vref/(Vout+1e-6)-1) # a vérifer j'ai fait tres vite
		return self.__calculte_temp(Rth)


#private	

	def __calculte_temp(self,Rth):
		T = 1/(self.coefA + self.coefB*np.log(Rth) + self.coefC*np.power(np.log(Rth),3))
		return T-273.15
