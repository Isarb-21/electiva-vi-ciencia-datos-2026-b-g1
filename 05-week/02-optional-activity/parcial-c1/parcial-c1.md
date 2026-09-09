# Parcial Práctico – Corte 1
## 🛍️ Gestión Comercial y de Inventario Basada en Datos: Caso Vélez S.A.S.

**Isabella Ramos Betancourt**  
Facultad de Ingeniería, Corporación Universitaria del Huila (CORHUILA)  
Ciencia de Datos (Cód. 69109) [Pénsum 40D, Grupo 1]  
Jesús Ariel Gonzáles Bonilla  
Septiembre 8 de 2026

---

## 1. Introducción

La Ciencia de Datos ofrece herramientas que permiten a las organizaciones transformar grandes volúmenes de información operativa en conocimiento útil para la toma de decisiones estratégicas. En el sector de la moda y la marroquinería, donde la variedad de referencias, tallas y colores puede superar miles de combinaciones por temporada, gestionar el inventario y anticipar la demanda representa uno de los principales retos empresariales. Vélez S.A.S., empresa colombiana fundada en 1986 y especializada en la fabricación y comercialización de productos de cuero, opera más de 300 puntos de venta en el país y cuenta con un canal de comercio electrónico en crecimiento, lo que la convierte en un caso representativo de organización intensiva en datos (Vélez, 2024).

Este trabajo presenta un ejercicio práctico de diagnóstico de datos aplicado a la gestión comercial y de inventario de Vélez. Se identifican cuatro tipos de datos generados en su cadena de valor y se clasifican según su estructura. A partir de ellos, se formula una pregunta de analítica descriptiva y una de analítica predictiva. Luego, se construye un diagrama de flujo que representa el recorrido de los datos desde su origen hasta la visualización para la toma de decisiones. Por último, se establece la diferencia conceptual entre ambos tipos de analítica en idioma inglés.

---

## 2. Desarrollo del parcial

### 2.1. Identificación y clasificación de tipos de datos

Para responder a los retos de gestión comercial de Vélez, se requieren datos provenientes de distintas fuentes a lo largo de su cadena de valor. Provost y Fawcett (2013) señalan que la comprensión del tipo de dato es el primer paso para definir qué técnicas de análisis son aplicables y qué infraestructura de almacenamiento se necesita. Chen (2023) distingue tres categorías fundamentales — estructurada, semiestructurada y no estructurada — según el grado de organización interna del dato y su capacidad para ser interpretado directamente por sistemas de gestión de bases de datos.

| # | Fuente / Dato | Descripción | Tipo |
|:-:|---|---|:-:|
| 1 | 🧾 **Transacciones de venta (POS / ERP)** | Registros de cada venta realizada en tienda física o en línea: referencia del producto, talla, color, precio, descuento, fecha, tienda y método de pago. Se almacenan en el sistema ERP corporativo con un esquema fijo de campos. | `Estructurado` |
| 2 | 📦 **Pedidos del canal digital (JSON)** | Datos de los pedidos realizados a través de la tienda en línea: carrito de compra, dirección de envío, estado del pedido y tiempos de entrega. Los campos pueden variar entre pedidos según opciones seleccionadas por el cliente. | `Semiestructurado` |
| 3 | 📸 **Fotografías de productos y campañas** | Imágenes de colecciones publicadas en Instagram, el sitio web corporativo y catálogos digitales. No poseen una organización interna interpretable automáticamente; su análisis requiere visión por computadora. | `No estructurado` |
| 4 | 💬 **Reseñas y comentarios de clientes** | Opiniones escritas en Google Maps, el sitio web de Vélez y redes sociales. El texto libre no sigue plantilla alguna; para extraer información útil se requiere procesamiento de lenguaje natural (NLP). | `No estructurado` |

Los cuatro tipos de datos cubren el espectro completo de estructura: registros transaccionales altamente organizados (fuente 1), documentos con campos variables (fuente 2) y contenido generado por usuarios sin esquema predefinido (fuentes 3 y 4), lo que refleja la diversidad de información que una empresa de retail moderno debe gestionar (Mayer-Schönberger & Cukier, 2013).

---

### 2.2. Preguntas de analítica

#### 2.2.1. Pregunta de analítica descriptiva

> *¿Cuáles fueron las diez referencias de calzado más vendidas durante la temporada de fin de año 2025, y cuál fue el ingreso total generado por cada una en los canales físico y digital?*

Esta pregunta busca describir lo que ya ocurrió a partir del historial de transacciones almacenado en el ERP de Vélez. La analítica descriptiva organiza, resume y presenta los datos pasados mediante métricas como totales, promedios y rankings, sin proyectar hacia el futuro (Delen, 2020). Su respuesta permite identificar qué referencias impulsan los ingresos por temporada y comparar el desempeño entre el canal físico y el digital, orientando decisiones de reposición y exhibición para la siguiente colección.

#### 2.2.2. Pregunta de analítica predictiva

> *¿Qué cantidad de unidades por referencia, talla y color deberá producir y distribuir Vélez en cada región del país durante el primer trimestre de 2026, con el fin de maximizar la disponibilidad del producto y minimizar el exceso de inventario?*

Esta pregunta emplea modelos de aprendizaje automático entrenados con el historial de ventas, datos estacionales, tendencias de moda y comportamiento de compra por región, con el propósito de anticipar la demanda futura. La analítica predictiva transforma patrones históricos en proyecciones accionables que orientan decisiones de producción y logística (Provost & Fawcett, 2013). Dado que se cuenta con registros históricos etiquetados por resultado de venta, el enfoque supervisado — mediante modelos como XGBoost o redes LSTM para series de tiempo — es el más adecuado para este caso.

---

### 2.3. Diagrama de flujo de datos

El siguiente diagrama representa el recorrido de los datos en el ecosistema de información de Vélez, desde las fuentes de origen hasta la visualización para la toma de decisiones estratégicas y operativas.

```
  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
  │     FUENTE      │  │     FUENTE      │  │     FUENTE      │  │     FUENTE      │
  │  Transacciones  │  │  Pedidos online │  │  Fotografías    │  │  Reseñas        │
  │  POS / ERP      │  │  JSON           │  │  productos      │  │  clientes       │
  │  (Estructurado) │  │  (Semiestruc.)  │  │  (No estruc.)   │  │  (No estruc.)   │
  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
           │                    │                    │                    │
           └────────────────────┴──────────┬─────────┘────────────────────┘
                                           │
                                           ▼
                          ┌────────────────────────────────┐
                          │        ALMACENAMIENTO          │
                          │  Data Warehouse (ERP / SAP)    │
                          │  + Data Lake (Azure / AWS S3)  │
                          │  para imágenes y texto libre   │
                          └───────────────┬────────────────┘
                                          │
                                          ▼
                          ┌────────────────────────────────┐
                          │            ANÁLISIS            │
                          │  · Limpieza y transformación   │
                          │  · Estadística descriptiva     │
                          │    (ventas, rankings, tendenc.)│
                          │  · Modelo predictivo supervis. │
                          │    (XGBoost / LSTM — demanda)  │
                          │  · Análisis de sentimiento NLP │
                          └───────────────┬────────────────┘
                                          │
                                          ▼
                          ┌────────────────────────────────┐
                          │         VISUALIZACIÓN          │
                          │  Dashboard Power BI:           │
                          │  · Ventas por región y canal   │
                          │  · Predicción de demanda       │
                          │  · Alertas de inventario       │
                          │  · Sentimiento del cliente     │
                          └────────────────────────────────┘
```

**Descripción del flujo:**

1. **Fuente:** Los datos se originan en cuatro fuentes principales. Las transacciones en puntos de venta físicos y en la tienda en línea generan registros estructurados almacenados en el ERP corporativo. Los pedidos digitales llegan en formato JSON semiestructurado con campos variables según las opciones del cliente. Las fotografías de colecciones y las reseñas escritas de clientes constituyen datos no estructurados que requieren procesamiento especial antes de poder ser analizados.

2. **Almacenamiento:** Los datos transaccionales estructurados se consolidan en un Data Warehouse (SAP BW), mientras que los datos no estructurados — imágenes y texto libre — se almacenan en un Data Lake sobre plataformas de nube como Azure Data Lake Storage o AWS S3. Esta arquitectura híbrida permite gestionar la variedad característica de los datos de una empresa de retail moderno (Inmon & Linstedt, 2022).

3. **Análisis:** Sobre los datos almacenados se aplican procesos de limpieza, integración y modelado. La analítica descriptiva genera indicadores de desempeño por referencia, canal y región. Los modelos predictivos supervisados, como XGBoost para la clasificación de demanda o redes LSTM para series de tiempo, proyectan las necesidades de inventario por talla, color y punto de venta. El análisis de sentimiento, aplicado sobre las reseñas de clientes, complementa el diagnóstico comercial.

4. **Visualización:** Los resultados se presentan en un tablero interactivo en Power BI, accesible para los equipos de planeación, comercial y logística, mostrando las ventas históricas, las predicciones de demanda y las alertas de inventario crítico, además del análisis de sentimiento derivado de las opiniones de los clientes.

---

### 2.4. Diferencia entre analítica descriptiva y analítica predictiva (en inglés)

> **Frase 1:**
> Descriptive analytics examines historical sales and operational data to explain *what has already happened*, providing Vélez with a clear picture of past performance through metrics such as total revenue, top-selling references, and regional sales rankings.

> **Frase 2:**
> Predictive analytics applies machine learning models trained on historical patterns to forecast *what is likely to happen in the future*, allowing Vélez to anticipate product demand by size, color, and region, and to make proactive inventory and production decisions.

---


### 2.5. Enlace del Repositorio

Este es el enlace del repositorio: https://github.com/Isarb-21/electiva-vi-ciencia-datos-2026-b-g1 

---

## 3. Conclusión

El ejercicio desarrollado demuestra que Vélez S.A.S. genera una diversidad significativa de datos a lo largo de su operación comercial, abarcando los tres tipos de estructura: registros transaccionales estructurados del ERP, pedidos digitales semiestructurados en formato JSON, e imágenes y reseñas de clientes no estructuradas. Esta variedad exige una arquitectura de almacenamiento híbrida — Data Warehouse para datos tabulares y Data Lake para contenido multimedia y textual — que garantice la disponibilidad y la integridad de la información para su posterior análisis.

Las preguntas de analítica formuladas reflejan los dos niveles de madurez analítica más relevantes para una empresa de retail: la analítica descriptiva, que permite entender qué referencias han generado mayor valor por canal y región, y la analítica predictiva, que habilita la planificación anticipada de producción e inventario para evitar tanto el desabastecimiento como el exceso de stock. La capacidad de anticipar la demanda por talla, color y punto de venta representa una ventaja competitiva directa para una empresa con más de 300 tiendas en el país.

Finalmente, el diagrama de flujo construido — desde las fuentes de datos hasta el dashboard en Power BI — permite visualizar de manera integral cómo los datos se transforman en decisiones operativas y estratégicas, evidenciando el valor de la Ciencia de Datos como disciplina aplicada a la gestión empresarial moderna.

---

## 4. Referencias

Chen, M. (2023). *Foundations of database management systems* (3.ª ed.). Pearson Education.

Delen, D. (2020). *Prescriptive analytics: The final frontier for evidence-based management and optimal decision making*. Pearson FT Press.

Inmon, W. H., & Linstedt, D. (2022). *Data architecture: A primer for the data scientist* (2.ª ed.). Academic Press.

Mayer-Schönberger, V., & Cukier, K. (2013). *Big data: A revolution that will transform how we live, work, and think*. Houghton Mifflin Harcourt.

Provost, F., & Fawcett, T. (2013). *Data science for business: What you need to know about data mining and data-analytic thinking*. O'Reilly Media.

Vélez. (2024). *Quiénes somos*. https://www.velez.com.co/pages/quienes-somos
