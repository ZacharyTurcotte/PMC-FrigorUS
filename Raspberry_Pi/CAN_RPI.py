import os
import can
import time
import numpy as np


class CAN_driver:
	
#public
	def __init__(self,canX,bitrate):

		if int(bitrate) != 125000 and int(bitrate) != 250000 and int(bitrate) != 500000 and int(bitrate) != 1000000: 
			raise ValueError("Bitrate invalide")
		
		self.bitrate = str(bitrate)
		self.CAN_channel = str(canX)
		
		#os.system('sudo ip link set ' + str(canX) + ' type can bitrate ' +str(bitrate))
		#os.system('sudo ifconfig '+ str(canX) + ' up')
		self.can0 = can.interface.Bus(channel = self.CAN_channel ,bustype='socketcan')

		
	def send_can_data_frame(self,id,data):
		msg1 = can.Message(arbitration_id=id, data=data,is_extended_id=False)	
		self.can0.send(msg1)
		time.sleep(0.01) #pour laisser le temps d'envoyer le frame


	def send_remote_frame(self,id):
		msg1 = can.Message(arbitration_id=id,is_extended_id=False,is_remote_frame=True)	
		self.can0.send(msg1)
		msg = self.__read_can_bus(1.0) #timeout après 1 seconde
		if msg is None:
			print("timeout, aucun message recu")
			return None
		
		msg = self.__decode_can_msg(msg)
		return msg
 
 # private
	def __decode_can_msg(self,msg):
		out = np.zeros(msg.dlc)
		for i in range(msg.dlc):
			out[i] =  msg.data[i]
		return out


	def  __read_can_bus(self,timeout):
		msg = self.can0.recv(timeout)
		return msg
