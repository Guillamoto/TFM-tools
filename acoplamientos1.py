from DRG_module import *
from itertools import combinations

### EL OBJETIVO DE ESTE SCRIPT ES COMENZAR A CALCULAR ACOPLAMIENTOS.

# PUNTO DE PARTIDA: CÁLCULO DE LAS PROPORCIONES DE TODOS LOS EFMS

listaReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")

proporcionesTotal = CalculoProporciones(listaReacciones, listaEFMs)

### OBTENCIÓN DE TODAS LAS COMBINACIONES DE REACCIONES POSIBLES:
combinaciones = [i for i in combinations(listaReacciones,2)]

# LISTAS A CONSIDERAR
acoplamientoPerfectoTotales = []

# PRIMER RECORRIDO: ACOPLAMIENTOS CLAROS EN PROPORCIONES TOTALES
for i in combinaciones:
    for ind, j in enumerate(listaReacciones):
        if j == i[0]:
            i1 = ind
        if j == i[1]:
            i2 = ind

    if proporcionesTotal[i[0]] == proporcionesTotal[i[1]]:
        l1 = CalcularLongitud(EFMsReaccion([i1],listaEFMs)[0])
        l2 = CalcularLongitud(EFMsReaccion([i2],listaEFMs)[0])

        if np.mean(l1) == np.mean(l2) and np.std(l1) == np.std(l2):
            acoplamientoPerfectoTotales.append(i)

with open("AcoplamientosPares.txt","w") as fichero:
    fichero.write("Estos son todos los pares de acoplamientos encontrados.")
    fichero.write(str(acoplamientoPerfectoTotales))


# otrosEstudios sirve para coger el resto de posibles acoplamientos y darle caña
otrosEstudios = []
for i in combinaciones:
    if i not in acoplamientoPerfectoTotales:
        otrosEstudios.append(i)

setsFinalesTotales = CombinarAcoplamiento(BarridoAcoplamientos(acoplamientoPerfectoTotales))

with open("Acoplamientos.txt","w") as fichero:
    fichero.write("Los acoplamientos que se dan en absolutamente todos los casos son:")
    fichero.write(str(setsFinalesTotales))
    fichero.write("\n\n-----------------------------------\n") # Línea de corte

# AHORA DEBERÍA HACER ESOS MISMOS RECORRIDOS PERO SIN TENER EN CUENTA ESAS REACCIONES.

### VAMOS A MIRAR CUANDO HAY Y CUANDO NO HAY: OXÍGENO (R 31), BIOMASA (R 12), RPI (R 77), CS (R 14), ATP4Sr (R 11).

for r in (31,12,77,14,11):
    # Proporciones donde esa reacción está y donde no está.
    EFMsCon = EFMsReaccion([r],listaEFMs)[0]
    EFMsSin = EFMsNoReaccion([r],listaEFMs)[0]
    proporciones = CalculoProporciones(listaReacciones,EFMsCon)
    proporcionesNo = CalculoProporciones(listaReacciones, EFMsSin)

    # Listas donde almacenar los acoplamientos.
    acoplamientosCon = []
    acoplamientosSin = []

    for c in otrosEstudios:
        for ind, j in enumerate(listaReacciones):
            if j == c[0]:
                i1 = ind
            if j == c[1]:
                i2 = ind


        if proporciones[c[0]] == proporciones[c[1]]:
            l1 = CalcularLongitud(EFMsReaccion([i1],EFMsCon)[0])
            l2 = CalcularLongitud(EFMsReaccion([i2],EFMsCon)[0])

            if np.mean(l1) == np.mean(l2) and np.std(l1) == np.std(l2):
                acoplamientosCon.append(c)

        elif proporcionesNo[c[0]] == proporcionesNo[c[1]]:
            l1 = CalcularLongitud(EFMsReaccion([i1],EFMsSin)[0])
            l2 = CalcularLongitud(EFMsReaccion([i2],EFMsSin)[0])

            if np.mean(l1) == np.mean(l2) and np.std(l1) == np.std(l2):
                acoplamientosSin.append(c)

    acoplamientosConFinal = CombinarAcoplamiento(BarridoAcoplamientos(acoplamientosCon))
    acoplamientosSinFinal = CombinarAcoplamiento(BarridoAcoplamientos(acoplamientosSin))

    with open("Acoplamientos.txt","a") as fichero:
        fichero.write(f"Los acoplamientos que se han observado en los EFMs que contienen la reacción nº {r} son:\n")
        fichero.write(str(acoplamientosConFinal))
        fichero.write(f"\nLos acoplamientos que se han observado en los EFMs que NO contienen la reacción nº {r} son:\n")
        fichero.write(str(acoplamientosSinFinal))   
        fichero.write("\n\n-----------------------------------\n") # Línea de separación  


# HABIENDO HECHO TODO ESTO, AHORA TENGO QUE REPETIRLO PARA BUSCAR LOS ACOPLAMIENTOS INVERSOS (ES DECIR, QUE NUNCA ESTÁN ACOPLADAS ENTRE SÍ) Y LOS PARCIALES.

# PARA BUSCARLOS PODRÍA BUSCAR REACCIÓN A REACCIÓN Y VER A VER QUÉ ME ENCUENTRO, QUIZÁS SERÍA LO MÁS FÁCIL.

    
