from DRG import *
import numpy as np
import pandas as pd

# OBJETIVO DE ESTE SCRIPT: CALCULAR TODAS LAS ESTAS NEGATIVAS Y TODAS LAS ÉSTAS PARCIALES. LO HAGO DESDE AQUÍ PARA AHORRAR EN RESUMEN.

listaReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")

candidatosParcial = []
candidatosNo = []

listaProporciones = []

for ind, r in enumerate(listaReacciones):

    # Cálculo de los EFMs a los que pertenece una reacción específica.
    EFMs = EFMsReaccion([ind],listaEFMs)[0]
    # Calculo de proporciones en esos EFMs
    proporcionesReaccion = CalculoProporciones(listaReacciones, EFMs)
    # Guardamos las proporciones en un array.
    listaProporciones.append(proporcionesReaccion)

    for i in proporcionesReaccion:
        if proporcionesReaccion[i] == 0:
            candidatosNo.append((r,i))
        elif proporcionesReaccion[i] == len(EFMs):
            if r != i:
                candidatosParcial.append((r,i))

bloqueosClaros = []
identicas = []

for i in candidatosParcial:
    for j in candidatosParcial:
        if i[0] == j[1] and i[1] == j[0]:
            identicas.append(i)
            identicas.append(j)

reaccionesParciales = [i for i in candidatosParcial if i not in identicas]

for i in candidatosNo:
    for j in candidatosNo:
        if i[0] == j[1] and i[1] == j[0]:
            bloqueosClaros.append([i[0],i[1]])

remove = []
for i in reaccionesParciales:
    if i[1] == 'R_EX_glc__D_e' or i[1] == 'R_GLCpts':
        remove.append(i)

parciales2 = [i for i in reaccionesParciales if i not in remove]


########################################################################################################

# TENIENDO LOS RESULTADOS, VAMOS A TRANSFORMARLOS DECENTEMENTE LEÑE

acoplamientosTotales = [{'R_ACALDt', 'R_EX_acald_e'}, {'R_ACKr', 'R_PTAr', 'R_ACt2r', 'R_EX_ac_e'}, {'R_CS', 'R_ACONTb', 'R_ACONTa'}, {'R_PPS', 'R_ADK1'}, {'R_SUCOAS', 'R_AKGDH'}, {'R_AKGt2r', 'R_EX_akg_e'}, {'R_EX_etoh_e', 'R_ALCD2x', 'R_ETOHt2r'}, {'R_EX_pi_e', 'R_Biomass_Ecoli_core', 'R_PIt2r'}, {'R_EX_co2_e', 'R_CO2t'}, {'R_O2t', 'R_CYTBD', 'R_EX_o2_e'}, {'R_D_LACt2', 'R_EX_lac__D_e', 'R_LDH_D'}, {'R_PGM', 'R_ENO', 'R_GAPD', 'R_PGK'}, {'R_PFL', 'R_EX_for_e'}, {'R_EX_glc__D_e', 'R_GLCpts'}, {'R_GLUt2r', 'R_EX_glu__L_e'}, {'R_EX_h2o_e', 'R_H2Ot'}, {'R_NH4t', 'R_EX_nh4_e'}, {'R_PYRt2', 'R_EX_pyr_e'}, {'R_FBA', 'R_TPI'}, {'R_G6PDH2r', 'R_GND', 'R_PGL'}, {'R_MALS', 'R_ICL'}, {'R_TALA', 'R_TKT1'}]

reordenamientoParciales = []

for i in acoplamientosTotales:
    lista = []
    for j in parciales2:
        if j[1] in i:
            lista.append(j)
    reordenamientoParciales.append(lista)

# CAMBIAR ACOPLAMIENTOS A ELEMENTO - BLOQUE COMÚN.

acoplamientosParcialesFinales = []

for i in reordenamientoParciales:
    if len(i) > 0:
        ref = set(i[0])
        for j in i:
            ref = ref.union(set(j))
        acoplamientosParcialesFinales.append(ref)
    elif len(i) == 0:
        acoplamientosParcialesFinales.append({'Ninguno'})

for i, v in enumerate(acoplamientosTotales):
    for j in v:
        acoplamientosParcialesFinales[i].discard(j)

print(acoplamientosParcialesFinales)

with open("Acoplamientos2.txt","w") as fichero:
    fichero.write("Se han observado las siguientes implicaciones negativas:\n")
    fichero.write(str(bloqueosClaros))
    fichero.write("\n\n-----------------------------------\n")
    fichero.write("Se han observado las siguientes implicaciones parciales:\n")
    for i in range(len(acoplamientosTotales)):
        fichero.write(f"\nPara el bloque {str(acoplamientosTotales[i])} se ha observado que existen dependencias de:\n")
        fichero.write(str(acoplamientosParcialesFinales[i]))
