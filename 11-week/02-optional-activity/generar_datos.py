"""Genera una serie diaria SIMULADA de producción (unidades/día) de una línea de envasado.

Datos ilustrativos creados solo para la actividad opcional de la Semana 11.
Componentes: tendencia creciente + estacionalidad anual + efecto día de la semana + ruido.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)  # semilla fija para reproducir el mismo CSV

fechas = pd.date_range("2023-01-01", "2025-12-31", freq="D")
t = np.arange(len(fechas))

# Tendencia: crecimiento lineal suave (aprox. +9 % anual)
tendencia = 1000 * (1 + 0.09 * t / 365)

# Estacionalidad anual (factor multiplicativo por mes)
factor_mes = {1: 0.88, 2: 0.90, 3: 0.97, 4: 0.98, 5: 1.00, 6: 1.03,
              7: 1.05, 8: 1.00, 9: 0.99, 10: 1.06, 11: 1.14, 12: 1.20}
estacional = np.array([factor_mes[m] for m in fechas.month])

# Efecto día de la semana (domingo con producción reducida)
factor_dia = np.where(fechas.dayofweek == 6, 0.35, 1.0)

ruido = rng.normal(1.0, 0.04, len(fechas))

unidades = (tendencia * estacional * factor_dia * ruido).round().astype(int)

df = pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"), "unidades": unidades})
df.to_csv("produccion_diaria.csv", index=False)
print(df.head(), f"\nFilas: {len(df)}")
