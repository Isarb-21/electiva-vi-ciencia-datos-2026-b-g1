# Actividad Práctica · Semana 8
## Conexión de datos: APIs, ETL y pipelines
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

En el proyecto de Ciencia de Datos, los datos raramente viven en un solo lugar ni llegan ya listos para analizar. Como establece la clase de la Semana 8, los datos de un sistema productivo provienen de múltiples fuentes (sensores IoT, archivos históricos, APIs climáticas externas) y deben pasar por un proceso de **ETL** (*Extraer, Transformar, Cargar*) antes de poder ser consultados y visualizados (Kleppmann, 2017).

En el contexto del caso de **Gestión del Riego Agroindustrial**, identificado en el Corte 1, existen tres tipos de fuentes diferenciadas:
1. **Sensores IoT** que generan lecturas continuas de humedad del suelo y temperatura.
2. **Archivos CSV e historial operativo** de los registros de riego y cosechas por lote.
3. **APIs externas** que entregan datos de pronóstico meteorológico y lluvia acumulada.

El propósito de esta actividad es diseñar el **diagrama de pipeline ETL** para el caso, identificando cada etapa (*Extraer*, *Transformar*, *Cargar*) con sus herramientas, justificando qué partes del proceso se realizan mediante streaming y cuáles en batch, y demostrando la conexión en Python para el consumo de una API meteorológica mediante `requests`.

---

## 2. Desarrollo de la actividad

### 2.1. Diagrama del Pipeline ETL

El pipeline sigue la secuencia: **Fuentes → Extraer → Transformar → Cargar → BI / Decisión**.

#### Representación en texto (Formato de clase):

```text
FUENTES
  ├── Sensores IoT (Humedad, Temperatura) → Kafka (streaming en tiempo real)
  ├── API Meteorológica (Lluvia, Pronóstico) → requests.get() en Python (pull diario)
  └── Archivos CSV (Bitácoras de riego, Cosechas) → pd.read_csv() (por lotes mensual/semanal)
         │
         ▼
   [EXTRAER]
   Kafka consume las lecturas de los sensores a medida que llegan.
   Python extrae el JSON de la API con requests y los CSV con pandas.
         │
         ▼
   [TRANSFORMAR]
   Python / pandas:
     - Convertir unidades y tipos (texto → número, texto → fecha)
     - Estandarizar nombres de lotes ("LOT 01" → "LOT-001")
     - Completar faltantes (fillna con último valor conocido del sensor)
     - Calcular métricas: eficiencia hídrica = rendimiento_ton / agua_total_m3
     - Unir (merge) datos de sensores con registros de riego por id_lote y fecha
         │
         ▼
   [CARGAR]
   Base de datos relacional (PostgreSQL / SQLite):
     - Tablas: Lote, Tecnico, Registro_Riego, Lectura_Sensor
   (Orquestado por n8n: coordina la ejecución automatizada de las tareas batch)
         │
         ▼
   [BI / DECISIÓN]
   Power BI conectado a la base de datos:
     - Tablero de humedad promedio por lote
     - Consumo de agua acumulado por ciclo
     - Alerta cuando humedad < 30% (señal de riego urgente)
```

---

### 2.2. Justificación de procesamiento batch y streaming

De acuerdo a las necesidades operativas de la Gestión del Riego, el pipeline combina dos modalidades de procesamiento de datos:

**1. Procesamiento Streaming (Tiempo real / Continuo):**
* **Componente:** Sensores IoT (Humedad y Temperatura) a través de Kafka.
* **Justificación:** El estado del suelo puede cambiar rápidamente en condiciones de sol intenso. Para evitar estrés hídrico en los cultivos, se requiere monitoreo continuo. El *streaming* permite ingerir las lecturas de humedad de los sensores tan pronto como ocurren, permitiendo al sistema enviar alertas inmediatas de "riego urgente" sin tener que esperar al fin del día para procesar la información.

**2. Procesamiento Batch (Por lotes / Programado):**
* **Componentes:** API Meteorológica y Archivos CSV (Bitácoras y cosechas) a través de Python y n8n.
* **Justificación:** Los datos del clima, aunque dinámicos, no requieren actualizaciones al segundo; basta con descargar el pronóstico y el historial de lluvia una vez al día (diariamente a las 06:00 a.m.). Igualmente, las bitácoras de riego y las cosechas se registran manualmente al finalizar los turnos o la temporada agrícola, por lo que su extracción y transformación ocurre mediante ejecución de tareas programadas (por lotes) una vez que se cuenta con un volumen consolidado de registros.

---

### 2.3. Consumo de API Pública (Opcional)

A continuación, se demuestra el uso de la librería `requests` de Python para conectarse a una API pública (Open-Meteo Archive) que actúa como fuente de datos climáticos externos (Lluvia, Viento y Temperatura). Este paso corresponde a la fase de **Extracción** del pipeline ETL:

```python
import requests

# URL de la API Histórica de Open-Meteo (Coordenadas para Neiva, Huila)
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 2.91,
    "longitude": -75.2669,
    "start_date": "2026-06-01",
    "end_date": "2026-10-03",
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "precipitation",
        "wind_speed_10m"
    ],
    "timezone": "auto"
}

# Consumo de la API pública
respuesta = requests.get(url, params=params)

if respuesta.status_code == 200:
    datos = respuesta.json()
    
    # Extraer las listas horarios para los primeros 3 registros
    horas = datos["hourly"]["time"]
    temperaturas = datos["hourly"]["temperature_2m"]
    humedades = datos["hourly"]["relative_humidity_2m"]
    temp_aparente = datos["hourly"]["apparent_temperature"]
    precipitacion = datos["hourly"]["precipitation"]
    viento = datos["hourly"]["wind_speed_10m"]
    
    # Mostrar los primeros 3 registros (Requisito de rúbrica)
    print("--- PRIMEROS 3 REGISTROS OBTENIDOS DE LA API ---")
    for i in range(3):
        print(f"Registro {i + 1}:")
        print(f"  Fecha y Hora      : {horas[i]}")
        print(f"  Temp (2m)         : {temperaturas[i]} °C")
        print(f"  Humedad Relativa  : {humedades[i]} %")
        print(f"  Temp Aparente     : {temp_aparente[i]} °C")
        print(f"  Precipitación     : {precipitacion[i]} mm")
        print(f"  Velocidad Viento  : {viento[i]} km/h")
        print("-" * 45)
else:
    print(f"Error al consultar la API. Código HTTP: {respuesta.status_code}")
```

---

## 3. Conclusión

El diseño del pipeline ETL para la Gestión del Riego Agroindustrial ilustra cómo la orquestación de datos convierte múltiples formatos y fuentes aisladas en información accionable. Se estructuró un flujo donde conviven herramientas de **streaming** (Kafka para la inmediatez de los sensores IoT) con procesos **batch** (Python/pandas orquestados vía n8n para el consumo de la API climática y archivos CSV operativos). Esta arquitectura híbrida garantiza tanto la reacción en tiempo real ante el estrés hídrico de la planta, como el análisis consolidado de la eficiencia del agua una vez por temporada en la base de datos relacional y tableros de Business Intelligence.

---

## 4. Referencias

* Food and Agriculture Organization of the United Nations (FAO). (2026). *Water data and resource assessment*. https://www.fao.org/land-water/water/water-data-and-resource-assessment
* IBM. (2024). *What is ETL (Extract, Transform, Load)?* IBM Think. https://www.ibm.com/think/topics/etl
* Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.
* McKinney, W. (2022). *Python for Data Analysis* (3rd ed.). O'Reilly Media.
