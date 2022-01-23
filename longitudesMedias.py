from DRG_module import FicheroMatriz, EFMsReaccion, CalcularLongitud
import numpy as np
import pandas as pd


#### OBJETIVO: CALCULAR LA LONGITUD MEDIA DE LOS EFMS DE TODAS LAS REACCIONES ####

listaReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")

### DATOS TOTALES

longitudes = CalcularLongitud(listaEFMs)
print(f"La media total es {np.mean(longitudes)}")
print(f"La desviación estándar total es {np.std(longitudes)}")


## DATOS DE CADA REACCIÓN

arrayLongitudes = []
for i in range(len(listaReacciones)):
    EFMs = EFMsReaccion([i],listaEFMs)
    longitudes = CalcularLongitud(EFMs[0])
    arrayLongitudes.append(longitudes)

listaMedias = []
listaDesviaciones = []
for i in arrayLongitudes:
    listaMedias.append(np.mean(i))
    listaDesviaciones.append(np.std(i))

### ARRAY PARA PASAR A DATAFRAME

matriz = [listaReacciones,listaMedias,listaDesviaciones]

df = pd.DataFrame(matriz).T

df = df.rename(columns={0: "REACCION", 1: "MEDIA", 2: "STD"})

df.to_csv("DataFrameLongitudes.csv")