# Actualización Metodológica: Índice de Pobreza de Tiempo (IPT)
**Proyecto:** CronoMX (SIGMA)
**Fase:** Semana 3 - Integración de Datos Reales GTFS

---

## 1. Selección y Justificación del Modelo Matemático

Para la implementación oficial de CronoMX se ha seleccionado el **Índice Compuesto de Pobreza de Tiempo ($IPT_{comp}$)** como la métrica central de análisis. 

$$IPT_{comp} = (1 - Acc_{Relativa}) \times (1 + IM)$$

Donde:
*   $Acc_{Relativa}$: Accesibilidad al polo de empleo más cercano, con base en el tiempo de traslado (decaimiento máximo de 120 minutos).
*   $IM$: Índice de Marginación de CONAPO normalizado (0 a 1).

**Justificación de la elección:**
Se seleccionó este modelo por ser la aproximación más robusta y completa a la realidad urbana de la ZMVM. A diferencia de las métricas que solo miden el tiempo cronológico ($IPT_{gap}$), el modelo compuesto refleja la **doble penalización estructural** que sufren las periferias: la ineficiencia de la red de transporte masivo cruzada con una alta vulnerabilidad sociodemográfica. Esta fórmula permite visibilizar y cuantificar la exclusión territorial severa de manera proporcional.

---

## 2. Validación Computacional con Datos Reales

Para validar que la fórmula produce resultados precisos y aplicables, se diseñó una arquitectura de procesamiento de grafos utilizando Python (`pandas`, `numpy`) y la librería de teoría de redes `networkx`, alimentada directamente por los archivos reales del sistema GTFS (`stops.csv` y `stop_times.csv`).

### Proceso de Construcción del Modelo Espacial:
1.  **Limpieza y Parseo de Horarios:** Se convirtieron los tiempos de llegada (`arrival_time`) del formato HH:MM:SS a minutos absolutos continuos.
2.  **Construcción del Grafo Dirigido:** Se estructuró un grafo `nx.DiGraph()` donde cada estación es un nodo y cada tramo entre estaciones es una arista direccional. El peso de la arista (`weight`) corresponde al tiempo real programado para ese tramo específico.
3.  **Lógica de Transbordos (Caminata):** Para conectar las distintas líneas independientes, se programó una regla de adyacencia que une estaciones con el mismo nombre, añadiendo una penalización estándar de 5 minutos de fricción por el cruce peatonal entre andenes.
4.  **Algoritmo de Enrutamiento:** Se implementó el **Algoritmo de Dijkstra** para buscar la ruta más rápida (shortest path) minimizando la sumatoria del peso en minutos.

### Diseño Multi-Destino
El algoritmo es altamente escalable y busca simultáneamente la ruta más corta desde los nodos de origen en las periferias hacia una matriz de los principales **Polos de Empleo** de la ZMVM:
*   **Centro CDMX** (Pino Suárez - Línea 2)
*   **Reforma / Polanco** (Polanco - Línea 7)
*   **Santa Fe** (Observatorio - Línea 1)

El modelo asume dinámicamente el tiempo mínimo (polo más cercano) para calcular el índice $Acc_{Relativa}$, reflejando la toma de decisión real de los usuarios.

---

## 3. Resultados del Piloto y Mapeo de Exclusión

Al correr el algoritmo sobre la red real, se obtuvieron métricas exactas que demuestran la eficacia de la fórmula para estratificar la vulnerabilidad. 

| Municipio de Origen | Nodo (Estación) | Polo Empleo Más Cercano | Tiempo de Viaje (Mins) | $IM$ (Marginación) | $IPT_{comp}$ Final |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cuauhtémoc** | Insurgentes (L1) | Centro CDMX | 11.4 | 0.10 | **0.104** (Baja) |
| **Nezahualcóyotl** | Nezahualcóyotl (LB) | Centro CDMX | 30.2 | 0.60 | **0.403** (Media-Alta) |
| **Ecatepec** | Ciudad Azteca (LB) | Centro CDMX | 44.2 | 0.75 | **0.645** (Severa) |
| **Chalco** | La Paz (LA) | Centro CDMX | 50.3 | 0.65 | **0.692** (Severa) |

**Conclusión Operativa:** El modelo computacional logra mapear con éxito cómo zonas periféricas como Chalco (50.3 minutos mínimos en red) sufren índices de exclusión casi siete veces mayores que zonas céntricas (0.692 vs 0.104), cumpliendo con los objetivos centrales del proyecto SIGMA.
