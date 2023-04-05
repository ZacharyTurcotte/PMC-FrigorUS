from MAX11625EEG import MAX11625EEG
import numpy as np


class thermistance_NTC:

#public

	def __init__(self,ADC_Vref,ADC_CS,spi):
		
		self.coefA = 1.131e-3 # mettre les vrai coeff avec toutes les decs
		self.coefB = 2.3381e-4
		self.coefC = 0.89038e-7
		self.Vref = ADC_Vref
		self.CS = ADC_CS
		self.Rref = 10e3
		self.ADC = MAX11625EEG(self.Vref,self.CS,spi)
				
	def get_single_temperature(self,channel):
		
		Vout = self.ADC.read_adc_SE(channel)
		Rth = self.Rref*(self.Vref/(Vout+1e-6)-1) # a vérifer j'ai fait tres vite
		return self.__calculte_temp(Rth)


	def get_all_temperature(self):
		
		Vout = self.ADC.read_all_channel()
		out = [0] * len(Vout)
		
		for i in range(len(Vout)):
			Rth = Rth = self.Rref*(self.Vref/(Vout[i]+1e-6)-1)
			out[i] = self.__calculte_temp(Rth)

		return out

	def get_average_temp(self):
		
		Temp = self.get_all_temperature()
		mean = sum(Temp)/len(Temp)
		return mean
	

#private	

	def __calculte_temp(self,Rth):
		T = 1/(self.coefA + self.coefB*np.log(Rth) + self.coefC*np.power(np.log(Rth),3))
		return T-273.15
