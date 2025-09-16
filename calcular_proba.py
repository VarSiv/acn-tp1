import numpy as np
import json
import math
from math import comb
from pathlib import Path
import re, json, math
import pandas as pd
import matplotlib.pyplot as plt
''''''
archivo= open("salidas_sim/sim_anteriores/run_p=0.016666666666666666_sim=100000.json")
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

# analiza_runs.py
#
#
def se_mean(x):
    x = np.asarray(x).ravel() /60
    n = x.size
    mean = x.mean()
    se = x.std(ddof=1) / math.sqrt(n) if n > 1 else float("nan")
    return mean, se, n

def se_prop(k, n):
    if n <= 0:
        return float("nan"), float("nan"), 0
    p = k / n
    se = math.sqrt(p * (1 - p) / n)
    return p, se, n

def load_run(path: Path):
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    p = float(data["parametros"]["p"])
    A = np.asarray(data["cant_arribos_por_hora"])         # shape (S, H)
    D = np.asarray(data["cant_detectados_por_hora"])
    M = np.asarray(data["cant_aviones_a_montevideo"])
    C = np.asarray(data["cant_congestion_por_hora"])
    return p, A, D, M, C

def main():
    rows = [] 
    runs = [
        Path("salidas_sim/run_p=0.02_sim=100000.json"),
        Path("salidas_sim/run_p=0.1_sim=100000.json"),
        Path("salidas_sim/run_p=1_sim=100000.json"),
        Path("salidas_sim/run_p=0.2_sim=100000.json"),
        Path("salidas_sim/run_p=0.5_sim=100000.json")
    ]
    for fp in runs:
        p, A, D, M, C = load_run(fp)

        # Aplanamos por “hora de simulación” (S*H muestras)
        A_f = A.ravel()
        D_f = D.ravel()
        M_f = M.ravel()
        C_f = C.ravel()

        # Medias por hora y SE
        mean_arr, se_arr, n_arr = se_mean(A_f)
        mean_mvd, se_mvd, n_mvd = se_mean(M_f)
        mean_cong, se_cong, n_cong = se_mean(C_f)

        # Probabilidad de que en una hora haya ≥1 congestión
        cong_any = (C_f > 0).astype(int)
        p_cong_any, se_cong_any, n_any = se_prop(cong_any.sum(), cong_any.size)

        # Tasas por avión detectado (aproximación con agregados horarios)
        total_detect = D_f.sum()
        total_cong = C_f.sum()
        total_mvd = M_f.sum()

        # ¿Aumenta λ la frecuencia de congestiones? ¿Se ve gráficamente?
        p_cong_per_detect, se_cong_per_detect, n_cd = se_prop(total_cong, total_detect)
        
        p_mvd_per_detect, se_mvd_per_detect, n_md = se_prop(total_mvd, total_detect)    

        rows.append(dict(
            lambda_=p,
            mean_arribos_hora=mean_arr, se_arribos=se_arr, n_arr=n_arr,
            mean_desvios_mvd_hora=mean_mvd, se_desvios=se_mvd, n_mvd=n_mvd,
            mean_congestion_hora=mean_cong, se_congestion=se_cong, n_cong=n_cong,
            prob_hubo_congestion_hora=p_cong_any, se_prob_cong=se_cong_any, n_prob=n_any,
            prob_congestion_por_detectado=p_cong_per_detect, se_cong_por_detect=se_cong_per_detect, n_cd=n_cd,
            prob_mvd_por_detectado=p_mvd_per_detect, se_mvd_por_detect=se_mvd_per_detect, n_md=n_md,
            file=fp.name
        ))

    df = pd.DataFrame(rows).sort_values("lambda_").reset_index(drop=True)

    # Tabla resumen bonita
    pd.options.display.float_format = lambda x: f"{x:,.4f}"
    cols_show = [
        "lambda_",
        "mean_arribos_hora", "se_arribos",
        "mean_congestion_hora", "se_congestion",
        "prob_hubo_congestion_hora", "se_prob_cong",
        "mean_desvios_mvd_hora", "se_desvios",
        "prob_congestion_por_detectado", "se_cong_por_detect",
        "prob_mvd_por_detectado", "se_mvd_por_detect",
        "file",
    ]
    print("\n=== RESUMEN POR λ (medias por hora ± error estándar) ===\n")
    print(df[cols_show])

    # Guardar CSV
    df.to_csv("resumen_lambda.csv", index=False)
    print("\nGuardé resumen en resumen_lambda.csv")
    
    # --------- Gráficos simples ----------
    # 1) Congestión (eventos/hora) vs λ
    plt.figure()
    plt.plot(df["lambda_"], df["mean_congestion_hora"], marker="o")
    plt.xlabel("λ (prob. de llegada por minuto)")
    plt.ylabel("'%'de minutos con congestión")
    plt.title("Congestión vs λ")
    plt.grid(True)
    plt.savefig("plots/plot_congestion_vs_lambda.png", bbox_inches="tight")

    # 2) Probabilidad de que haya ≥1 congestión en la hora vs λ
    plt.figure()
    plt.plot(df["lambda_"], df["prob_hubo_congestion_hora"], marker="o")
    plt.xlabel("λ (prob. de llegada por minuto)")
    plt.ylabel("Pr(hubo ≥1 congestión en la hora)")
    plt.title("Probabilidad de congestión horaria vs λ")
    plt.grid(True)
    plt.savefig("plots/plot_prob_congestion_vs_lambda.png", bbox_inches="tight")

    # 3) Desvíos a Montevideo por hora vs λ
    plt.figure()
    plt.plot(df["lambda_"], df["mean_desvios_mvd_hora"], marker="o")
    plt.xlabel("λ (prob. de llegada por minuto)")
    plt.ylabel("Desvíos a Montevideo por hora (promedio)")
    plt.title("Desvíos a Montevideo vs λ")
    plt.grid(True)
    plt.savefig("plots/plot_mvd_vs_lambda.png", bbox_inches="tight")

    print("\nExporté gráficos: plot_congestion_vs_lambda.png, plot_prob_congestion_vs_lambda.png, plot_mvd_vs_lambda.png")

if __name__ == "__main__":
    main()
