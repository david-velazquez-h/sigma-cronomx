# Reporte Metodológico Actualizado: Modelado Espacial y Datos Reales GTFS
**Proyecto:** CronoMX / SIGMA
**Fase:** Semana 3 - Validación Computacional y Topológica
**Autor:** Max

---

## 1. Evolución del Modelo: Semana 2 vs. Semana 3

El desarrollo del Índice de Pobreza de Tiempo (IPT) ha transitado de una validación teórica estática hacia una implementación algorítmica dinámica sobre la infraestructura real de la CDMX.

*   **Semana 2 (Fase Estática):** La evaluación se centró en definir el marco conceptual. Se debatió entre usar una Brecha de Tiempo Libre ($IPT_{gap}$) o un índice relativo. Las pruebas se realizaron con vectores de datos simulados (*dummy data*) y promedios teóricos de viaje, sin considerar la geografía real ni las interconexiones físicas de las líneas de transporte.
*   **Semana 3 (Fase Dinámica y Espacial):** Se adoptó oficialmente el **Índice Compuesto ($IPT_{comp}$)**. La innovación principal es el abandono de los promedios estáticos; el cálculo ahora se ejecuta mediante un motor de grafos matemáticos (`networkx`) que lee directamente la base de datos abierta de movilidad (`stops.csv` y `stop_times.csv`), permitiendo mapear la asimetría territorial real mediante el algoritmo de Dijkstra.

## 2. Definición de la Fórmula Oficial

El modelo adoptado penaliza doblemente a los territorios que sufren desconexión física y vulnerabilidad social:

$$IPT_{comp} = (1 - Acc_{Relativa}) \times (1 + IM)$$

*   **$Acc_{Relativa}$:** Accesibilidad gravitacional calculada a partir del tiempo mínimo de viaje al polo de empleo más cercano (usando un umbral de decaimiento de 120 minutos).
*   **$IM$:** Índice de Marginación de CONAPO normalizado en un rango de 0 a 1.

## 3. Implementación Topológica y el Supuesto de Transbordo (Fricción Espacial)

Para que el Algoritmo de Dijkstra pudiera navegar la red, se construyó un grafo dirigido (`nx.DiGraph()`) donde los nodos son estaciones y las aristas son los tiempos de recorrido. 

**Decisión Técnica sobre Transbordos:**
En el estándar GTFS, los tiempos oficiales de caminata entre líneas se alojan en el archivo `transfers.txt`. Dado que el set de datos depurado actual (`gtfs_limpio`) omitía este archivo, el algoritmo inicialmente leía cada línea del Metro como un sistema aislado, arrojando tiempos de conexión infinitos (`inf`).

Para resolver esta fragmentación y garantizar la continuidad de la red, se aplicó la siguiente regla de imputación topológica:
1.  **Conexión Lógica:** El script identifica estaciones que pertenecen a distintas líneas pero comparten el mismo identificador de nombre (`stop_name`), asumiendo que son estaciones de correspondencia.
2.  **Penalización Estándar (5 Minutos):** Se generó una arista bidireccional entre estos nodos asignando un costo fijo de **5 minutos**. En el modelado de movilidad urbana, este es el valor *proxy* estandarizado para simular la "fricción espacial" (recorrido peatonal por pasillos, cambios de nivel y tiempos de espera para el siguiente tren) cuando se carece de la micromedición topográfica exacta.

## 4. Enrutamiento Multi-Destino

El modelo ya no calcula rutas lineales simples. Se implementó una arquitectura escalable basada en diccionarios que evalúa simultáneamente las rutas desde zonas periféricas de origen hacia una matriz de polos de atracción laboral:

*   **Orígenes (Vulnerabilidad):** Ecatepec (Ciudad Azteca), Nezahualcóyotl (Línea B) y Chalco (La Paz).
*   **Destinos (Empleo):** Centro Histórico (Pino Suárez), Reforma/Polanco (Polanco) y Santa Fe (Observatorio).

El algoritmo selecciona dinámicamente el destino que ofrece la menor fricción temporal para el usuario antes de calcular el Índice de Accesibilidad.

## 5. Representación Visual de la Red (Grafo)

Para comprobar la sanidad de la estructura de datos más allá de los resultados numéricos, se integró la librería `matplotlib` para renderizar visualmente la matriz espacial del GTFS.

La visualización generada (`grafo_red_cronomx.png`) valida la correcta construcción del modelo mediante tres elementos clave:
*   **Nodos Celestes:** Representan las 568 paradas intermedias procesadas del sistema Metro y Metrobús.
*   **Aristas Grises:** Trazan las 928 conexiones de viaje direccional, incluyendo los enlaces artificiales de transbordo de 5 minutos generados por el script.
*   **Nodos Rojos:** Resaltan geográficamente las 6 estaciones clave inyectadas en los diccionarios de configuración (orígenes periféricos y destinos centrales). 

El mapa de nodos demuestra que el motor lógico ha logrado unificar ramales dispersos en un solo tejido de movilidad navegable, sentando la base técnica para la integración del índice en la interfaz interactiva de SIGMA.oritmo de Dijkstra** para buscar la ruta más rápida (shortest path) minimizando la sumatoria del peso en minutos.

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
