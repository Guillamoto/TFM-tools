from DRG_module import *
import pandas as dp

listaReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")

# Lista de longitudes total
longitudes = CalcularLongitud(listaEFMs)

# Dado que coinciden los índices...

array = [[] for i in range(14)]

# Separación por intervalos de 5 reacciones de longitud. DEBE EXISTIR UN MÉTODO MÁS EFICIENTE: Investigar.
for i,v in enumerate(longitudes):
    if v <= 5:
        array[0].append(listaEFMs[i])
    elif v > 5 and v <= 10:
        array[1].append(listaEFMs[i])
    elif v > 10 and v <= 15:
        array[2].append(listaEFMs[i])        
    elif v > 15 and v <= 20:
        array[3].append(listaEFMs[i])
    elif v > 20 and v <= 25:
        array[4].append(listaEFMs[i])
    elif v > 25 and v <= 30:
        array[5].append(listaEFMs[i])
    elif v > 30 and v <= 35:
        array[6].append(listaEFMs[i])
    elif v > 35 and v <= 40:
        array[7].append(listaEFMs[i])
    elif v > 40 and v <= 45:
        array[8].append(listaEFMs[i])
    elif v > 45 and v <= 50:
        array[9].append(listaEFMs[i])
    elif v > 50 and v <= 55:
        array[10].append(listaEFMs[i])
    elif v > 55 and v <= 60:
        array[11].append(listaEFMs[i])
    elif v > 60 and v <= 65:
        array[12].append(listaEFMs[i])
    elif v > 65 and v <= 70:
        array[13].append(listaEFMs[i])

proporciones = []

for i in range(14):
    proporciones.append(CalculoProporciones(listaReacciones, array[i]).values())

df = dp.DataFrame(data=proporciones, columns = listaReacciones, index = [len(array[i]) for i in range(14)])

print(df)

df.T.to_csv("ProporcionesLongitudes.csv")