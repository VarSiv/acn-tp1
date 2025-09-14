from typing import *
from tools_visualizacion import *
import random
import pygame
import numpy as np
import json
from pathlib import Path
import sys

"""
Cosas para chequear: 

    - ver que nigun avion vuelve
    - chequear que el id esté bien
    - ⁠ver el sys.exit si está bien
    - ⁠ver bien las funciones que usamos para graficar, chequear que este todo bien y este tomando los datos bien.
"""


class Avion:
    def __init__(self,id ,velocidad:float, distancia:float, franja:int, t:float, m_atterizaje:float):
        self.id=id
        self.velocidad= velocidad
        self.distancia= distancia
        self.franja_temporal = franja
        self.tiempoAep=t
        self.m_atterizaje=m_atterizaje

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
    
    def actualizar(self):
        avance = self.velocidad * 1/60
        self.distancia = max(0,self.distancia - avance)

        if self.distancia  >= (100*1.852):
            self.franja_temporal = 5
        elif self.distancia < (100*1.852) and self.distancia >= (50*1.852):
             self.franja_temporal = 4
        elif self.distancia < (50*1.852) and self.distancia >= (15*1.852):
             self.franja_temporal = 3
        elif self.distancia < (15*1.852) and self.distancia >= (5*1.852):
             self.franja_temporal = 2
        elif self.distancia < (5*1.852): 
             self.franja_temporal = 1

    def actualizar_velocidad(self):
        if self.franja_temporal  == 4:
            self.set_velocidad(300*1.852)
        if self.franja_temporal  == 3:
            self.set_velocidad(250*1.852)
        elif self.franja_temporal  == 2:
            self.set_velocidad(200*1.852)
        elif self.franja_temporal  == 1:
            self.set_velocidad(150*1.852)
     
    
    def set_tiempoAep(self, t: float):
        self.tiempoAep = t

    def get_tiempoAep(self):
        return self.tiempoAep
    
    def get_aterrizaje(self):
        return self.m_atterizaje
    
    def set_aterrizaje(self, m:float):
        self.m_atterizaje = m
    

def calcular_tiempo_aep(avion):
    tiempos_franjas=[(5/150)*60, (10/200)*60, (35/250)*60,(50/300)*60]
    franjas=[0,5,15,50,100]
    tiempo=0
    for i in range(avion.get_franja()):
        if i+1 == avion.get_franja():
            tiempo += (((avion.get_distancia()-franjas[i])/avion.get_velocidad())*60)
        else:
            tiempo+=tiempos_franjas[i]
    
    avion.set_tiempoAep(tiempo)
    return tiempo
       
def calcular_dist_entre_aviones(lista):
    distancias=[]
    deben_ser_reubicados=[]
    for elem in range(len(lista)):
       if elem ==0: # primer avion
            distancias.append(calcular_tiempo_aep(lista[elem]))

       else:
            distancias.append(calcular_tiempo_aep(lista[elem]))
            if (abs(lista[elem-1].get_tiempoAep() - lista[elem].get_tiempoAep()))<4:
                deben_ser_reubicados.append(elem)
             
    return distancias, deben_ser_reubicados   

def debajo_minimo_de_franja(avion):
    f=avion.get_franja()
    v=avion.get_velocidad()
    ret=False
    if f==1 and v<120*1.852:
        ret=True
    elif f==2 and v<150*1.852:
        ret=True
    elif f==3 and v<200*1.852:
        ret=True
    elif f==4 and v<250*1.852:
        ret = True
    return ret

franjas_y_vel_maxima={1:150*1.852, 2:200*1.852,3:250*1.852,4:300*1.852,5:500*1.852}
def reubicar(fila_aviones, deben_ser_reubicados):
    #Antes de acutalizar las posiciones de los avione
    #movemos por minuto 
    aviones_que_se_eliminan=[]
    for i in deben_ser_reubicados:
        fila_aviones[i].set_velocidad((fila_aviones[i].get_velocidad() - 20*1.852))      # Se reduce en veinte nudos la velocidad
        if(debajo_minimo_de_franja(fila_aviones[i])):
            print("entro en -200")
            fila_aviones[i].set_velocidad(-200*1.852)                                     # Al estar por debajo del minimo de la franja se debe , retroceder 
        #avion como indice
        if not (i==0 or i==len(fila_aviones)-1): #Este caso es para analizar si un avion se puede ubicar entre dos aviones dados los requisitos. 
            if((fila_aviones[i+1].get_tiempoAep()-fila_aviones[i].get_tiempoAep())>5 and fila_aviones[i].get_tiempoAep()-fila_aviones[i-1].get_tiempoAep()>5):
                vel_max_de_franja=franjas_y_vel_maxima[fila_aviones[i].get_franja()]
                fila_aviones[i].set_velocidad(vel_max_de_franja)
                print(" se intercala el avion")



        elif i==len(fila_aviones)-1: #Este caso es para analizar si se tiene que actualizar el ultimo avion que bajo de velocidad en 20 nudos al tener ya mas de 5 minutos de distancia. 
            if( fila_aviones[i].get_tiempoAep()-fila_aviones[i-1].get_tiempoAep()>5):
                vel_max_de_franja=franjas_y_vel_maxima[fila_aviones[i].get_franja()]
                fila_aviones[i].set_velocidad(vel_max_de_franja)
                print("___________________________________________________________________________________")

        
        if(fila_aviones[i].get_distancia() > 100*1.852): #va a montevideo
            aviones_que_se_eliminan.append(fila_aviones[i])
            print(" se vuelve a montevideo el ultimo avion")
    
    for av in aviones_que_se_eliminan:
        if av in fila_aviones:
            fila_aviones.remove(av)
            
    return 



#Ejercicio 1

#viisualizacion
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AEP – Simulación + Visualización")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)


rangoSim= 10
rangoHorario = 18
p= 0.3

cant_arribados=0
cant_arribos_por_hora = np.zeros((rangoSim, rangoHorario)) ## Matriz de conteos: filas = simulaciones, columnas = horas (6..23)
cant_aviones_a_montevideo = np.zeros((rangoSim, rangoHorario)) ## Matriz de conteos: filas = simulaciones, columnas = cantidad fueron a Montevideo en la i hora ( 6..23)

for simulacion in range(rangoSim):  
    id=1
    fila_aviones: List[Avion] = []
    acc_time = 0
    for m in range(round(rangoHorario/(1/60))):
        # 1) actualizar todos
        llegados=[]
        for avion in fila_aviones:
            avion.actualizar()
            ##Quitar aquellos que ya llegaron de la lista y sumarlos al contador. 
            
            if avion.get_tiempoAep()==0 or avion.get_distancia()<=0:
                llegados.append(avion)
                cant_arribados+=1
           
            
        for avion in llegados: #Para evitar recorrer una lista como fila_aviones que vamos modificando en la linea 154
            fila_aviones.remove(avion)

        fila_aviones.sort()

        # 2) posible nuevo avión
        nuevo_detectado = np.random.binomial(1, p) 
        if nuevo_detectado==1:
            a = Avion(id, 300*1.852, 100*1.852, 4, 23.4, None)
            id+=1
            fila_aviones.append(a)
            fila_aviones.sort()

        # 3) reubicar si hace falta
        distancias, deben_ser_reubicados = calcular_dist_entre_aviones(fila_aviones) 
        # antes de reubicar
        pre_montevideo=len(fila_aviones)
        reubicar(fila_aviones, deben_ser_reubicados)
        # post de reubicar: len(fila_aviones)
        fueron_a_montevideo=pre_montevideo-len(fila_aviones)
        
        for idx, avion in enumerate(fila_aviones):
            if (idx not in deben_ser_reubicados) and (avion.get_velocidad() >= 0):
                avion.actualizar_velocidad()


        #para la visualizacion
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.display.quit()  # Cierra la ventana de visualización
                sys.exit()             # Termina la ejecución del programa

        screen.fill((20, 22, 28)) #borra lo que había dibujado en el frame anterior
        draw_marks(screen, font) #Traza marcas verticales en las posiciones de 5, 15, 50 y 100 millas náuticas.
        
        
        draw_planes(screen, font, fila_aviones) #dibuja los aviones de la fila con su id, color segun velocidad,ect.

        #para mostrar la hora
        hora_str = format_time_hhmm(acc_time)
        screen.blit(font.render(f"Hora simulada: {hora_str}", True, (255,255,255)), (WIDTH-220, 20))

        pygame.display.flip()#para que se vea todo en la pantalla
        clock.tick(10)  # para que no resfresque tan seguis y consuma mucha cpu

        # avanzar tiempo simulado en 1 min
        acc_time += 1
        
        """ for avion in fila_aviones:
            print("Simulacion:",simulacion, " minuto:",m, " avion:",avion.id, " velocidad:",avion.get_velocidad())
        print("-"*20) """

        """
        # 4) registrar arribos en la matriz y remover los llegados : sacar los aviones que tienen distancia 0 o negativa a aeroparque. son los que llegaron.
        if (m+1) % 60 ==0:
              cant_arribos_por_hora[simulacion][m//60]=cant_arribados
              cant_aviones_a_montevideo[simulacion][m//60]=fueron_a_montevideo
              cant_arribados=0
              fueron_a_montevideo=0 """

pygame.quit()


###Guardado de parametros y matrices del archivo
'''
Ejemplo de como se estructurará:
salidas_sim/
├── run_p=0.0166_sim=10.json
└── run_p=0.0083_sim=20.json
'''
def guardar_run_json(output_dir, params_dict,
                     cant_arribos_por_hora,
                     cant_aviones_a_montevideo):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    p_val = params_dict.get("p", "x")
    sim_val = params_dict.get("rangoSim", "x")

    file_name = f"run_p={p_val}_sim={sim_val}.json"
    file_path = Path(output_dir, file_name)

    data = {
        "parametros": params_dict,
        "cant_arribos_por_hora": cant_arribos_por_hora.tolist(),
        "cant_aviones_a_montevideo": cant_aviones_a_montevideo.tolist()
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Guardado {file_path}")

params = {
    "rangoSim": rangoSim,
    "p": p
}

guardar_run_json(
    output_dir="salidas_sim",    # carpeta donde guardar
    params_dict=params,
    cant_arribos_por_hora=cant_arribos_por_hora,
    cant_aviones_a_montevideo=cant_aviones_a_montevideo
)