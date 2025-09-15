import numpy as np
import json
import math
from math import comb

archivo= open("salidas_sim/run_p=0.016666666666666666_sim=100000.json")
data = json.load(archivo)
cant_detectados_por_hora = data["cant_detectados_por_hora"]


def horas_igual_que_x_promedio_por_sim(matriz: np.ndarray, x:int) -> float:
    """
    Cuenta cuántas celdas de la matriz son ==x y divide por la cantidad de simulaciones.
    matriz: shape (S, H) = (simulaciones, horas)
    """
    data = np.asarray(matriz)
    total_hits = int((data == x).sum())  # total de horas (en todas las sims) con valor == x
    # data.shape[0] = cantidad de simulaciones

    return total_hits /  (data.shape[0]*18)

res1=horas_igual_que_x_promedio_por_sim(cant_detectados_por_hora , 5)

def p_bin_5(p, n=60):
    return math.comb(n, 5) * (p**5) * ((1-p)**(n-5))

p = 1/60
res2=p_bin_5(p)

print("exacta:",res2, "nuestra:" ,res1)
