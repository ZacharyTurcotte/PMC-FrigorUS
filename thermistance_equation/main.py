import numpy as np
import matplotlib.pyplot as plt


temp = np.array([-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
res = np.array([333.56, 241.072, 176.082, 129.925, 96.807, 72.809, 55.253, 42.292, 32.64, 25.391, 19.902, 15.713, 12.493, 10, 8.056, 6.53, 5.325, 4.367])*1000
Rref = 10000
A = 1.131024546/1000
B = 2.338051738/10000
C = 0
D = 0.8903773352/10000000

temp_cal = 1/(A +(B*np.log(res))+(D*np.log(res)**3))-273.15
plt.show()
plt.plot(res, temp, label="température datasheet")
plt.plot(res, temp_cal, label="temp cal")
plt.legend()
plt.title("Comparaison entre la courbe de la datasheet et la courbe estimée")
plt.xlabel("Résistance de $R_th (\Omega)$")
plt.ylabel("Température (°C)")
plt.grid()
plt.show()