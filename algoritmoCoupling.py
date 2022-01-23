
from DRG_module import *

# EL OBJETIVO AHORA ES CALCULAR LAS REACCIONES REVERSIBLES, Y CALCULAR EFMs en los que tienen flujos en una dirección u en otra. ¿Estudio de acoplamiento de flujos?


listaReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")

# Doble listado con mismo orden: número y nombre de cada reacción de interés. Una alternativa sería un diccionario.
listaReversibles = [11, 13, 22, 28, 35, 40, 45, 50, 55, 65, 76, 82, 84, 85, 86]
listaReversiblesNombres = ["ATPS4r", "CO2t", "EX_co2_e", "EX_h2o_e", "FBA", "FUM", "GLUDy", "H2Ot", "MDH", "PGI", "RPE", "TALA", "TKT1", "TKT2", "TPI"]
## Son las siguientes reacciones, en ese orden:
# ATPS4r
# CO2t
# EX_co2_e
# EX_h2o_e
# FBA
# FUM
# GLUDy
# H2Ot
# MDH
# PGI
# RPE
# TALA
# TKT1
# TKT2
# TPI

#### ALGORITMO: ANÓTAME EN CUÁNTOS EFMs ES EL FLUJO POSITIVO, Y EN CUÁNTOS NEGATIVO.

conteoFlujos = []
EFMsPositivos = []
EFMsNegativos = []

for ind, v in enumerate(listaReversibles):
    positivo = 0
    negativo = 0
    EFMplus = []
    EFMminus = []
    for j in listaEFMs:
        if float(j[v]) > 0:
            positivo += 1
            EFMplus.append(j)
        elif float(j[v]) < 0:
            negativo += 1
            EFMminus.append(j)
    conteoFlujos.append([listaReversiblesNombres[ind],positivo,negativo])
    EFMsPositivos.append(EFMplus)
    EFMsNegativos.append(EFMminus)

print(conteoFlujos)

proporcionesPositivas = []
proporcionesNegativas = []

for i in EFMsPositivos:
    proporcionesPositivas.append(CalculoProporciones(listaReacciones, i))

for i in EFMsNegativos:
    proporcionesNegativas.append(CalculoProporciones(listaReacciones, i))

for i in range(len(listaReversibles)):
    porcentajePlus = {key:(round((value/conteoFlujos[i][1]*100),4)) for key, value in proporcionesPositivas[i].items()}
    porcentajeMinus = {key:(round((value/conteoFlujos[i][2]*100),4)) for key, value in proporcionesNegativas[i].items()}

    dfp = dfProporciones(listaReacciones, proporcionesPositivas[i], proporcionesNegativas[i], porcentajePlus, porcentajeMinus)
    dfp.to_csv(f"Proporciones{listaReversiblesNombres[i]}.csv")






