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

*   **$Acc_{Relativa}$:** Accesibilidad gravitacional calculada a partir del tiempo mínimo de viaje al polo de empleo más cercano (usando un umbral de decaimiento máximo de 120 minutos).
*   **$IM$:** Índice de Marginación de CONAPO normalizado en un rango de 0 a 1.

## 3. Implementación Topológica y el Supuesto de Transbordo (Fricción Espacial)

Para que el Algoritmo de Dijkstra pudiera navegar la red, se construyó un grafo dirigido (`nx.DiGraph()`) donde los nodos son estaciones y las aristas son los tiempos de recorrido. 

**Decisión Técnica sobre Transbordos:**
En el estándar GTFS, los tiempos oficiales de caminata entre líneas se alojan en el archivo `transfers.txt`. Dado que el set de datos depurado actual (`gtfs_limpio`) omitía este archivo, el algoritmo inicialmente leía cada línea del Metro como un sistema aislado.

Para resolver esta fragmentación y garantizar la continuidad de la red, se aplicó la siguiente regla de imputación topológica:
1.  **Conexión Lógica:** El script identifica estaciones que pertenecen a distintas líneas pero comparten el mismo identificador de nombre (`stop_name`), asumiendo que son estaciones de correspondencia.
2.  **Penalización Estándar (5 Minutos):** Se generó una arista bidireccional entre estos nodos asignando un costo fijo de **5 minutos**. En el modelado de movilidad urbana, este es el valor *proxy* estandarizado para simular la "fricción espacial" (recorrido peatonal por pasillos, cambios de nivel y tiempos de espera para el siguiente tren) cuando se carece de la micromedición topográfica exacta.

## 4. Enrutamiento Multi-Destino y Resultados del Piloto

El modelo ya no calcula rutas lineales simples. Se implementó una arquitectura escalable basada en diccionarios que evalúa simultáneamente las rutas desde zonas periféricas de origen hacia una matriz de polos de atracción laboral. El algoritmo selecciona dinámicamente el destino que ofrece la menor fricción temporal para el usuario antes de calcular el Índice de Accesibilidad.

**Nodos de Origen (Vulnerabilidad):**
*   Ecatepec (Ciudad Azteca)
*   Nezahualcóyotl (Línea B)
*   Chalco (La Paz)

**Nodos de Destino (Polos de Empleo):**
*   Centro CDMX (Pino Suárez)
*   Reforma / Polanco (Polanco)
*   Santa Fe (Observatorio)

**Matriz de Resultados:**

| Municipio de Origen | Polo Empleo Más Cercano | Tiempo de Viaje (Mins) | $IM$ (Marginación) | $IPT_{comp}$ Final |
| :--- | :--- | :--- | :--- | :--- |
| **Nezahualcóyotl** | Centro CDMX | 30.2 | 0.60 | **0.403** (Media-Alta) |
| **Ecatepec** | Centro CDMX | 44.2 | 0.75 | **0.645** (Severa) |
| **Chalco** | Centro CDMX | 50.3 | 0.65 | **0.692** (Severa) |

*Conclusión Operativa:* El modelo computacional mapea con éxito la exclusión territorial, demostrando matemáticamente cómo las periferias más alejadas como Chalco alcanzan niveles críticos de pobreza de tiempo.

## 5. Representación Visual de la Red (Grafo)

Para comprobar la sanidad de la estructura de datos más allá de los resultados numéricos, se integró la librería `matplotlib` para renderizar visualmente la matriz espacial del GTFS.

La visualización generada (`grafo_red_cronomx.png`) valida la correcta construcción del modelo mediante tres elementos clave:
*   **Nodos Celestes:** Representan las 568 paradas intermedias procesadas del sistema Metro y Metrobús.
*   **Aristas Grises:** Trazan las conexiones de viaje direccional, incluyendo los enlaces artificiales de transbordo de 5 minutos generados por el script.
*   **Nodos Rojos:** Resaltan geográficamente las 6 estaciones clave inyectadas en los diccionarios de configuración (los 3 orígenes periféricos y los 3 destinos centrales). 

El mapa de nodos demuestra que el motor lógico ha logrado unificar ramales dispersos en un solo tejido de movilidad navegable, sentando la base técnica para la integración del índice en la interfaz interactiva de SIGMA.
