
from DRG import *

pares = [('R_ACALDt', 'R_EX_acald_e'), ('R_ACKr', 'R_ACt2r'), ('R_ACKr', 'R_EX_ac_e'), ('R_ACKr', 'R_PTAr'), ('R_ACONTa', 'R_ACONTb'), ('R_ACONTa', 'R_CS'), ('R_ACONTb', 'R_CS'), ('R_ACt2r', 'R_EX_ac_e'), ('R_ACt2r', 'R_PTAr'), ('R_ADK1', 'R_PPS'), ('R_AKGDH', 'R_SUCOAS'), ('R_AKGt2r', 'R_EX_akg_e'), ('R_ALCD2x', 'R_ETOHt2r'), ('R_ALCD2x', 'R_EX_etoh_e'), ('R_ATPM', 'R_GLUN'), ('R_Biomass_Ecoli_core', 'R_EX_pi_e'), ('R_Biomass_Ecoli_core', 'R_PIt2r'), ('R_CO2t', 'R_EX_co2_e'), ('R_CYTBD', 'R_EX_o2_e'), ('R_CYTBD', 'R_O2t'), ('R_D_LACt2', 'R_EX_lac__D_e'), ('R_D_LACt2', 'R_LDH_D'), ('R_ENO', 'R_GAPD'), ('R_ENO', 'R_PGK'), ('R_ENO', 'R_PGM'), ('R_ETOHt2r', 'R_EX_etoh_e'), ('R_EX_ac_e', 'R_PTAr'), ('R_EX_for_e', 'R_PFL'), ('R_EX_glc__D_e', 'R_GLCpts'), ('R_EX_glu__L_e', 'R_GLUt2r'), ('R_EX_h2o_e', 'R_H2Ot'), ('R_EX_lac__D_e', 'R_LDH_D'), ('R_EX_nh4_e', 'R_NH4t'), ('R_EX_o2_e', 'R_O2t'), ('R_EX_pi_e', 'R_PIt2r'), ('R_EX_pyr_e', 'R_PYRt2'), ('R_FBA', 'R_TPI'), ('R_FORt2', 'R_SUCCt2_2'), ('R_G6PDH2r', 'R_GND'), ('R_G6PDH2r', 'R_PGL'), ('R_GAPD', 'R_PGK'), ('R_GAPD', 'R_PGM'), ('R_GND', 'R_PGL'), ('R_ICL', 'R_MALS'), ('R_PGK', 'R_PGM'), ('R_TALA', 'R_TKT1')]

listaReacciones, listaEFMs = FicheroMatriz("EFMsEColi.txt")

listadoAcop = []
flujosGAPDENO = []
for index, i in enumerate(pares):
    acopTotal = 0
    acopParcial = 0
    acopIrr = 0
    acopTotalInv = 0
    for ind, j in enumerate(listaReacciones):
        if i[0] == j:
            indice = ind
        if i[1] == j:
            indice2 = ind
    reaccionesPresentes = EFMsReaccion([indice],listaEFMs)[0]
    reaccionesPares = EFMsReaccion([indice2],reaccionesPresentes)[0]
    for efm in reaccionesPares:
        if index == 41:
            flujosGAPDENO.append([efm[indice],efm[indice2]])
        if efm[indice] == efm[indice2]:
            acopTotal += 1
        elif abs(float(efm[indice])) == abs(float(efm[indice2])):
            acopTotalInv += 1
        elif float(efm[indice]) % float(efm[indice2]) == 0: 
            acopParcial += 1
        elif float(efm[indice2]) % float(efm[indice]) == 0:
            acopParcial += 1
        else:
            acopIrr += 1
    
    listadoAcop.append(f"Para el par {i}, hay {acopTotal} acop totales positivos, {acopTotalInv} acop totales negativos, {acopParcial} acop parciales y {acopIrr} acop irregulares\n")

with open("ResultadosAcoplamientos.txt","w") as fichero:
    for i in listadoAcop:
        fichero.write(i)

with open("EstudioGAPDENO.txt","w") as file:
    file.write(str([i for i in flujosGAPDENO]))

flujoCasiTotal = 0
flujoDistinto = 0

sumaEFMsProp = []
proporcion = 0.90

while proporcion < 1.00:
    for i in flujosGAPDENO:
        if abs(float(i[0])/float(i[1])) > proporcion and abs(float(i[0])/float(i[1])) < 1.00001:
            flujoCasiTotal += 1
        elif abs(float(i[1])/float(i[0])) > proporcion and abs(float(i[1])/float(i[0])) < 1.00001:
            flujoCasiTotal += 1
    PropEFMs = flujoCasiTotal
    flujoCasiTotal = 0
    proporcion += 0.01
    sumaEFMsProp.append(PropEFMs)
    
print(sumaEFMsProp)


plt.plot([0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99], sumaEFMsProp)
plt.ylabel("EFMs")
plt.xlabel("Proporcionalidad")
plt.title("Similitud en Valores")
plt.axis([0.9,1,25000,100500])
plt.savefig("FiguraProporcionesAcoplamiento")
plt.close()