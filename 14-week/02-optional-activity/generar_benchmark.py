"""
Actividad opcional - Semana 14: Optimiza una consulta (opción A: SQL)
Ciencia de Datos (CORHUILA) - Isabella Ramos Betancourt

Caso: Gestión del Riego Agroindustrial. Tabla lectura_sensor del modelo ERD
(id_lectura, id_lote, fecha_hora, humedad_suelo_pct, temperatura_c).

DATOS SIMULADOS: se generan 600 000 lecturas (una por minuto-lote, durante
una por lote cada 5 minutos, de dic. 2024 a oct. 2026) solo para poder medir la diferencia de tiempos.
No son registros reales. Se usa SQLite (módulo estándar de Python).

El script:
  1. Crea la base y la puebla (sin índice).
  2. Ejecuta la consulta LENTA  (SELECT * + función en el WHERE).
  3. Ejecuta la consulta RÁPIDA (columnas necesarias + rango de fechas).
  4. Crea el índice y vuelve a ejecutar la consulta rápida.
  5. Verifica que ambas consultas dan el mismo resultado.
  6. Guarda resultados.json y comparacion_tiempos.png.
"""
import json
import random
import sqlite3
import statistics
import time
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(42)
N_FILAS = 600_000
LOTES = ["LOT-001", "LOT-002", "LOT-003"]
REPETICIONES = 7

# ------------------------------------------------------------ 1. Base de datos
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("""
CREATE TABLE lectura_sensor (
    id_lectura        INTEGER PRIMARY KEY,
    id_lote           TEXT NOT NULL,
    fecha_hora        TEXT NOT NULL,      -- 'YYYY-MM-DD HH:MM:SS'
    humedad_suelo_pct REAL,
    temperatura_c     REAL
)""")

inicio = datetime(2024, 12, 1)   # con paso de 5 min termina a fines de oct. 2026
filas = []
for i in range(N_FILAS):
    t = inicio + timedelta(minutes=5 * (i // len(LOTES)))
    lote = LOTES[i % len(LOTES)]
    filas.append((i + 1, lote, t.strftime("%Y-%m-%d %H:%M:%S"),
                  round(random.uniform(28, 56), 1),
                  round(random.uniform(19, 27), 1)))
cur.executemany("INSERT INTO lectura_sensor VALUES (?,?,?,?,?)", filas)
conn.commit()
fecha_min, fecha_max = cur.execute(
    "SELECT MIN(fecha_hora), MAX(fecha_hora) FROM lectura_sensor").fetchone()

# ------------------------------------------------------------ 2. Consultas
# Pregunta: humedad promedio por lote durante septiembre de 2026.
SQL_LENTA = """
SELECT *
FROM lectura_sensor
WHERE strftime('%Y-%m', fecha_hora) = '2026-09'
"""
SQL_RAPIDA = """
SELECT id_lote, humedad_suelo_pct
FROM lectura_sensor
WHERE fecha_hora >= '2026-09-01' AND fecha_hora < '2026-10-01'
"""


def medir(sql):
    """Mediana de REPETICIONES ejecuciones (ms) y filas devueltas."""
    tiempos, filas_dev = [], 0
    for _ in range(REPETICIONES):
        t0 = time.perf_counter()
        res = conn.execute(sql).fetchall()
        tiempos.append((time.perf_counter() - t0) * 1000)
        filas_dev = len(res)
    return statistics.median(tiempos), filas_dev


def promedio_por_lote(sql):
    """Resultado de negocio (humedad promedio por lote) calculado en Python."""
    acum = {}
    for fila in conn.execute(sql).fetchall():
        if len(fila) == 5:                  # SELECT *: lote, humedad en pos. 1 y 3
            lote, hum = fila[1], fila[3]
        else:
            lote, hum = fila
        acum.setdefault(lote, []).append(hum)
    return {k: round(sum(v) / len(v), 3) for k, v in sorted(acum.items())}


def plan(sql):
    return [r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + sql).fetchall()]


res = {"filas_tabla": N_FILAS, "rango_datos": [fecha_min, fecha_max],
       "repeticiones": REPETICIONES}

# a) Lenta (sin índice)
t, n = medir(SQL_LENTA)
res["lenta"] = {"ms": round(t, 1), "filas": n, "plan": plan(SQL_LENTA)}
# b) Rápida, todavía sin índice (efecto de columnas + rango)
t, n = medir(SQL_RAPIDA)
res["rapida_sin_indice"] = {"ms": round(t, 1), "filas": n, "plan": plan(SQL_RAPIDA)}
# c) Rápida con índice
cur.execute("CREATE INDEX idx_lectura_fecha ON lectura_sensor(fecha_hora)")
conn.commit()
t, n = medir(SQL_RAPIDA)
res["rapida_con_indice"] = {"ms": round(t, 1), "filas": n, "plan": plan(SQL_RAPIDA)}

# d) Misma respuesta
r_lenta, r_rapida = promedio_por_lote(SQL_LENTA), promedio_por_lote(SQL_RAPIDA)
res["resultado_lenta"], res["resultado_rapida"] = r_lenta, r_rapida
res["mismo_resultado"] = r_lenta == r_rapida
assert res["mismo_resultado"], "Las consultas no devuelven el mismo resultado"
assert res["lenta"]["filas"] == res["rapida_con_indice"]["filas"]

res["mejora_total_x"] = round(res["lenta"]["ms"] / res["rapida_con_indice"]["ms"], 1)
res["mejora_indice_x"] = round(
    res["rapida_sin_indice"]["ms"] / res["rapida_con_indice"]["ms"], 1)
res["mejora_sin_indice_x"] = round(
    res["lenta"]["ms"] / res["rapida_sin_indice"]["ms"], 1)

with open("resultados.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

# ------------------------------------------------------------ 3. Gráfico
GRIS, NARANJA, TEXTO = "#b8bcc2", "#e8710a", "#222222"
etiquetas = ["1. Lenta\n(SELECT * + función\nen el WHERE)",
             "2. Columnas + rango\n(sin índice)",
             "3. Columnas + rango\n+ índice en fecha_hora"]
valores = [res["lenta"]["ms"], res["rapida_sin_indice"]["ms"],
           res["rapida_con_indice"]["ms"]]
fig, ax = plt.subplots(figsize=(10, 5.8), dpi=150)
ax.bar(etiquetas, valores, color=[GRIS, GRIS, NARANJA], width=0.55, zorder=3)
ax.set_ylim(0, max(valores) * 1.18)
for i, v in enumerate(valores):
    ax.text(i, v + max(valores) * 0.02, f"{v:,.1f} ms", ha="center",
            fontsize=12, fontweight="bold" if i == 2 else "normal", color=TEXTO)
ax.set_ylabel("Tiempo de ejecución (ms, mediana de 7 corridas)", fontsize=10,
              color="#555555")
ax.yaxis.grid(True, color="#e6e6e6", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="x", labelsize=10)
fig.text(0.02, 0.96,
         f"La consulta optimizada responde unas {res['mejora_total_x']:.0f} veces más rápido",
         fontsize=15, fontweight="bold", color=TEXTO, ha="left", va="top")
fig.text(0.02, 0.905,
         f"Humedad del suelo de septiembre de 2026 sobre {N_FILAS:,} lecturas "
         "simuladas. Mismo resultado en las tres versiones.",
         fontsize=10.5, color="#555555", ha="left", va="top")
fig.subplots_adjust(left=0.09, right=0.97, top=0.84, bottom=0.18)
fig.savefig("comparacion_tiempos.png", facecolor="white")

print(json.dumps(res, ensure_ascii=False, indent=2))
