"""
Actividad calificable - Corte 3: Optimización de una consulta SQL
Ciencia de Datos (CORHUILA) - Isabella Ramos Betancourt

Mide la consulta ANTES (lenta) y DESPUÉS (optimizada) sobre una tabla
registro_riego con datos SIMULADOS, usando SQLite en memoria.

Pregunta de negocio: ¿cuánta agua se aplicó en el lote LOT-001 durante 2026?

Nota: en MySQL/SQL Server la versión lenta usa YEAR(fecha) = 2026; SQLite no
tiene YEAR(), su equivalente es strftime('%Y', fecha) = '2026'. El efecto es
el mismo: una función aplicada a la columna impide usar el índice.
Ejecutar:  python optimizar_consulta.py
"""
import sqlite3
import statistics
import time

import numpy as np
import pandas as pd

N = 400_000
rng = np.random.default_rng(7)
fechas = pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 1035, N), unit="D")

conn = sqlite3.connect(":memory:")
conn.execute("""
CREATE TABLE registro_riego (
    id_riego INTEGER PRIMARY KEY,
    id_lote TEXT, id_tecnico TEXT, fecha TEXT,
    volumen_agua_m3 REAL, duracion_min INTEGER, observaciones TEXT)""")
filas = zip(
    range(1, N + 1),
    rng.choice(["LOT-001", "LOT-002", "LOT-003"], N),
    rng.choice(["TEC-01", "TEC-02"], N),
    fechas.strftime("%Y-%m-%d"),
    rng.uniform(1, 6, N).round(2),
    rng.integers(20, 70, N),
    ["Riego programado según bitácora de campo del turno"] * N,
)
conn.executemany("INSERT INTO registro_riego VALUES (?,?,?,?,?,?,?)", filas)
conn.commit()

ANTES = """SELECT * FROM registro_riego
WHERE strftime('%Y', fecha) = '2026' AND id_lote = 'LOT-001'"""
DESPUES = """SELECT fecha, volumen_agua_m3 FROM registro_riego
WHERE id_lote = 'LOT-001' AND fecha >= '2026-01-01' AND fecha < '2027-01-01'"""


def medir(sql, repeticiones=7):
    tiempos = []
    for _ in range(repeticiones):
        t = time.perf_counter()
        filas = conn.execute(sql).fetchall()
        tiempos.append((time.perf_counter() - t) * 1000)
    return statistics.median(tiempos), filas


def plan(sql):
    return [r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + sql)]


t_antes, f_antes = medir(ANTES)
print("ANTES  plan:", plan(ANTES))
print(f"ANTES  filas={len(f_antes)}  columnas={len(f_antes[0])}  mediana={t_antes:.1f} ms")

# Índice compuesto y cubriente: lote (igualdad) + fecha (rango) + volumen
conn.execute("CREATE INDEX idx_riego_lote_fecha ON registro_riego (id_lote, fecha, volumen_agua_m3)")
conn.commit()

t_despues, f_despues = medir(DESPUES)
print("DESPUÉS plan:", plan(DESPUES))
print(f"DESPUÉS filas={len(f_despues)}  columnas={len(f_despues[0])}  mediana={t_despues:.1f} ms")

suma_antes = sum(r[4] for r in f_antes)
suma_despues = sum(r[1] for r in f_despues)
print(f"\nSuma m3 antes={suma_antes:.2f} | después={suma_despues:.2f} | iguales={abs(suma_antes - suma_despues) < 1e-6}")
print(f"Mejora: {t_antes / t_despues:.1f}x más rápida ({(1 - t_despues / t_antes) * 100:.0f} % menos tiempo)")
