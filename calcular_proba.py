import numpy as np
import json
import math
from math import comb
from pathlib import Path
import re, json, math
import pandas as pd
import matplotlib.pyplot as plt
'''
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
'''
# analiza_runs.py
#
#
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
        A_f, D_f, M_f, C_f = A.ravel(), D.ravel(), M.ravel(), C.ravel()

        # Prob de ≥1 minuto con congestión en la hora
        cong_any = (C_f > 0).astype(int)
        cong_any = (C_f > 0).astype(int)

        print(f"\nλ={p}")
        print("Horas totales simuladas:", cong_any.size)
        print("Horas con ≥1 avión congestionado:", cong_any.sum())
        print("Proporción:", cong_any.sum() / cong_any.size)

        p_cong_any, se_cong_any, n_any = se_prop(cong_any.sum(), cong_any.size)

        # Tasas por detectado (aprox con agregados horarios)
        total_detect = D_f.sum()
        total_cong_min = C_f.sum()
        total_mvd = M_f.sum()
        p_cong_per_detect, se_cong_per_detect, n_cd = se_prop(total_cong_min, total_detect)
        p_mvd_per_detect, se_mvd_per_detect, n_md = se_prop(total_mvd, total_detect)

        rows.append(dict(
        lambda_=p,
        # ¿hubo ≥1 avión en congestión en la hora?
        prob_hubo_congestion_hora=p_cong_any, se_prob_cong=se_cong_any, n_prob=n_any,

        # Tasas por avión detectado
        prob_congestion_por_detectado=p_cong_per_detect, se_cong_por_detect=se_cong_per_detect, n_cd=n_cd,
        prob_mvd_por_detectado=p_mvd_per_detect, se_mvd_por_detect=se_mvd_per_detect, n_md=n_md,

        file=fp.name
))

    df = pd.DataFrame(rows).sort_values("lambda_").reset_index(drop=True)

    pd.options.display.float_format = lambda x: f"{x:,.4f}"
    cols_show = [
    "lambda_",
    # Prob. de que haya al menos 1 avión en congestión en la hora
    "prob_hubo_congestion_hora", "se_prob_cong",

    # % de aviones detectados que tuvieron congestión
    "prob_congestion_por_detectado", "se_cong_por_detect",

    # % de aviones detectados que se desviaron a MVD
    "prob_mvd_por_detectado", "se_mvd_por_detect",

    "file",
]
    print("\n=== RESUMEN POR λ (medias por hora ± error estándar) ===\n")
    print(df[cols_show])

    df.to_csv("resumen_lambda.csv", index=False)
    print("\nGuardé resumen en resumen_lambda.csv")

    # ---------- Gráficos ----------
    # 1) % de aviones con congestión vs λ (entre los detectados)
    plt.figure()
    plt.plot(df["lambda_"], 100*df["prob_congestion_por_detectado"], marker="o")
    plt.xlabel("λ (probabilidad de llegada por minuto)")
    plt.ylabel("% de aviones con congestión")
    plt.title("Aviones con congestión vs λ")
    plt.grid(True)
    plt.savefig("plots/plot_congestion_vs_lambda.png", bbox_inches="tight")

    # 1) Proba de que haya una congestion en cualquier hora
    plt.figure()
    plt.plot(df["lambda_"], df["prob_hubo_congestion_hora"], marker="o")
    plt.xlabel("λ (probabilidad de llegada por minuto)")
    plt.ylabel("Prob. de ≥1 avión en congestión en la hora")
    plt.title("Probabilidad de congestión horaria vs λ")
    plt.figtext(0.5, -0.05,
                "Probabilidad de que una hora cualquiera tenga al menos un avión congestionado",
                wrap=True, ha="center", fontsize=9)
    plt.grid(True)
    plt.savefig("plots/plot_prob_congestion_vs_lambda.png", bbox_inches="tight")


   # 3) % de aviones desviados a Montevideo vs λ
    plt.figure()
    plt.plot(df["lambda_"], 100*df["prob_mvd_por_detectado"], marker="o")
    plt.xlabel("λ (probabilidad de llegada por minuto)")
    plt.ylabel("% de aviones desviados a Montevideo")
    plt.title("Aviones desviados a Montevideo vs λ")
    plt.grid(True)
    plt.savefig("plots/plot_mvd_vs_lambda.png", bbox_inches="tight")

    print("\nExporté: plot_congestion_vs_lambda.png, plot_prob_congestion_vs_lambda.png, plot_mvd_vs_lambda.png")


if __name__ == "__main__":
    main()