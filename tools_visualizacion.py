import pygame
import random
from typing import List


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
    mins = int(total_minutes)
    # ciclo de 18h, arrancando a las 06:00
    mins_in_window = mins % (18*60)       # 0..1079
    h = 6 + mins_in_window // 60          # 6..23
    m = mins_in_window % 60
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
