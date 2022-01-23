import numpy as np
import matplotlib.pyplot as plt
from DRG import FicheroMatriz, CalcularLongitud
from random import randrange

listaReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")

proporcionesTotales = {}
for i in listaReacciones:
    proporcionesTotales[i] = 0
for i in EFMsEColi:
    for ind, j in enumerate(i):
        if j != '0':
            proporciones[listaReacciones[ind]] += 1 
print(len(listaEFMs))

i = len(listaEFMs)
recorridoEFMs = []
listaLongitudes = []
mediaAcumulada = []
listaProporciones = []

while i > 0:
    EFM = listaEFMs.pop(randrange(0, i-1))
    recorridoEFMs.append(EFM)

    longitud = CalcularLongitud(EFM)
    listaLongitudes.append(longitud)
    mediaAcumulada.append(np.mean(listaLongitudes))

    

    i = len(listaEFMs)
    print(i)

plt.plot(mediaAcumulada)
plt.savefig("mediaAcumuladaEstadistico")

