from typing import *
import random

import numpy as np
class Avion:
    def __init__(self, velocidad:float, distancia:float):
        self.velocidad= velocidad
        self.distancia= distancia

    def get_velocidad(self):
        return self.velocidad
    
    def get_distancia(self):
        return self.distancia
    
    def set_velocidad(self, vel:float):
        self.velocidad = vel 
        return

    def set_distancia(self, dist:float):
        self.distancia=dist
        return
    
    def __lt__(self, other):
        return self.distancia < other.distancia
    
    def actualizar(self, delta):
        avance = self.velocidad * delta
        self.distancia = self.distancia - avance
        if self.distancia  >= (100*1,852):
            self.velocidad= 500*1,852
        if self.distancia < (100*1,852) and self.distancia >= (50*1,852):
             self.velocidad= 300*1,852
        if self.distancia < (50*1,852) and self.distancia >= (15*1,852):
             self.velocidad= 250*1,852
        if self.distancia < (15*1,852) and self.distancia >= (5*1,852):
             self.velocidad= 200*1,852
        if self.distancia < (5*1,852): 
             self.velocidad= 150*1,852
    

#Ejercicio 1

fila_aviones: List[Avion] = []
rangoSim= 10000
rangoHorario = 18
delta= 1/60
Lambda = 0.5

for simulacion in range(rangoSim):  
    for m in range(round(rangoHorario/delta)):
        for avion in range(fila_aviones):
            dist_avion = avion.get_distancia()

        cant_detectados = np.random.poisson(Lambda)
        for avion in range(cant_detectados):
            a= Avion(300*1,852, 100*1,852)
            fila_aviones.append(a)
        



    