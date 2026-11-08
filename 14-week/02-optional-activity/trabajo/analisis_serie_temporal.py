"""
Actividad calificable - Corte 3: Análisis temporal y visualización
Ciencia de Datos (CORHUILA) - Isabella Ramos Betancourt

Caso: Gestión del riego agroindustrial basada en datos.

Qué hace este script:
  1. Genera una serie diaria SIMULADA de consumo de agua de riego (m3/día)
     y la guarda en consumo_riego_diario.csv.
  2. Carga el CSV con la fecha como índice, agrega por mes (resample) y calcula
     una media móvil de 3 meses (rolling).
  3. Cuantifica tendencia (regresión lineal) y estacionalidad (índice estacional).
  4. Construye dos gráficos: evolución (grafico_evolucion.png) y comparación
     (grafico_comparacion.png).

DATOS ILUSTRATIVOS (simulados): no corresponden a registros de una finca real.
Ejecutar:  python analisis_serie_temporal.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
TEXTO, GRIS, NARANJA = "#222222", "#b8bcc2", "#e8710a"

# ----------------------------------------------------------------------------
# 1. Serie diaria simulada (2024-01-01 a 2026-10-31)
# ----------------------------------------------------------------------------
rng = np.random.default_rng(42)
dias = pd.date_range("2024-01-01", "2026-10-31", freq="D")

# Régimen bimodal de lluvias (tipo Huila): meses secos -> más riego.
factor_mes = {1: 1.15, 2: 1.15, 3: 0.85, 4: 0.70, 5: 0.75, 6: 1.05,
              7: 1.30, 8: 1.35, 9: 1.25, 10: 0.90, 11: 0.80, 12: 1.10}
estacional = dias.month.map(factor_mes).to_numpy()
tendencia = 28 + 0.37 * (np.arange(len(dias)) / 30.4)   # crecimiento ~ +0.37 m3/día por mes
ruido = rng.normal(0, 2.2, len(dias))
consumo = np.clip(tendencia * estacional + ruido, 3, None).round(2)

pd.DataFrame({"fecha": dias.strftime("%Y-%m-%d"), "volumen_agua_m3": consumo}) \
    .to_csv(AQUI / "consumo_riego_diario.csv", index=False)

# ----------------------------------------------------------------------------
# 2. Carga con la fecha como índice, resample mensual y media móvil
# ----------------------------------------------------------------------------
df = pd.read_csv(AQUI / "consumo_riego_diario.csv", parse_dates=["fecha"]).set_index("fecha")

mensual = df["volumen_agua_m3"].resample("ME").sum().to_frame("total_m3")
mensual["dias"] = mensual.index.days_in_month
mensual["m3_por_dia"] = mensual["total_m3"] / mensual["dias"]
mensual["media_movil_3m"] = mensual["m3_por_dia"].rolling(3).mean()

print("Filas diarias:", len(df), "| meses agregados:", len(mensual))
print(mensual.round(2).head(6))

# ----------------------------------------------------------------------------
# 3. Tendencia y estacionalidad
# ----------------------------------------------------------------------------
x = np.arange(len(mensual))
pend, interc = np.polyfit(x, mensual["m3_por_dia"], 1)
mensual["tendencia"] = interc + pend * x
crec_total = pend * (len(mensual) - 1) / mensual["tendencia"].iloc[0] * 100

mensual["indice"] = mensual["m3_por_dia"] / mensual["tendencia"] * 100
indice_mes = mensual.groupby(mensual.index.month)["indice"].mean()
nombres = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

print(f"\nPendiente: {pend:.3f} m3/día por mes | crecimiento de la tendencia: {crec_total:.1f} %")
print("Índice estacional (100 = nivel de tendencia):")
print(indice_mes.round(1).to_string())

top = indice_mes.sort_values(ascending=False)
bajo = indice_mes.sort_values()
print("\nMeses más altos:", [nombres[m - 1] for m in top.index[:3]])
print("Meses más bajos:", [nombres[m - 1] for m in bajo.index[:3]])

# ----------------------------------------------------------------------------
# 4. Gráfico 1 - EVOLUCIÓN (línea): mensual + media móvil + tendencia
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=150)
ax.plot(mensual.index, mensual["m3_por_dia"], color=GRIS, lw=1.8, marker="o",
        ms=3.5, label="Promedio diario del mes", zorder=2)
ax.plot(mensual.index, mensual["media_movil_3m"], color=NARANJA, lw=2.8,
        label="Media móvil de 3 meses", zorder=3)
ax.plot(mensual.index, mensual["tendencia"], color="#555555", lw=1.4, ls="--",
        label=f"Tendencia lineal (+{crec_total:.0f} % en el periodo)", zorder=1)
ax.set_ylim(0, mensual["m3_por_dia"].max() * 1.15)      # escala honesta: desde 0
ax.set_ylabel("Consumo de agua (m³ por día)", fontsize=10, color="#555555")
ax.yaxis.grid(True, color="#e6e6e6", lw=0.8)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#999999")
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.tick_params(colors="#555555")
ax.legend(frameon=False, fontsize=9.5, loc="lower right", ncol=1)
fig.text(0.02, 0.96,
         f"El consumo de riego crece ~{crec_total:.0f} % en 34 meses y se repite un patrón "
         "de dos picos al año",
         fontsize=14.5, fontweight="bold", color=TEXTO, ha="left", va="top")
fig.text(0.02, 0.905,
         "Consumo diario promedio de agua de riego por mes, ene 2024 – oct 2026. Datos ilustrativos (simulados).",
         fontsize=10, color="#555555", ha="left", va="top")
fig.subplots_adjust(left=0.08, right=0.97, top=0.83, bottom=0.10)
fig.savefig(AQUI / "grafico_evolucion.png", facecolor="white")
plt.close(fig)

# ----------------------------------------------------------------------------
# 5. Gráfico 2 - COMPARACIÓN (barras): índice estacional por mes del año
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=150)
top3 = set(top.index[:3])
cols = [NARANJA if m in top3 else GRIS for m in indice_mes.index]
ax.bar(range(12), indice_mes.values, color=cols, width=0.68, zorder=3)
ax.axhline(100, color="#555555", ls="--", lw=1.3, zorder=4)
ax.set_xlim(-0.6, 13.6)
ax.text(11.6, 101.5, "Nivel típico (100)", fontsize=9, color="#555555", ha="left")
ax.set_xticks(range(12))
ax.set_xticklabels(nombres, fontsize=10.5, color=TEXTO)
ax.set_ylim(0, max(indice_mes.max() * 1.15, 140))        # barras desde 0
for i, v in enumerate(indice_mes.values):
    ax.text(i, v + 2, f"{v:.0f}", ha="center", fontsize=9.5, color=TEXTO,
            fontweight="bold" if (i + 1) in top3 else "normal")
ax.set_ylabel("Índice estacional (100 = nivel de tendencia)", fontsize=10, color="#555555")
ax.yaxis.grid(True, color="#e6e6e6", lw=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#999999")
ax.tick_params(axis="y", colors="#555555")
ax.tick_params(axis="x", length=0)
m1, m2, m3 = [nombres[m - 1] for m in sorted(top3)]
fig.text(0.02, 0.96,
         f"El riego se dispara en {m1}, {m2} y {m3}: hasta "
         f"{indice_mes.max() - 100:.0f} % sobre lo normal, y cae ~{100 - indice_mes.min():.0f} % en el mes más lluvioso",
         fontsize=14, fontweight="bold", color=TEXTO, ha="left", va="top")
fig.text(0.02, 0.905,
         "Consumo diario de riego frente a la tendencia, promedio por mes del año (2024–2026). Datos ilustrativos (simulados).",
         fontsize=10, color="#555555", ha="left", va="top")
fig.subplots_adjust(left=0.09, right=0.97, top=0.83, bottom=0.09)
fig.savefig(AQUI / "grafico_comparacion.png", facecolor="white")
plt.close(fig)

mensual.round(3).to_csv(AQUI / "consumo_riego_mensual.csv", index_label="mes")
print("\nGráficos y CSV generados.")
