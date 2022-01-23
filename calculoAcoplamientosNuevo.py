from DRG import *
from itertools import combinations
import numpy as np
import pandas as pd
import time

tiempo0 = time.process_time()

# Con un fichero con la matriz de reacciones, extraer la lista de reacciones y la lista de EFMs por separado.
nombresReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")
# Cálculo de todas las posibles combinaciones de implicaciones (a pares). El propio comando filtra las repeticiones en otro orden.
combinaciones= set(i for i in combinations(nombresReacciones,2))

tiempo1 = time.process_time()
print("t1:", tiempo1-tiempo0)

# PRIMER RECORRIDO: IMPLICACIONES CLARAS EN PROPORCIONES TOTALES
# Set para guardar las implicaciones
implicacionesPerfectas = set()

# Calculamos con proporciones: si la proporción es idéntica con todos los decimales, se entiende que podría darse una implicación idéntica. Calculamos la longitud media y desviación de sus EFMs para confirmar.

# SE CALCULA LA PROPORCIÓN EN LA QUE APARECE CADA REACCIÓN
proporcionesTotal = CalculoProporciones(nombresReacciones, listaEFMs)

tiempo2 = time.process_time()
print("t2:",tiempo2-tiempo1)

# Recorremos cada tupla de combinaciones posibles.
for i in combinaciones:
    # Barrido con las reacciones para asignar su índice en la lista de reacciones para usarlo en "CalcularLongitud"
    for ind, j in enumerate(nombresReacciones):
        if j == i[0]:
            i1 = ind
        if j == i[1]:
            i2 = ind

    # UNA VEZ ESTABLECEMOS EL PAR, SI COINCIDE EL % DE APARICIÓN DE AMBAS REACCIONES...
    if proporcionesTotal[i[0]] == proporcionesTotal[i[1]]:
        # Calculamos la longitud media y desviación típica para el listado de EFMs que SIEMPRE contienen la reacción concreta.
        l1 = CalcularLongitud(EFMsReaccion([i1],listaEFMs)[0])
        l2 = CalcularLongitud(EFMsReaccion([i2],listaEFMs)[0])

        # Si coinciden, guardamos la implicación como una perfecta. 
        if np.mean(l1) == np.mean(l2) and np.std(l1) == np.std(l2):
            implicacionesPerfectas.add(i)

tiempo3 = time.process_time()
print("t3:",tiempo3-tiempo2)

# Ahora, combinamos con una función recursiva de modo que todas las implicaciones perfectas se guarden como bloques, en vez de como pares.
bloquesImplicacionesPerfectas = CombinarAcoplamiento(BarridoAcoplamientos(implicacionesPerfectas))



# Escritura de estos resultados en el fichero.
with open("ImplicacionesAcoplamientosNuevo.txt","w") as fichero:
    fichero.write("Estos son todos los bloques de implicaciones perfectas encontrados.")
    fichero.write(str(bloquesImplicacionesPerfectas))

tiempo4 = time.process_time()
print("t4:",tiempo4-tiempo3)

# SEGUNDA PARTE: IMPLICACIONES PARCIALES Y NEGATIVAS

# Primero separamos los pares ya resueltos del resto para ahorrar recursos computacionales en posteriores procedimientos.
combinaciones2 = []
for i in combinaciones:
    if i not in implicacionesPerfectas:
        combinaciones2.append(i)

tiempo5 = time.process_time()
print("t5:",tiempo5-tiempo4)

# Ahora, comenzamos calculando las implicaciones negativas, al ser más fáciles.
# Para cada reacción, calculamos la lista de EFMs que la contienen SIEMPRE, y entonces, la proporción en la que aparecen el resto de reacciones. 
# Si la proporción es 0, se trata de una implicación negativa (nunca aparecen juntas) y forman parte de su propia lista.

paresNegativas = []
paresParciales = []

# Recorriendo el listado de combinaciones...
for i in combinaciones2:
    # Barrido para establecer los índices respectivos en la lista de reacciones y así funcionar con los EFMs.
    for ind, j in enumerate(nombresReacciones):
        if j == i[0]:
            i1 = ind
        if j == i[1]:
            i2 = ind

    # Calculamos los EFMs en los que aparece la reacción en la posición 1
    EFMs1 = EFMsReaccion([i1], listaEFMs)[0]
    # La proporción (nº EFMs en los que aparece R2)
    # Si la proporción es 0, es un par de implicación negativa.
    if ProporcionesDiana(i2, EFMs1) == 0:
        paresNegativas.append(i)
    # Si el nº de EFMs es total (100%), como la lista excluye acoplamientos perfectos, es un par parcial.
    elif ProporcionesDiana(i2, EFMs1) == len(EFMs1):
        paresParciales.append(i)
    else:
        # Si no casa de ninguna otra, manejamos la inversa: calculamos los EFMs en los que aparece R1 frente al listado de EFMs que siempre incluyen R2, para ver si hay un par parcial.

        EFMs2 = EFMsReaccion([i2], listaEFMs)[0]
        if ProporcionesDiana(i1, EFMs2) == len(EFMs2):
            paresParciales.append(i)

with open("ImplicacionesAcoplamientosNuevo.txt","a") as fichero:
    fichero.write("\nEstos son todos los pares de implicaciones negativas encontrados.\n")
    fichero.write(str(paresNegativas))
    fichero.write("\n\n")
    fichero.write("\nEstos son todos los pares de implicaciones parciales encontrados.\n")
    fichero.write(str(paresParciales))

tiempo6 = time.process_time()
print("t6:",tiempo6-tiempo5)