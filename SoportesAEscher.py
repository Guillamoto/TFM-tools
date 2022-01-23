#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cobra
from cobra.test import create_test_model
import numpy as np
modelo = create_test_model("textbook")

reacciones=[]
for i in range(len(modelo.reactions)):
    reacciones.append(modelo.reactions[i].id)


# In[4]:


fichero=open("./datos/EFMs.txt","r")
texto=fichero.readlines()
fichero.close()
nombres=texto[0]
nombres2=nombres.split()
for i in range(len(nombres2)):
    nombres2[i]=nombres2[i][2:]
reacciones2=[]
for nombre in reacciones:
    if nombre in nombres:
        reacciones2.append(nombre)


# In[5]:


traduce=dict()
for i in range(len(nombres2)):
    for j in range(len(modelo.reactions)):
        if modelo.reactions[j].id==nombres2[i]:
            traduce[i]=j


# In[6]:


interesantes=[]
soportes=[]
for i in range(1,len(texto)):
    EFM=texto[i]
    EFM2=EFM.split()
    sop=[]
    for j in range(len(EFM2)):
        val=eval(EFM2[j])
        if not abs(val)<10**-12:
            indice=traduce[j]
            sop.append(traduce[j])
    if len(sop)<20:
        interesantes.append(i)
        soportes.append(sop)


# In[7]:


indices=interesantes
for i in range(len(indices)):
    nombre="./Soluciones/solucion_"+str(indices[i])+".csv"
    fichero=fichero=open(nombre,"w+")
    lineas=[",fluxes"]
    EFM=texto[indices[i]+1]
    EFM2=EFM.split()
    for j in range(len(modelo.reactions)):
        if j in soportes[i]:
            linea="\n"+modelo.reactions[j].id+",1.0"
        else:
            linea="\n"+modelo.reactions[j].id+",0.0"
        lineas.append(linea)
    fichero.writelines(lineas)
    fichero.close()

