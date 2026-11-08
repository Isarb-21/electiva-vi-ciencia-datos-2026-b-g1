"""Actividad opcional – Semana 11: análisis de una serie de tiempo.

1) Carga la serie diaria con la fecha como índice.
2) La agrega por mes (resample) y calcula medias móviles (rolling).
3) Grafica la serie mensual con sus medias móviles y resume tendencia y estacionalidad.
"""
import pandas as pd
import matplotlib
import matplotlib.dates as mdates

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1. Carga: la fecha se interpreta como fecha (no como texto) y pasa a ser el índice
df = pd.read_csv("produccion_diaria.csv", parse_dates=["fecha"]).set_index("fecha")
print(df.dtypes, df.index.min(), df.index.max(), sep="\n")

# 2. Agregación mensual ("MS" = cada mes queda rotulado con su primer día)
mensual = df["unidades"].resample("MS").sum()

# Medias móviles sobre la serie mensual
movil3 = mensual.rolling(3).mean()    # suaviza el ruido (trimestre móvil)
movil12 = mensual.rolling(12).mean()  # elimina la estacionalidad anual -> deja la tendencia

# 3. Apoyo numérico para la interpretación
anual = mensual.groupby(mensual.index.year).sum()
print("\nProducción anual:\n", anual)
print("Crecimiento anual (%):\n", (anual.pct_change() * 100).round(1))

# Índice estacional: promedio de cada mes / promedio mensual de toda la serie
indice = (mensual.groupby(mensual.index.month).mean() / mensual.mean()).round(2)
print("\nÍndice estacional por mes:\n", indice)
print("\nMedia móvil 12 meses (primer y último valor):",
      round(movil12.dropna().iloc[0]), round(movil12.dropna().iloc[-1]))

# Gráfico
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(mensual.index, mensual / 1000, color="#B0B7BF", lw=1.6, marker="o", ms=3.5,
        label="Producción mensual")
ax.plot(movil3.index, movil3 / 1000, color="#E8710A", lw=2.2, label="Media móvil 3 meses")
ax.plot(movil12.index, movil12 / 1000, color="#1F3A5F", lw=2.6, label="Media móvil 12 meses")
ax.set_title("La producción crece 7–9 % por año y alcanza su pico cada diciembre",
             loc="left", fontsize=13, fontweight="bold", pad=24)
ax.text(0, 1.015, "Producción mensual simulada de una línea de envasado, 2023–2025 (miles de unidades)",
        transform=ax.transAxes, fontsize=9.5, color="#555555")
ax.set_ylabel("Miles de unidades por mes")
ax.set_xlabel("Mes")
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.grid(axis="y", color="#E5E5E5")
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig("grafico_serie.png", dpi=200)
print("\nGráfico guardado: grafico_serie.png")
