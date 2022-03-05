#####################################
#Author: Monica Ocaña Bastante
#Date: 2021/11/15
#Estrategia evolutiva cuyo fitness se obtiene de una pagina web
#####################################
from typing import TYPE_CHECKING
from warnings import simplefilter
import requests as rq
import random as r
import numpy as np
import os
import pathlib as pat
from datetime import datetime
#####################################################
#VARIABLES##############VARIABLES####################
#####################################################

#parametros
sizepoblacion = 1 #embergadura de poblacion
motores = 10
sizeCromosoma = motores*2 #longitud de cromosomas Motores y la varianza de cada uno
web ='http://memento.evannai.inf.uc3m.es/age/robot10?' #pagina con la funcion
grados = 0 #media en torno a la cual se genera la normal
varianzaInicial = 100 #varianza para inicializar la poblacion
umbral = 10 #numero de veces se generan hijos antes de cambiar la varianza
contador = 0 #veces mejora por ciclo
c = 0.82
parada = 1e-15#varianza que se debe alcanzar para detener el codigo
rondas = 1e10 #numero maximo de veces que se haran las 10 evaluaciones
pruebas = 20  #numero de veces queremos que se ejecute el codigo con los mismos parametros
ruta= "ficheros/" #ruta donde queremos que se guarden los ficheros

#auxiliares
bandera = False #False, no se cumple criterio de parada. True, se cumple criterio
numeroF = 0.0
numeroI = 0
cromosoma=""
conectado=False #False, no se ha podido conectar. True, se ha logrado conectar
aux="c"
igual="="
ampersan="&"
aux2=1
comienzo=datetime.now().strftime('%H:%M:%S')
fin=""

#Inicializamos la matriz de la poblacion inicial de cada ciclo
#son tan largos como un cromosoma mas un espacio extra para poder guardar el valor de fitnnes del individuo
poblacionInicial = []
for i in range(sizepoblacion):
    a = [0]*(sizeCromosoma+1)
    poblacionInicial.append(a)

poblacion=[]
for i in range(sizepoblacion):
    a = [0]*(sizeCromosoma)
    poblacion.append(a)

#CREACION DE FICHEROS 
nombreMejor=ruta+"individuos"
nombreCSV=ruta+"datosFitness"
granGlobal=open("datosGlobalesGrandes.csv","a")
texto=".txt"
csvT=".csv"
nombreCSV2=ruta+"datosGlobales"+csvT
try:
    csv2 = open (nombreCSV2,"a")
except:
    print("Ruta erronea. Generando carpeta y cambiando ruta")
    try:
        os.mkdir(str(pat.Path(__file__).parent.absolute())+"/archivosEE")
        nombreCSV2="archivosEE/datosGlobales"+csvT
        ruta="archivosEE/"
        csv2 = open (nombreCSV2,"a")
    except:
        print("Error al crear carpeta. Creando en carpeta programa.")
        nombreCSV2="datosGlobales"+csvT
        csv2 = open (nombreCSV2,"a")
csv2.write("Error;umbral;parada;c;rondas;generaciones\n")
#granGlobal.write("Error;umbral;parada;c;rondas;generaciones;motores\n")
#BUCLE DE LAS PRUEBAS
#Ejecuta el codigo principal tantas veces como se quiera con los mismos parametros
if pruebas < 1:
    pruebas=1

for z in range (pruebas):
    nombreMejor=ruta+"individuos"
    nombreCSV=ruta+"datosFitness"
    if(z!=(pruebas-1)):
        print("Prueba "+str(z+1)+"\n")
    else:
        print("Ultima prueba \n")
    #inicializar poblacion inicial
    for i in range(sizepoblacion):
        for x in range(sizeCromosoma):
            if(x%2==0):
                numeroF=r.gauss(grados,varianzaInicial)
                poblacionInicial[i][x]=numeroF
            else:
                numeroI=r.randint(10,20)
                numeroF=float(numeroI)+r.random()
                poblacionInicial[i][x]=numeroF

    #ficheros auxiliares. Creacion
    nombreMejor=nombreMejor+str(z)+texto
    nombreCSV=nombreCSV+str(z)+csvT
    try:
        mejores = open(nombreMejor,"a")
    except:
        nombreCSV2 ="individuos"+str(z)+texto
        mejores=open(nombreCSV2,"a")
    try:
        csv = open(nombreCSV,"a")
    except:
        nombreCSV2 ="datosFitness"+str(z)+texto
        csv = open(nombreCSV2,"a")
    csv.write("Epadre;Ehijo\n")#cabecera csv
    
    #reinicio de variables auxiliares
    i=0
    bandera=False
    #bucle principal
    while i<rondas and bandera==False:
        print("Generacion: "+str(i))
        contador = 0
        #####################################################
        #EVALUACION###################EVALUACION#############
        #####################################################
        for k in range (umbral):
            cromosoma=""
            aux2=1
            for j in range(sizepoblacion):
                for cr in range(sizeCromosoma):
                    if(cr%2==0):
                        if(cr!=0):
                            aux2+=1
                            cromosoma=cromosoma+ampersan+aux+str(aux2)+igual+str(poblacionInicial[j][cr])
                        else:
                            cromosoma=cromosoma+aux+str(aux2)+igual+str(poblacionInicial[j][cr])
            conectado=False
            while not conectado:
                try:
                    resultado=rq.get(web + cromosoma)
                    conectado=True
                except:
                    conectado=False
                    print("Fallo de conexion. Volviendo a intentar")
           #print(resultado.text)
            poblacionInicial[0][sizeCromosoma]=float(resultado.text)
        #####################################################
        #CRUCE###################CRUCE#######################
        #####################################################
            for j in range(sizepoblacion):
                for cr in range(sizeCromosoma):
                    if(cr%2==0):
                        poblacion[j][cr]=r.gauss(0,poblacionInicial[j][(cr+1)])+poblacionInicial[j][cr]
                    else:
                        poblacion[j][cr]=poblacionInicial[j][cr]

           
            #guardar
            csv.write(str(poblacionInicial[0][sizeCromosoma])+";"+resultado.text+"\n")

        #####################################################
        #EVALUACION###################EVALUACION#############
        #####################################################
            cromosoma=""
            aux2=1
            #pasar cromosoma al string requerido para el servidor
            for j in range(sizepoblacion):
                for cr in range(sizeCromosoma):
                    if(cr%2==0):
                        if(cr!=0):
                            aux2+=1
                            cromosoma=cromosoma+ampersan+aux+str(aux2)+igual+str(poblacion[j][cr])
                        else:
                            cromosoma=cromosoma+aux+str(aux2)+igual+str(poblacion[j][cr])
            conectado=False

            #obtener valor del error
            while not conectado:
                try:
                    resultado=rq.get(web + cromosoma)
                    conectado=True
                except:
                    conectado=False
                    print("Fallo de conexion. Volviendo a intentar")

            if(float(resultado.text)<poblacionInicial[0][sizeCromosoma]):
               contador+=1 
               for j in range(sizepoblacion):
                    for cr in range(sizeCromosoma):
                       poblacionInicial[j][cr]=poblacion[j][cr]       

            i+=1
        #####################################################
        #MUTACION#############MUTACION#######################
        #####################################################
        valor=contador/umbral
        #cambio dela varianza
        if(valor>0.2):
            for j in range(sizepoblacion):
               for cr in range(sizeCromosoma):
                   if(cr%2!=0):
                      poblacionInicial[j][cr]=poblacionInicial[j][cr]/c
        elif(valor<0.2):
           for j in range(sizepoblacion):
              for cr in range(sizeCromosoma):
                 if(cr%2!=0):
                        poblacionInicial[j][cr]=poblacionInicial[j][cr]*c
        contador = 0
        print("Fitness actual: "+str(poblacionInicial[0][sizeCromosoma]))
    
        #####################################################
        #        COMPROBACION DE CONDICION DE PARADA        #
        #####################################################
        for j in range(sizepoblacion):
          for cr in range(sizeCromosoma):
               if(cr%2!=0):
                   if(poblacionInicial[j][cr]<=parada):
                      bandera=True
        if(bandera):
            print("Tenemos una gran solucion")
        i+=0
    #fin bucle
    print("Valor final: "+str(poblacionInicial[0][sizeCromosoma]))

    #escribir valores finales en fichero
    csv2.write(str(poblacionInicial[0][sizeCromosoma])+";"+str(umbral)+";"+str(parada)+";"+str(c)+";"+str(rondas)+";"+str(i)+"\n")
    granGlobal.write(str(poblacionInicial[0][sizeCromosoma])+";"+str(umbral)+";"+str(parada)+";"+str(c)+";"+str(rondas)+";"+str(i)+";"+str(motores)+"\n")
    cromosma=""
    for x in range (sizepoblacion):
        for cr in range(sizeCromosoma):
            cromosoma=cromosoma+str(poblacionInicial[x][cr])
    mejores.write(cromosoma+"\nFitness: "+str(poblacionInicial[0][sizeCromosoma]))
    #cierre de ficheros auxiliares
    mejores.close()
    csv.close()

print("Fin de las pruebas")
print("Ficheros guardados en: "+ruta)
csv2.close()
granGlobal.close()
fin=datetime.now().strftime('%H:%M:%S')
print("Las pruebas comenzaron a: "+comienzo)
print("Las pruebas terminaron a: "+fin)