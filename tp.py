from typing import *
import random

import numpy as np
class Avion:
    def __init__(self, velocidad:float, distancia:float, franja:int):
        self.velocidad= velocidad
        self.distancia= distancia
        self.franja_temporal = franja

    def get_velocidad(self):
        return self.velocidad
    
    def get_distancia(self):
        return self.distancia
    
    def get_franja(self):
        return self.franja_temporal
    
    def set_velocidad(self, vel:float):
        self.velocidad = vel 
        return

    def set_distancia(self, dist:float):
        self.distancia=dist
        return
    
    def __lt__(self, other):
        return self.distancia < other.distancia
    
    def actualizar(self, delta, retrocede):
        avance = self.velocidad * delta
        self.distancia = (1-retrocede)* (self.distancia - avance) + (retrocede)* (self.distancia + avance) 
        if self.distancia  >= (100*1.852):
            self.velocidad= 500*1.852
            self.franja_temporal = 5
        elif self.distancia < (100*1.852) and self.distancia >= (50*1.852):
             self.velocidad= 300*1.852
             self.franja_temporal = 4
        elif self.distancia < (50*1.852) and self.distancia >= (15*1.852):
             self.velocidad= 250*1.852
             self.franja_temporal = 3
        elif self.distancia < (15*1.852) and self.distancia >= (5*1.852):
             self.velocidad= 200*1.852
             self.franja_temporal = 2
        elif self.distancia < (5*1.852): 
             self.velocidad= 150*1.852
             self.franja_temporal = 1


def calcular_distancia_aep(avion):
    tiempos_franjas=[(5/150)*60, (10/200)*60, (35/250)*60,(50/300)*60]
    franjas=[0,5,15,50,100]
    dist=0
    for i in range(avion.get_franja()):
        if i+1 == avion.get_franja():
            dist += (((avion.get_distancia()-franjas[i])/avion.get_velocidad())*60)
        else:
            dist+=tiempos_franjas[i]
        
'''
def calcular_dist_entre_aviones(lista):
    distancias=[]


    for elem in range(len(lista)-1):
        if lista[elem].get_franja() == lista[elem+1].get_franja():
            dist_av1= (lista[elem].get_distancia()/lista[elem].get_velocidad())*60
            dist_av2= (lista[elem+1].get_distancia()/lista[elem+1].get_velocidad())*60
            distancias.append(abs(dist_av1-dist_av2))
        else:
            dist_av1= (lista[elem].get_distancia()/lista[elem].get_velocidad())*60
            dist_av2= (lista[elem+1].get_distancia()/lista[elem+1].get_velocidad())*60
            if lista[elem].get_franja() - lista[elem+1].get_franja()>1:
        
        
    return distancias

'''   


#Ejercicio 1

rangoSim= 10000
rangoHorario = 18
delta= 1/60
Lambda = 0.5

for simulacion in range(rangoSim):  
    fila_aviones: List[Avion] = []
    for m in range(round(rangoHorario/delta)):
        for avion in fila_aviones:
            avion.actualizar()

        cant_detectados_nuevos = np.random.poisson(Lambda)
        for avion in range(cant_detectados_nuevos):
            a= Avion(300*1.852, 100*1.852, 4)
            fila_aviones.append(a)
        fila_aviones.sort()
        distancias = calcular_dist_entre_aviones(fila_aviones)




class Avion:
    _NEXT_ID = 0
    def __init__(self, velocidad_kmh, distancia_km):
        self.id = Avion._NEXT_ID; Avion._NEXT_ID += 1
        self.velocidad = velocidad_kmh   # km/h
        self.distancia = distancia_km    # km
        self.sentido = +1                # +1: hacia la pista, -1: retroceso
        self.en_retroceso = False

    def iniciar_retroceso(self):
        self.sentido = -1
        self.velocidad = 200 * 1.852     # 200 kt
        self.en_retroceso = True

    def terminar_retroceso(self):
        self.sentido = +1
        self.en_retroceso = False

    def actualizar(self, delta_horas):
        avance = self.velocidad * delta_horas * self.sentido
        # si sentido = +1: distancia -= (v*dt); si -1: distancia aumenta
        self.distancia = max(0.0, self.distancia - avance)

        # (solo si se acerca) setear la Vmax por rango
        if self.sentido == +1:
            d = self.distancia
            if d > 100*1.852:      self.velocidad = 500*1.852
            elif d > 50*1.852:     self.velocidad = 300*1.852
            elif d > 15*1.852:     self.velocidad = 250*1.852
            elif d > 5*1.852:      self.velocidad = 200*1.852
            else:                  self.velocidad = 150*1.852

    