# Actividad Calificable – Corte 1
## Diagnóstico de datos de un proceso
###  🌱 Gestión del Riego Agroindustrial basada en Datos
**Isabella Ramos Betancourt**  
Facultad de Ingeniería, Corporación Universitaria del Huila (CORHUILA)  
Ciencia de Datos (Cód. 69109) [Pénsum 40D, Grupo 1]  
Jesús Ariel Gonzáles Bonilla  
Agosto 30 de 2026

---

## 1. Introducción

La Ciencia de Datos se aplica en diversos procesos productivos para analizar información y optimizar la toma de decisiones. En el sector agroindustrial, el uso de datos permite evolucionar de una estrategia de riego basada en estimaciones empíricas o calendarios fijos hacia un enfoque centrado en el estado real del suelo y del cultivo. En este contexto, la gestión del riego basada en datos emplea variables operativas como la humedad del suelo, la temperatura y el consumo de agua para apoyar decisiones más eficientes y sostenibles. De acuerdo con la FAO (2026), contar con datos confiables sobre el agua es fundamental para apoyar la toma de decisiones en los sistemas agroalimentarios, y herramientas como WaPOR utilizan datos satelitales y de sensores para evaluar la productividad del agua en los cultivos.

Este trabajo presenta un caso práctico de gestión del riego en un proceso de producción agroindustrial. Para su desarrollo, se identifican las variables clave, su tipología y sus fuentes de origen. Asimismo, se evalúa el tipo de analítica requerido y se analiza si el volumen de información cumple con las características de Big Data a través de sus dimensiones principales (V). Por último, se estructura el ciclo de vida del proyecto, desde la pregunta inicial hasta la toma de decisiones.

---

## 2. Desarrollo de la actividad

### 2.1. Problema y pregunta de datos

En un proceso de producción agroindustrial, una programación deficiente del riego puede generar dos tipos de pérdidas: el desperdicio de agua cuando se riega más de lo necesario, y la pérdida de rendimiento cuando el cultivo entra en estrés hídrico por falta de irrigación oportuna. Por ello, resulta fundamental monitorear el comportamiento del suelo y del clima para detectar desviaciones de las condiciones óptimas de forma temprana.

Esta problemática se aborda mediante la gestión del riego basada en datos, la cual utiliza variables como la humedad del suelo, la temperatura y los datos de precipitación para determinar cuándo y cuánto regar (FAO, 2026). Este enfoque cuenta con antecedentes en la industria: la FAO (2026) documenta el uso de herramientas satelitales como WaPOR en múltiples países para monitorear la productividad del agua en cultivos y apoyar la planificación del riego de manera basada en evidencia.

En consecuencia, el problema consiste en determinar si los datos operativos e históricos del proceso de riego permiten identificar las condiciones de suelo y clima asociadas a un mayor rendimiento del cultivo, con el fin de optimizar la programación del riego, surgiendo la siguiente **pregunta de datos**:

> *¿Cómo se pueden utilizar los datos de humedad del suelo, temperatura y consumo de agua para mejorar la programación del riego y optimizar el rendimiento de los cultivos?*

---

### 2.2. Inventario de datos

Para responder a la pregunta planteada, se requieren variables sobre el estado del suelo, las condiciones climáticas y los resultados de producción. La FAO (2026) destaca el uso de sensores de humedad del suelo y datos satelitales de temperatura y vegetación como insumos principales para la evaluación de la productividad del agua en sistemas agrícolas, mientras que IBM (2024) evidencia cómo la integración de datos estructurados y no estructurados de múltiples fuentes permite construir análisis más completos sobre procesos productivos.

| # | Fuente / Dato | Descripción | Tipo |
|:-:|---|---|:-:|
| 1 | 🌡️ Sensores de humedad del suelo | Registran el porcentaje de humedad en diferentes profundidades y puntos del cultivo. | `Estructurado` |
| 2 | 🌡️ Sensores de temperatura | Capturan la temperatura ambiente y del suelo de forma continua. | `Estructurado` |
| 3 | 💧 Medidores de consumo de agua | Registran el volumen de agua utilizado en cada evento de riego por lote. | `Estructurado` |
| 4 | 🌧️ Pluviómetros (precipitación) | Miden la cantidad de lluvia recibida en el área del cultivo por período. | `Estructurado` |
| 5 | 🌿 Registro de etapa de crecimiento | Base de datos con la fase fenológica del cultivo por fecha y lote. | `Estructurado` |
| 6 | 📊 Historial de rendimiento de cosechas | Registros con el volumen y calidad de producción obtenida por ciclo y lote. | `Estructurado` |
| 7 | 📋 Bitácoras de riego (órdenes de trabajo) | Documentos con actividades de riego realizadas, técnico responsable y fecha. Pueden estar en formularios o sistemas de gestión agrícola. | `Semiestructurado` |
| 8 | 🛰️ Imágenes satelitales y de drones | Imágenes del cultivo para evaluar el índice NDVI y detectar zonas de estrés hídrico. | `No estructurado` |

El inventario integra métricas numéricas obtenidas en tiempo real (fuentes 1–4), datos históricos de producción (fuentes 5–6) y registros cualitativos del historial operativo (fuentes 7–8), cubriendo los tres tipos de estructura de datos.

---

### 2.3. Tipo de analítica y Big Data

#### 2.3.1. Tipo de analítica

El proyecto abarca **cuatro niveles de analítica** que se complementan progresivamente:

| Tipo | Pregunta clave | Aplicación al caso |
|---|:-:|---|
| 🔍 **Descriptiva** | ¿Qué ocurrió? | Identificar qué lotes tuvieron mayor consumo de agua y cuál fue el comportamiento promedio de humedad, temperatura y rendimiento por ciclo. **Es el eje principal del diagnóstico.** |
| 🔎 **Diagnóstica** | ¿Por qué ocurrió? | Analizar correlaciones entre variables operativas (humedad, temperatura, precipitación, etapa de crecimiento) y resultados de producción para entender las causas de ineficiencia hídrica. |
| 📈 **Predictiva** | ¿Qué podría ocurrir? | Estimar con anticipación la necesidad de riego de cada lote usando modelos entrenados sobre el historial etiquetado disponible (ML supervisado: Random Forest, XGBoost, LSTM). |
| ⚙️ **Prescriptiva** | ¿Qué se debe hacer? | Generar un plan de riego óptimo para la semana siguiente que maximice el rendimiento y minimice el consumo de agua, combinando el modelo predictivo con algoritmos de optimización. |

El **punto de partida es la analítica descriptiva**, ya que el objetivo inmediato es comprender qué condiciones históricas han estado asociadas a un mayor rendimiento (IBM, 2024). La analítica diagnóstica complementa este análisis al explicar las causas de los ciclos ineficientes.

#### 2.3.2. ¿Es un caso de Big Data?

Este proyecto **tiene potencial de convertirse en un caso de Big Data** si la operación cuenta con múltiples lotes monitoreados y sensores que generen información de forma continua durante varios ciclos de producción. El análisis por las **cinco V** confirma esto:

| V | Evaluación para este caso |
|:-:|---|
| 📦 **Volumen** | Múltiples sensores en distintos puntos del cultivo generan miles de registros diarios. Acumulados durante años de producción, el volumen puede superar la capacidad de herramientas convencionales de análisis. |
| ⚡ **Velocidad** | Los sensores pueden generar datos con frecuencia horaria o mayor, especialmente durante períodos críticos de alta temperatura. IBM (2026) señala que la velocidad determina la capacidad del sistema para responder a cambios en tiempo oportuno. |
| 🗂️ **Variedad** | El proyecto integra datos numéricos estructurados (sensores), registros semiestructurados (bitácoras) e imágenes satelitales no estructuradas. **Esta es la V más desafiante técnicamente.** |
| ✅ **Veracidad** | Los datos deben ser confiables: un sensor descalibrado puede llevar a decisiones incorrectas de riego. **Esta es la V más crítica operativamente**, ya que un dato erróneo de humedad impacta directamente el rendimiento de la cosecha. |
| 💰 **Valor** | El análisis permite reducir el consumo de agua, mejorar el rendimiento del cultivo y aumentar la eficiencia económica del proceso, justificando la inversión en infraestructura de datos. |


**Conclusión:** el proyecto presenta características de Big Data principalmente por la **variedad** (múltiples formatos y fuentes) y la **veracidad** (calidad crítica de los datos de sensores). El **volumen** y la **velocidad** dependen de la escala de la operación; en una finca con decenas de lotes y muestreo horario, estas dimensiones también aplican plenamente.

---

### 2.4. Ciclo de vida del proyecto

```
┌──────────────────────────────────────────────────────────────┐
│                      1. PREGUNTA                             │
│  ¿Cómo usar los datos de humedad, temperatura y consumo      │
│  de agua para optimizar el riego y el rendimiento?           │
│  → Analítica descriptiva como punto de partida               │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      2. OBTENER                              │
│  Recolectar datos de sensores (humedad, temperatura,         │
│  precipitación), bitácoras de riego, historial de cosechas   │
│  e imágenes satelitales. Fuentes: IoT, pluviómetros,         │
│  sistemas de gestión agrícola y teledetección (FAO, 2026).   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      3. LIMPIAR                              │
│  Detectar y corregir valores faltantes, lecturas fuera de    │
│  rango (sensores descalibrados), registros duplicados e       │
│  inconsistencias entre fuentes. Aplicar reglas de rango,     │
│  IQR y comparación cruzada entre sensores y pluviómetros.    │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      4. ANALIZAR                             │
│  Calcular estadísticas descriptivas por lote y ciclo.        │
│  Identificar correlaciones entre humedad, temperatura,        │
│  consumo de agua y rendimiento de cosecha. Detectar patrones │
│  históricos de eficiencia hídrica (analítica descriptiva     │
│  y diagnóstica).                                             │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      5. VISUALIZAR                           │
│  Presentar dashboards en Power BI con: consumo de agua por   │
│  lote, relación humedad–rendimiento, comportamiento de        │
│  temperatura por etapa de cultivo y tendencias históricas     │
│  de producción. Facilitar la lectura por el técnico agrícola.│
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      6. DECIDIR                              │
│  Programar el riego de cada lote según las condiciones       │
│  óptimas identificadas en el análisis histórico. Reducir     │
│  desperdicio de agua y mejorar la eficiencia hídrica del     │
│  proceso agroindustrial.                                     │
└──────────────────────────────────────────────────────────────┘
```

---

### 2.5. Problem & Data

Agroindustrial irrigation management faces a critical operational challenge: poorly scheduled irrigation results in two types of losses — water waste when crops are over-irrigated, and yield reduction when crops experience hydric stress due to insufficient or delayed watering. The goal of this project is to determine whether historical and real-time operational data can reveal the soil and climate conditions most strongly associated with high crop yield, enabling evidence-based irrigation scheduling. The required dataset includes eight data sources across all structure types: structured IoT sensor readings (soil moisture, temperature, water consumption, precipitation), a structured crop growth stage registry, structured harvest yield records, semi-structured irrigation logbooks, and unstructured satellite and drone imagery for NDVI-based stress detection. Descriptive analytics is the primary approach, since the immediate objective is to characterize past irrigation cycles and identify patterns between operational variables and production outcomes; diagnostic analytics complements this by uncovering the root causes of inefficient cycles. The project may qualify as Big Data in large-scale operations due to high data variety (structured, semi-structured, and unstructured sources integrated in a single pipeline) and the critical veracidad of sensor data, where a single miscalibrated humidity sensor can trigger incorrect irrigation decisions that directly affect crop performance.

---

## 3. Conclusión

El diagnóstico realizado demuestra la aplicabilidad de la Ciencia de Datos para transformar la gestión del riego en el sector agroindustrial. La selección de ocho variables — que abarcan datos estructurados, semiestructurados y no estructurados — responde a metodologías validadas en la industria para el monitoreo continuo de cultivos y la evaluación de la productividad hídrica. La implementación de la analítica descriptiva permite pasar del análisis intuitivo basado en experiencia del técnico al análisis sistemático de patrones históricos que revelan qué condiciones de riego están asociadas a un mayor rendimiento.

El análisis de las cinco V confirma que el proyecto puede calificar como un caso de Big Data, siendo la variedad de fuentes y la veracidad de los datos de sensores las dimensiones más críticas en este contexto agroindustrial. La escala de la operación determina si el volumen y la velocidad también alcanzan las dimensiones propias del Big Data.

Finalmente, la estructuración del ciclo de vida — desde la pregunta inicial hasta la decisión operativa — garantiza la trazabilidad del proceso y asegura que el análisis de datos se traduzca en decisiones eficientes que reduzcan el desperdicio de agua y mejoren la rentabilidad del proceso productivo.

---

## 4. Referencias

Food and Agriculture Organization of the United Nations. (2026). *Water data and resource assessment*. https://www.fao.org/land-water/water/water-data-and-resource-assessment

Food and Agriculture Organization of the United Nations. (2026). *Tools in co-development: WaPOR, remote sensing for water productivity*. https://www.fao.org/in-action/remote-sensing-for-water-productivity/country-activities/tools-in-co-development

IBM. (2024). *What is Big Data analytics?* IBM Think. https://www.ibm.com/think/topics/big-data-analytics

IBM. (2026). *What is data velocity?* IBM Think. https://www.ibm.com/think/topics/data-velocity
