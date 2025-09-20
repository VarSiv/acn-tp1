from typing import List
import random
import numpy as np
import pygame

NM = 1.852  # km per nautical mile
p = 0.5     # probability of new plane

# --------- Avion class ----------
class Avion:
    def __init__(self,id ,velocidad:float, distancia:float, franja:int, t:float, m_atterizaje:float):
        self.id=id
        self.velocidad= velocidad
        self.distancia= distancia
        self.franja_temporal = franja
        self.tiempoAep=t
        self.m_atterizaje=m_atterizaje
        self.en_retroceso = False

    def get_velocidad(self): return self.velocidad
    def get_distancia(self): return self.distancia
    def get_franja(self): return self.franja_temporal
    def set_velocidad(self, vel:float): self.velocidad = vel
    def set_distancia(self, dist:float): self.distancia=dist
    def set_tiempoAep(self, t: float): self.tiempoAep = t
    def get_tiempoAep(self): return self.tiempoAep
    def get_aterrizaje(self): return self.m_atterizaje
    def set_aterrizaje(self, m:float): self.m_atterizaje = m

    def __lt__(self, other): return self.distancia < other.distancia

    def actualizar(self):
        avance = self.velocidad * 1/60
        self.distancia = max(0,self.distancia - avance)
        # update franja
        if self.distancia  >= (100*NM): self.franja_temporal = 5
        elif self.distancia >= (50*NM): self.franja_temporal = 4
        elif self.distancia >= (15*NM): self.franja_temporal = 3
        elif self.distancia >= (5*NM): self.franja_temporal = 2
        else: self.franja_temporal = 1

    def actualizar_velocidad(self):
        f = self.franja_temporal
        if f==4: self.velocidad = 300*NM
        elif f==3: self.velocidad = 250*NM
        elif f==2: self.velocidad = 200*NM
        elif f==1: self.velocidad = 150*NM

# ----- Functions for timing & repositioning -----
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
       distancias.append(calcular_tiempo_aep(lista[elem]))
       if elem>0 and abs(lista[elem-1].get_tiempoAep() - lista[elem].get_tiempoAep())<4:
           deben_ser_reubicados.append(elem)
    return distancias, deben_ser_reubicados   

def debajo_minimo_de_franja(avion):
    f=avion.get_franja()
    v=avion.get_velocidad()
    if f==1 and v<120*NM: return True
    if f==2 and v<150*NM: return True
    if f==3 and v<200*NM: return True
    if f==4 and v<250*NM: return True
    return False

franjas_y_vel_maxima={1:150*NM, 2:200*NM,3:250*NM,4:300*NM,5:500*NM}
def reubicar(fila_aviones, deben_ser_reubicados):
    for i in deben_ser_reubicados:
        fila_aviones[i].set_velocidad(fila_aviones[i].get_velocidad() - 20*NM)
        if(debajo_minimo_de_franja(fila_aviones[i])):
            fila_aviones[i].set_velocidad(-200*NM)
            fila_aviones[i].en_retroceso = True
        else:
            fila_aviones[i].en_retroceso = False

        if not (i==0 or i==len(fila_aviones)-1):
            if((fila_aviones[i+1].get_tiempoAep()-fila_aviones[i].get_tiempoAep())>5 and fila_aviones[i].get_tiempoAep()-fila_aviones[i-1].get_tiempoAep()>5):
                fila_aviones[i].set_velocidad(franjas_y_vel_maxima[fila_aviones[i].get_franja()])
        
        elif i==len(fila_aviones)-1:
            if fila_aviones[i].get_tiempoAep()-fila_aviones[i-1].get_tiempoAep()>5:
                fila_aviones[i].set_velocidad(franjas_y_vel_maxima[fila_aviones[i].get_franja()])

        if(fila_aviones[i].get_distancia() > 100*NM):
            fila_aviones.pop(i)

# ----- Pygame visualization -----
WIDTH, HEIGHT = 1200, 420
MARGIN_L, MARGIN_R = 80, 40
TRACK_LEN = WIDTH - (MARGIN_L + MARGIN_R)

def x_from_dist_km(dist_km: float) -> int:
    frac = max(0.0, min(1.0, dist_km / (100*NM)))
    return int(MARGIN_L + frac * TRACK_LEN)

def color_por_dist(dist_km: float):
    if dist_km < 5*NM: return (70, 200, 70)
    elif dist_km < 15*NM: return (70, 130, 255)
    elif dist_km < 50*NM: return (255, 165, 0)
    elif dist_km < 100*NM: return (255, 80, 80)
    else: return (180,180,180)

def draw_marks(screen, font):
    pygame.draw.line(screen, (230,230,230), (MARGIN_L,60), (MARGIN_L,HEIGHT-60),4)
    screen.blit(font.render("AEP", True, (230,230,230)), (MARGIN_L-24,25))
    for mn, label in [(5,"5 mn"),(15,"15 mn"),(50,"50 mn"),(100,"100 mn")]:
        x = x_from_dist_km(mn*NM)
        pygame.draw.line(screen, (120,120,120), (x,80), (x,HEIGHT-80),1)
        screen.blit(font.render(label, True, (160,160,160)), (x-20, HEIGHT-30))

def draw_planes(screen, font, fila_aviones: List[Avion]):
    y0, dy = 110, 26
    for i,av in enumerate(fila_aviones):
        d = av.get_distancia()
        x = x_from_dist_km(d)
        y = y0 + i*dy
        col = (230,80,80) if av.en_retroceso else color_por_dist(d)
        pygame.draw.polygon(screen, col, [(x, y), (x+15, y-8), (x+15, y+8)])
        screen.blit(font.render(f"ID {av.id}", True, (255,255,0)), (x-15,y-20))

def format_time_hhmm(total_minutes: float) -> str:
    mins = int(total_minutes)
    mins_in_window = mins % (18*60)
    h = 6 + mins_in_window//60
    m = mins_in_window % 60
    return f"{h:02d}:{m:02d}"

def pygame_anim(sim_step_fn, get_fila_fn, fps=30, minutos_por_seg=2.0):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AEP – Visualización")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16)

    running = True
    acc_time = 0.0
    while running:
        dt_ms = clock.tick(fps)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        minutos_sim = (dt_ms/1000.0) * minutos_por_seg
        delta_h = minutos_sim / 60.0
        sim_step_fn(delta_h)
        acc_time += minutos_sim

        screen.fill((20,22,28))
        draw_marks(screen,font)
        draw_planes(screen,font,get_fila_fn())
        screen.blit(font.render(f"Hora simulada: {format_time_hhmm(acc_time)}", True, (255,255,255)), (WIDTH-220,20))
        pygame.display.flip()

    pygame.quit()

# ----- Simulation step -----
def demo():
    fila: List[Avion] = []
    contador_id = 1

    def sim_step(delta_h):
        nonlocal contador_id

        # possible new plane
        if random.random() < p * (delta_h*60):
            a = Avion(contador_id, 300*NM, 100*NM, 4, 0.0, None)
            fila.append(a)
            contador_id += 1
            fila.sort()

        llegados = []
        for av in fila:
            pasos = int(delta_h*60)
            for _ in range(pasos):
                av.actualizar()
                av.actualizar_velocidad()
            if av.get_distancia() <= 0:
                llegados.append(av)

        for av in llegados:
            fila.remove(av)

        _, deben_ser_reubicados = calcular_dist_entre_aviones(fila)
        reubicar(fila, deben_ser_reubicados)

    def get_fila(): return fila

    pygame_anim(sim_step, get_fila, fps=30, minutos_por_seg=6.0)

if __name__=="__main__":
    demo()
