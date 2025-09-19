from typing import *
from tools_visualizacion import *
import random
import pygame
import numpy as np
import json
from pathlib import Path
import sys
from tp import *

# ========================
# PARÁMETROS DE SIMULACIÓN
# ========================
rangoSim= 100000
rangoHorario = 18
lambdas = [0.02, 0.1, 0.2, 0.5, 1]

for p in lambdas:
    cant_arribados=0
    cant_arribos_por_hora = np.zeros((rangoSim, rangoHorario)) 
    cant_aviones_a_montevideo = np.zeros((rangoSim, rangoHorario)) 
    cant_detectados_por_hora = np.zeros((rangoSim, rangoHorario))   
    cant_congestion_por_hora =  np.zeros((rangoSim, rangoHorario),  dtype=int)

    for simulacion in range(rangoSim):  
        print("arranca simulacion numero:", simulacion)
        id=1
        inicia_tormenta =  random.randint(0, 1049) #por minuto es de las 6am hasta las 11.29 pm inclusive
        fila_aviones: List[Avion] = []
        acc_time = 0
        cant_detectados=0
        fueron_a_montevideo=0
        ids_congestionados = set()   # guardamos todos los que ALGUNA VEZ bajaron vel (AEP o MVD)
        prev_cong_size = 0
        for m in range(round(rangoHorario/(1/60))):
            # 1) actualizar todos
            llegados=[]
            for avion in fila_aviones:
                avion.actualizar()
                if avion.get_tiempoAep()==0 or avion.get_distancia()<=0:
                    llegados.append(avion)
                    cant_arribados+=1
            
            for avion in llegados: 
                fila_aviones.remove(avion)

            fila_aviones.sort()

            # 2) posible nuevo avión (con tormenta)

            en_tormenta = inicia_tormenta <= m < (inicia_tormenta + 30)

            if en_tormenta:
                # todos los que ya están, hacen 180 y toman vel negativa máxima de franja
                for avion in fila_aviones:
                    vel_max_de_franja = franjas_y_vel_maxima[avion.get_franja()]
                    avion.set_velocidad(-vel_max_de_franja)

                # nuevos detectados solo se registran como detectados y Montevideo
                nuevo_detectado = np.random.binomial(1, p)
                if nuevo_detectado == 1:
                    cant_detectados += 1
                    fueron_a_montevideo += 1
                    # no se agrega a fila_aviones

            else:
                # funcionamiento normal
                nuevo_detectado = np.random.binomial(1, p)
                if nuevo_detectado == 1:
                    a = Avion(id, 300*1.852, 100*1.852, 4, 23.4, None, False)
                    id += 1
                    fila_aviones.append(a)
                    fila_aviones.sort()
                    cant_detectados += 1   

            # 3) reubicar si hace falta
            distancias, deben_ser_reubicados = calcular_dist_entre_aviones(fila_aviones) 
            pre_montevideo = len(fila_aviones)
            reubicar(fila_aviones, deben_ser_reubicados, ids_congestionados)
            fueron_a_montevideo += (pre_montevideo - len(fila_aviones))
            
            for idx, avion in enumerate(fila_aviones):
                if (idx not in deben_ser_reubicados) and (avion.get_velocidad() >= 0):
                    avion.actualizar_velocidad()

            # 4) registrar por hora
            if (m+1) % 60 == 0:
                h = m // 60
                cant_arribos_por_hora[simulacion][h] = cant_arribados
                cant_aviones_a_montevideo[simulacion][h] = fueron_a_montevideo
                cant_detectados_por_hora[simulacion][h] = cant_detectados
                nuevos = len(ids_congestionados) - prev_cong_size
                cant_congestion_por_hora[simulacion, h] = max(0, nuevos)  
                prev_cong_size = len(ids_congestionados)

                cant_arribados = 0
                fueron_a_montevideo = 0
                cant_detectados = 0


    pygame.quit()
    params = {
    "rangoSim": rangoSim,
    "p": p
    }

    guardar_run_json(
        output_dir="salidas_sim",
        params_dict=params,
        cant_arribos_por_hora=cant_arribos_por_hora,
        cant_aviones_a_montevideo=cant_aviones_a_montevideo,
        cant_detectados_por_hora=cant_detectados_por_hora,
        cant_congestion_por_hora=cant_congestion_por_hora
        
    )

