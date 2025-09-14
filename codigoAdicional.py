'''
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
'''


#para printear
""" for avion in fila_aviones:
            print("Simulacion:",simulacion, " minuto:",m, " avion:",avion.id, " velocidad:",avion.get_velocidad())
        print("-"*20) """