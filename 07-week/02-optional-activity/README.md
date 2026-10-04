# Actividad Práctica · Semana 7
## Herramientas y lenguajes (SQL, NoSQL, Python)
### 🌱 Caso: Gestión del Riego Agroindustrial basada en Datos

```yaml
# CONFIG
FULL_NAME: Isabella Ramos Betancourt
GITHUB_USER: Isarb-21
```

**Isabella Ramos Betancourt**  
Facultad de Ingeniería, Corporación Universitaria del Huila (CORHUILA)  
Ciencia de Datos (Cód. 69109) [Pénsum 40D, Grupo 1]  
Jesús Ariel Gonzáles Bonilla  
Octubre de 2026  

---

## 1. Introducción

Con el modelo entidad-relación diseñado en la Semana 6, el siguiente paso natural es consultar y manipular los datos almacenados en la base de datos relacional del sistema de riego. Como establece Silberschatz et al. (2020), SQL es el lenguaje estándar para interactuar con bases de datos relacionales y permite filtrar, combinar y agregar información con pocas cláusulas bien estructuradas.

En el contexto del proyecto de **Gestión del Riego Agroindustrial**, las tablas `Lote`, `Tecnico`, `Registro_Riego` y `Lectura_Sensor` contienen la información necesaria para responder a la pregunta de investigación planteada en el Corte 1:

> *«¿Cómo se pueden utilizar los datos de humedad del suelo, temperatura y consumo de agua para mejorar la programación del riego y optimizar el rendimiento de los cultivos?»*

El propósito de esta actividad es escribir **3 consultas SQL** que respondan preguntas operativas concretas del proyecto (una con filtro, una con JOIN y una con GROUP BY), y replicar una de ellas utilizando la librería **pandas** de Python, demostrando cómo ambas herramientas permiten analizar los mismos datos según la tarea y el entorno disponibles (IBM, 2024).

---

## 2. Desarrollo de la actividad

### 2.1. Contexto del Modelo de Datos

Las consultas se desarrollan sobre el esquema definido en la Semana 6:

```text
Lote          (id_lote PK, nombre, area_ha, tipo_suelo, cultivo, rendimiento_ton)
Tecnico       (id_tecnico PK, nombre, especialidad, telefono)
Registro_Riego (id_riego PK, id_lote FK, id_tecnico FK, fecha, volumen_agua_m3, duracion_min)
Lectura_Sensor (id_lectura PK, id_lote FK, fecha_hora, humedad_suelo_pct, temperatura_c)
```

---

### 2.2. Consulta 1: Filtro con WHERE

**Pregunta operativa:** ¿En qué fechas se aplicó más de 3 m³ de agua en el Lote Norte?

Esta consulta permite identificar los eventos de riego con mayor consumo hídrico en una parcela específica, útil para detectar posibles excesos de irrigación (FAO, 2026).

```sql
-- Consulta 1: Filtrar eventos de riego con volumen mayor a 3 m³ en el Lote Norte
SELECT fecha, volumen_agua_m3, duracion_min
FROM registro_riego
WHERE id_lote = 'LOT-001'
  AND volumen_agua_m3 > 3.0
ORDER BY fecha;
```

**Interpretación del resultado:**  
Devuelve únicamente los eventos donde se superaron los 3 m³ de agua aplicados en el lote identificado como `LOT-001`. La cláusula `WHERE` filtra filas que cumplen ambas condiciones simultáneamente, y `ORDER BY fecha` presenta los resultados en orden cronológico para facilitar la lectura del historial.

---

### 2.3. Consulta 2: JOIN (Cruzar dos tablas)

**Pregunta operativa:** ¿Qué técnico ejecutó cada riego y cuánta agua aplicó?

Para auditar la operación y relacionar la responsabilidad del personal con el consumo de agua, es necesario cruzar la tabla `Registro_Riego` con la tabla `Tecnico` mediante un JOIN sobre la clave foránea `id_tecnico` (Silberschatz et al., 2020).

```sql
-- Consulta 2: Cruzar registros de riego con el nombre del técnico responsable
SELECT t.nombre      AS tecnico,
       r.fecha,
       r.id_lote,
       r.volumen_agua_m3
FROM registro_riego r
JOIN tecnico t ON r.id_tecnico = t.id_tecnico
ORDER BY r.fecha;
```

**Interpretación del resultado:**  
El `JOIN` combina cada fila de `Registro_Riego` con la fila correspondiente de `Tecnico` usando la clave foránea. El resultado muestra en una sola fila el nombre legible del técnico junto con la fecha, el lote y el volumen de agua aplicado, eliminando la necesidad de buscar manualmente el nombre por su código.

---

### 2.4. Consulta 3: GROUP BY (Agregar por grupo)

**Pregunta operativa:** ¿Cuánta agua total consumió cada lote y cuál fue su rendimiento de cosecha?

Esta consulta es la más relevante para responder a la pregunta del proyecto, pues permite comparar el consumo acumulado de agua de cada parcela con su producción final en toneladas (FAO, 2026).

```sql
-- Consulta 3: Total de agua consumida y rendimiento por lote
SELECT l.nombre                  AS lote,
       l.cultivo,
       l.rendimiento_ton,
       SUM(r.volumen_agua_m3)    AS agua_total_m3,
       COUNT(r.id_riego)         AS num_riegos,
       ROUND(l.rendimiento_ton / NULLIF(SUM(r.volumen_agua_m3), 0), 3)
                                 AS eficiencia_ton_m3
FROM lote l
JOIN registro_riego r ON l.id_lote = r.id_lote
GROUP BY l.id_lote, l.nombre, l.cultivo, l.rendimiento_ton
ORDER BY eficiencia_ton_m3 DESC;
```

**Interpretación del resultado:**  
`GROUP BY` agrupa todos los riegos de cada lote en una sola fila. `SUM` acumula el agua total aplicada; `COUNT` informa cuántos eventos de riego ocurrieron; y la columna calculada `eficiencia_ton_m3` muestra cuántas toneladas produjo cada lote por metro cúbico de agua utilizado. Esta métrica es equivalente al indicador de eficiencia hídrica de la FAO (2026) y permite comparar directamente el desempeño entre parcelas.

---

### 2.5. Réplica de la Consulta 3 en Python con pandas

Como señala IBM (2024), pandas es la librería de Python para análisis de datos tabulares. Permite cargar archivos CSV o conectarse a una base de datos y replicar operaciones equivalentes a las de SQL con pocas líneas de código. A continuación se replica la Consulta 3 (GROUP BY + JOIN) sobre archivos CSV del proyecto:

```python
import pandas as pd

# --- Carga de los archivos CSV del caso ---
lote = pd.read_csv("lote.csv")
# Columnas esperadas: id_lote, nombre, area_ha, tipo_suelo, cultivo, rendimiento_ton

registro_riego = pd.read_csv("registro_riego.csv")
# Columnas esperadas: id_riego, id_lote, id_tecnico, fecha, volumen_agua_m3, duracion_min

# --- JOIN: combinar lote con los registros de riego (equivalente al JOIN en SQL) ---
df = pd.merge(registro_riego, lote, on="id_lote", how="left")

# --- GROUP BY + SUM: calcular el agua total y número de riegos por lote ---
resumen = (
    df.groupby(["id_lote", "nombre", "cultivo", "rendimiento_ton"])
    .agg(
        agua_total_m3=("volumen_agua_m3", "sum"),
        num_riegos=("id_riego", "count")
    )
    .reset_index()
)

# --- Calcular la eficiencia hídrica (ton por m³) ---
resumen["eficiencia_ton_m3"] = (
    resumen["rendimiento_ton"] / resumen["agua_total_m3"]
).round(3)

# --- Ordenar de mayor a menor eficiencia ---
resumen = resumen.sort_values("eficiencia_ton_m3", ascending=False)

print(resumen)
```

**Comparación SQL vs. pandas:**

| Operación | SQL | pandas |
|---|---|---|
| Cargar datos | `FROM tabla` | `pd.read_csv()` |
| Unir tablas | `JOIN … ON` | `pd.merge(…, on=)` |
| Agrupar | `GROUP BY` | `.groupby()` |
| Agregar | `SUM()`, `COUNT()` | `.agg(sum, count)` |
| Ordenar | `ORDER BY` | `.sort_values()` |

Ambas herramientas producen el mismo resultado. SQL es preferible cuando los datos están en una base de datos y el volumen es grande; pandas es útil para exploración interactiva, transformaciones complejas y visualización (IBM, 2024).

---

## 3. Conclusión

Las tres consultas desarrolladas permiten avanzar de forma progresiva en el análisis del riego agroindustrial: la primera identifica eventos de consumo elevado mediante filtrado simple; la segunda vincula operarios y riegos mediante un JOIN que aprovecha la integridad referencial diseñada en el ERD; la tercera agrega el consumo total por lote y calcula una métrica de eficiencia hídrica que conecta directamente el gasto de agua con el rendimiento del cultivo.

La réplica en pandas demuestra que SQL y Python no son herramientas excluyentes, sino complementarias: SQL filtra y agrega en la base de datos; pandas permite explorar, transformar y visualizar los resultados del análisis. Esta combinación constituye la base metodológica para las etapas de limpieza y visualización que se abordan en las semanas siguientes.

---

## 4. Referencias

* Food and Agriculture Organization of the United Nations (FAO). (2026). *Water data and resource assessment*. https://www.fao.org/land-water/water/water-data-and-resource-assessment
* IBM. (2024). *What is a Relational Database?* IBM Think. https://www.ibm.com/think/topics/relational-database
* McKinney, W. (2022). *Python for Data Analysis* (3rd ed.). O'Reilly Media.
* Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). *Database System Concepts* (7th ed.). McGraw-Hill Education.
