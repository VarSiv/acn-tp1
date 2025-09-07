from typing import *
import random
import numpy as np

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
        self.distancia = (self.distancia - avance)
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
    
    #Nuevo
    def set_tiempoAep(self, t: float):
        self.tiempoAep = t
    #Nuevo
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
    #Nuevo
    avion.set_tiempoAep(tiempo)
    return tiempo
       

#propuesta
def calcular_dist_entre_aviones(lista):
    distancias=[]
    deben_ser_reubicados=[]
    for elem in range(len(lista)):
       if elem ==0: #Osea es el primer avion
            distancias.append(calcular_tiempo_aep(lista[elem]))

       else:
            distancias.append(calcular_tiempo_aep(lista[elem]))
            if (abs(lista[elem-1].get_tiempoAep() - lista[elem].get_tiempoAep()))<4:
                deben_ser_reubicados.append(elem)
        
    #Si reubicamos tenemos que recalcular todo esto        
    return distancias, deben_ser_reubicados   

def debajo_minimo_de_franja(avion):
    f=avion.get_franja()
    v=avion.get_velocidad()
    ret=False
    if f==1 and v<120*1.852:
        #avion.set_franja=1
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
    for i in deben_ser_reubicados:
        fila_aviones[i].set_velocidad((fila_aviones[i].get_velocidad() - 20*1.852))      # tiempo = distancia / velocidad 
        if(debajo_minimo_de_franja( fila_aviones[i])):
            fila_aviones[i].set_velocidad(-200*1.852)
        #avion como indice
        if not (i==0 or i==len(fila_aviones)-1): 
            if((fila_aviones[i+1].get_distancia()-fila_aviones[i])>5 and fila_aviones[i].get_distancia()-fila_aviones[i-1]>5):
                vel_max_de_franja=franjas_y_vel_maxima[fila_aviones[i].get_franja()]
                fila_aviones[i].set_velocidad(vel_max_de_franja)

            else: #va a montevideo
                fila_aviones.remove(fila_aviones[i])


        else: #Este caso es para analizar si se tiene que reubicar el ultimo avion
            fila_aviones.remove(fila_aviones[i]) 
        
    return 



#Ejercicio 1
rangoSim= 10
rangoHorario = 18
p= 1/60
id=1
#cant_arribados=0
##cant_arribos_por_hora = np.zeros((rangoSim, rangoHorario))) ## Matriz de conteos: filas = simulaciones, columnas = horas (6..23)
for simulacion in range(rangoSim):  
    fila_aviones: List[Avion] = []

    for m in range(round(rangoHorario/(1/60))):
        # 1) actualizar todos
        for avion in fila_aviones:
            avion.actualizar()
            ##Quitar aquellos que ya llegaron de la lista y sumarlos al contador. 
            #if avion.get_tiempoAep==0 or avion.get_distancia<=0:
                #fila_aviones.remove(avion)
                #cant_arribados+=1

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
        # pre_montevideo=len(fila_aviones)
        reubicar(fila_aviones, deben_ser_reubicados)
            # post de reubicar: len(fila_aviones)
        # fueron_a_montevideo=len(fila_aviones)-pre_montevideo
        
        for avion in fila_aviones:
            index = fila_aviones.index(avion)
            print("Simulacion: ", simulacion, "minuto", m, "avion", index, "velocidad", avion.get_velocidad())
        print("-"*20)

        
        # 4) registrar arribos en la matriz y remover los llegados : sacar los aviones que tienen distancia 0 o negativa a aeroparque. son los que llegaron.
        ## if (m+1) % 60 ==0:
        ##      cant_arribos_por_hora[simulacion][m//60]=cant_arribados
        ##      cant_arribados=0
    #

##cta b : agregar una col xa reigstrar lo de montevideo?!!!

############################################################
import pygame
import random
from typing import List

# ====== Usa tu clase Avion y utilidades ======
NM = 1.852  # km por milla náutica

# --------- Colores por franja ----------
def color_por_dist(dist_km: float):
    if dist_km < 5*NM:      return (70, 200, 70)   # 0–5 mn
    elif dist_km < 15*NM:   return (70, 130, 255)  # 5–15 mn
    elif dist_km < 50*NM:   return (255, 165, 0)   # 15–50
    elif dist_km < 100*NM:  return (255, 80, 80)   # 50–100
    else:                   return (180, 180, 180) # >100

# ====== Parámetros de visual ======
WIDTH, HEIGHT = 1200, 420
MARGIN_L, MARGIN_R = 80, 40
TRACK_LEN = WIDTH - (MARGIN_L + MARGIN_R)  # largo de "cola" en pixeles

def x_from_dist_km(dist_km: float) -> int:
    # 0 mn = AEP (x=MARGIN_L), 100 mn = extremo derecho
    frac = max(0.0, min(1.0, dist_km / (100*NM)))
    return int(MARGIN_L + frac * TRACK_LEN)

def draw_marks(screen, font):
    # pista
    pygame.draw.line(screen, (230, 230, 230), (MARGIN_L, 60), (MARGIN_L, HEIGHT-60), 4)
    screen.blit(font.render("AEP", True, (230, 230, 230)), (MARGIN_L-24, 25))
    # marcas 5/15/50/100 mn
    for mn, label in [(5, "5 mn"), (15, "15 mn"), (50, "50 mn"), (100, "100 mn")]:
        x = x_from_dist_km(mn*NM)
        pygame.draw.line(screen, (120,120,120), (x, 80), (x, HEIGHT-80), 1)
        screen.blit(font.render(label, True, (160,160,160)), (x-20, HEIGHT-30))

def draw_planes(screen, font, fila_aviones: List):
    # Y por fila (separados)
    y0, dy = 110, 26
    for i, av in enumerate(fila_aviones):
        d = av.get_distancia()
        x = x_from_dist_km(d)
        y = y0 + i*dy
        col = (230, 80, 80) if getattr(av, "en_retroceso", False) else color_por_dist(d)
        #pygame.draw.circle(screen, col, (x, y), 7)
        pygame.draw.polygon(screen, col, [(x, y), (x+15, y-8), (x+15, y+8)])
        screen.blit(font.render(f"ID {av.id}", True, (255,255,0)), (x-15, y-20))
        # velocidad y distancia (opcional)
        v = int(av.get_velocidad()/NM)  # en kt
        #screen.blit(font.render(f"{v} kt", True, (200,200,200)), (x+10, y-10))

def format_time_hhmm(total_minutes: float) -> str:
    h = int(total_minutes // 60) + 6
    m = int(total_minutes % 60)
    return f"{h:02d}:{m:02d}"

def pygame_anim(sim_step_fn, get_fila_fn, fps=30, minutos_por_seg=2.0):
    """
    sim_step_fn(delta_horas) -> ejecuta un paso de simulación (tu lógica)
    get_fila_fn() -> devuelve la lista actual de aviones
    fps: frames por segundo
    minutos_por_seg: cuántos minutos simulados querés avanzar por segundo real
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AEP – Visualización")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16)

    running = True
    acc_time = 0.0  # minutos simulados acumulados
    while running:
        dt_ms = clock.tick(fps)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # avanzar simulación: dt real -> minutos simulados -> horas
        minutos_sim = (dt_ms/1000.0) * minutos_por_seg
        delta_h = minutos_sim / 60.0

        sim_step_fn(delta_h)   # <-- acá llamás tu paso de simulación

        acc_time += minutos_sim

        # dibujar
        screen.fill((20, 22, 28))
        draw_marks(screen, font)
        draw_planes(screen, font, get_fila_fn())
        # Mostrar hora simulada
        hora_str = format_time_hhmm(acc_time)
        screen.blit(font.render(f"Hora simulada: {hora_str}", True, (255,255,255)), (WIDTH-220, 20))
        pygame.display.flip()

    pygame.quit()

# =================== EJEMPLO MÍNIMO DE INTEGRACIÓN ===================
# Esto es solo para mostrar cómo enchufarlo; reemplazalo por tu lógica real.
class AvionDemo:
    def __init__(self, v_kmh, d_km, id): 
        self.velocidad = v_kmh
        self.distancia = d_km
        self.en_retroceso = False
        self.id=id
    def get_velocidad(self): return self.velocidad
    def get_distancia(self): return self.distancia
    def set_velocidad(self, v): self.velocidad = v
    def set_distancia(self, d): self.distancia = d
    def actualizar(self, delta_horas, retrocede=False):
        v = 200*NM if retrocede else self.velocidad
        self.distancia = max(0.0, self.distancia - v*delta_horas)

def demo():
    fila = [AvionDemo(300*NM, 100*NM, id=1)]
    p = 1/60  # 1 arribo por hora

    contador_id = 2   # para asignar IDs únicos

    def sim_step(delta_h):
        nonlocal contador_id
        if random.random() < p * (delta_h*60):
            fila.append(AvionDemo(300*NM, 100*NM, id=contador_id))
            contador_id += 1
        
        for av in fila:
            av.actualizar(delta_h, getattr(av, "en_retroceso", False))
        # limpiar aterrizados
        fila[:] = [av for av in fila if av.get_distancia() > 0.0]

    def get_fila(): return fila

    pygame_anim(sim_step, get_fila, fps=30, minutos_por_seg=6.0)

if __name__ == "__main__":
    demo()
