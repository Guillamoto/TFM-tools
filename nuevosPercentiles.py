import numpy as np
import matplotlib.pyplot as plt
from DRG import *

with open("ProporcionesFinales.txt","r") as fichero:
    listaFichero = fichero.readlines()
    lineas = []
    for ind, text in enumerate(listaFichero):
        lineas.append(listaFichero[ind].split())

    percentil4555 = []
    percentil80 = []

    for i in lineas:
        if float(i[6]) >= 45 and float(i[6]) <= 55:
            percentil4555.append(i[0])
        elif float(i[6]) >= 80 and float(i[6]) <= 90:
            percentil80.append(i[0])



with open("PercentilesReacciones2.txt","w") as escritura:
    escritura.write("Reacciones activas entre el 45 y 55%:\n")
    for i in percentil4555:
        escritura.write(f"{lineas[int(i)][2]}\n")
    
    escritura.write("\nReacciones activas entre el 80 - 90%: \n")
    for i in percentil80:
        escritura.write(f"{lineas[int(i)][2]}\n")

listaReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")

matrizReacciones4555 = EFMsReaccion(percentil4555,listaEFMs)
matrizNoReacciones4555 = EFMsNoReaccion(percentil4555,listaEFMs)

matrizReacciones80 = EFMsReaccion(percentil80,listaEFMs)
matrizNoReacciones80 = EFMsNoReaccion(percentil80,listaEFMs)

for i, v in enumerate(percentil4555):
    print(f"Número de EFMs para la reacción {v}: {len(matrizReacciones4555[i])}")



for i, v in enumerate(percentil80):
    print(f"Número de EFMs para la reacción {v}: {len(matrizReacciones80[i])}")