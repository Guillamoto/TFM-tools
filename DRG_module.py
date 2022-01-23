import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#### FUNCION PARA SACAR LA MATRIZ DE REACCIONES DE UN FICHERO DE EFMs ####
def FicheroMatriz(fichero):
    with open(fichero,"r") as lectura:
        contenido = lectura.readlines()
    nombresReacciones = tuple(contenido.pop(0).split())
    matrizEFMs = set(tuple((",".join(i.split())).split(",")) for i in contenido)

    return nombresReacciones, matrizEFMs


#### FUNCION PARA CONSEGUIR, DE UN LISTADO DE EFMs, EN CUÁLES SE ENCUENTRA UNA REACCIÓN O CONJUNTO DE REACCIONES. LAS SUBLISTAS ESTAN ORDENADAS SEGUN EL ORDEN DE LA LISTA DE REACCIONES INDICADA.
def EFMsReaccion(lista, EFMs):
    matrizReacciones = []
    for i in lista:
        EFMsReaccion = []
        for j in EFMs:
            # Puedo cambiarlo a float, pero de momento me es más cómodo para trabajar.
            if j[i] != '0':
                EFMsReaccion.append(j)
        matrizReacciones.append(EFMsReaccion)

    return matrizReacciones


#### LO MISMO QUE LA FUNCIÓN ANTERIOR PERO A LA INVERSA: EN QUE EFMS NO ESTA UNA REACCION. LAS SUBLISTAS ESTAN ORDENADAS SEGUN EL ORDEN DE LA LISTA DE REACCIONES INDICADA.
def EFMsNoReaccion(lista, EFMs):
    matrizReacciones = []
    for i in lista:
        EFMsReaccion = []
        for j in EFMs:
            if j[i] == '0':
                EFMsReaccion.append(j)
        matrizReacciones.append(EFMsReaccion)

    return matrizReacciones


# DADA UNA LISTA DE EFMS, NOS CALCULA LA PROPORCION EN LA QUE APARECE CADA REACCION. HAY QUE PASARLE LA LISTA DE REACCIONES QUE HAY PARA HACER EL DICCIONARIO.
def CalculoProporciones(listaReacciones, EFMs):
    # Definición del diccionario
    proporciones = {}
    # Para cada reacción, partimos de un número de EFMs en los que aparece = 0.
    for i in listaReacciones:
        proporciones[i] = 0

    # Completamos calculando proporciones.
    for i in EFMs:
        for ind, j in enumerate(i):
            # Nota para mí: probar a cambiar a "float(j) != 0" para comprobar eficiencia.
            if j != '0':
                proporciones[listaReacciones[ind]] += 1

    # Nos devuelve el diccionario relleno.
    return proporciones

# DADA UNA LISTA DE EFMS, NOS CALCULA EN QUÉ PROPORCIÓN APARECE UNA REACCIÓN ESPECÍFICA.
def ProporcionesDiana(indice, EFMs):
    # DEFINICIÓN DE LA VARIABLE DE CONTEO
    apariciones = len([x for x in EFMs if x[indice] != "0"])
    return apariciones

# Con el diccionario de proporciones, nos escribe los resultados de forma sencilla.
def ProporcionesFichero(dictProporciones):
    nombre = input("Escoge el nombre del fichero a guardar (especifica formato): \n")
    with open(nombre,"w") as fichero:
        for ind, clave in enumerate(dictProporciones):
            fichero.write(ind, clave, dictProporciones[clave], (round(dictProporciones[clave]/sum(dictProporciones.values()),4)*100), "\n")
    print(f"Fichero {nombre} escrito correctamente.")


# Lo mismo que la anterior pero más bonito y legible, para revisión manual.
def ProporcionesFicheroVisual(dictProporciones):
    nombre = input("Escoge el nombre del fichero a guardar (especifica formato): \n")
    with open(nombre,"w") as fichero:
        for ind, clave in enumerate(dictProporciones):
            fichero.write(f"{ind} ||| {clave} -> {dictProporciones[clave]} / {round(dictProporciones[clave]/sum(dictProporciones.values()),4)*100} % \n")
    print(f"Informe {nombre} escrito correctamente.")


# Función para, mediante diccionarios de proporciones, conseguir un dataframe. SE SOBREENTIENDEN QUE SON LAS MISMAS REACCIONES, EN EL MISMO ORDEN.
def dfProporciones(listaReacciones,*args):
    # Por hacerlo mas eficiente, primero se hace un "array" de listas anidadas.
    listado = [listaReacciones]
    for i in args:
        listado.append([i[j] for j in i])
    
    df = pd.DataFrame(listado[1:], columns=listado[0])
    return df.T

# Genera un histograma de las longitudes de los EFMs indicados comparando con los EFMs totales.
def HistogramaReaccion(listaEFMs, EFMsTotales,nombreFichero):
    # Calculamos la longitud de los EFMs de la lista donde esta nuestra reaccion.
    longitudesReaccion = []
    for i in listaEFMs:
        longitud = len([x for x in i if i[x] != '0'])
        longitudesReaccion.append(longitud)

    # Calculamos la longitud de TODOS los EFMs para presentar el histograma total a modo de contraste.
    longitudesTotal = []
    for i in EFMsTotales:
        longitud = len([x for x in i if i[x] != '0'])
        longitudesTotal.append(longitud)

    plt.hist(longitudesTotal, rwidth = 0.80, bins = [i for i in range(60)])
    plt.hist(longitudesReaccion, rwidth = 0.80, bins = [i for i in range(60)])
    plt.savefig(nombreFichero)
    plt.close()


def CalcularLongitud(listaEFMs):
    # Calculamos la longitud de los EFMs de la lista donde esta nuestra reaccion.
    longitudesReaccion = (len([e for e in i if e != 0]) for i in listaEFMs)

    # for i in listaEFMs:
    #     longitud = len([])
    #     for j in i:
    #         if float(j) != 0:
    #             longitud += 1
    #     longitudesReaccion.append(longitud)
    return longitudesReaccion

# BARRIDO INICIAL PARA ELIMINAR PARES DE ACOPLAMIENTO.
def BarridoAcoplamientos(sets): 
    sets = list(sets)   
    setsfinales = []
    while 0 < len(sets):
        ref = set(sets[0])
        removed = []
        for i in sets:
            if i[0] in ref or i[1] in ref:
                ref = ref.union(set(i))
                removed.append(i)
        sets = [e for e in sets if e not in removed]
        setsfinales.append(ref)
    return setsfinales

def CombinarAcoplamiento(acoplamientos):
    # Escogemos una referencia
    for i in acoplamientos:
        for ind, j in enumerate(acoplamientos[1:]):
            for k in j:
                if k in i:
                    i = i.union(j)
                    acoplamientos.pop(ind+1)
                    return CombinarAcoplamiento(acoplamientos)
        return acoplamientos

def TipoReacciones(modelo,nombreModelo):
    """
    Esta funcion nos permite calcular el tipo de la reacción, ajusta las irreversibles, desdobla las reversibles y elimina las bloqueadas en el modelo resultante.
    Si se incluyen las reacciones bloqueadas es para simplificar su eliminacion o estudio.
    Entrada: el modeo a analizar y el nombre del nuevo modelo.
    Salida: nuevo modelo ya alterado.
    """
    # Se definen las cuatro listas de reacciones necesarias.
    reversibles = []
    irreversibles = []
    irreversibles_i = []
    bloqueadas = []

    # Definimos el maximo de error, es decir, a partir de que valor consideramos que el valor es 0.
    error = 10**-12

    # Con enumerate tenemos tanto el indice (i) como el valor (r) al mismo tiempo.
    for i, r in enumerate(modelo.reactions):
        # Se define el objetivo a optimizar y se busca tanto su minimo como su maximo.
        modelo.objective = r
        solucionMin = modelo.optimize(objective_sense="minimize")
        solucionMax = modelo.optimize(objective_sense="maximize")
        minimo = solucionMin.objective_value
        maximo = solucionMax.objective_value
        # Cuando la reaccion no esta bloqueada...
        if abs(minimo) > error or abs(maximo) > error:
            # Si la reaccion es reversible...
            if minimo < 0 and maximo > 0:
                # Añadimos su indice a la lista de reacciones reversibles
                reversibles.append(i)
            # Si la reaccion es irreversible...
            elif minimo >= 0 and maximo > 0:
                irreversibles.append(i)
            # Si la reaccion es irreversible inversa...
            elif minimo < 0 and maximo <= 0:
                irreversibles_i.append(i)
        # Cuando no se cumple el criterio, lo que tenemos es una funcion bloqueada (su minimo y maximo es 0).
        else:
            bloqueadas.append(i)

    # Lo que se devuelve es una lista con todas las sublistas introducidas en el orden especificado.
    return [reversibles, irreversibles, irreversibles_i, bloqueadas]