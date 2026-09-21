# Reporte Metodológico: Modelado del Índice de Pobreza de Tiempo (IPT)
**Proyecto:** CronoMX / SIGMA
**Autor:** Max
**Estado:** Iteración Piloto (Implementación en Jupyter Lab)

## 1. Objetivo
Formular matemáticamente el concepto de "Pobreza de Tiempo Relacionada con el Transporte" (Transport-Related Time Poverty) para la Zona Metropolitana del Valle de México (ZMVM). El índice busca cuantificar cómo la fricción espacial, las ineficiencias de la red de transporte masivo (tiempos de espera y transbordo) y las condiciones sociodemográficas merman sistemáticamente el tiempo libre de los usuarios, restringiendo su desarrollo personal y social.

## 2. Delimitación y Alcance
* **Datos Base:** Archivos GTFS estáticos filtrados (Metro y Metrobús) procesados mediante Python (`pandas`, `networkx`).
* **Fase de Prueba:** La validación empírica inicial se ejecuta sobre 3 municipios piloto (Ecatepec, Iztapalapa, Cuauhtémoc) como *sanity check* algorítmico antes del escalamiento a toda la red ZMVM.
* **Limitación Teórica:** El índice mide una aproximación algorítmica espacial mediante tiempos observados en la red GTFS y datos demográficos proxy, no encuestas directas.

## 3. Marco Metodológico (Candidatos de Ecuación)

### 3.1. Brecha Decompuesta de Tiempo Libre ($IPT_{gap}$)
Evalúa el porcentaje del "presupuesto temporal de movilidad" que es expropiado por el sistema.
$$IPT_{gap, i} = \frac{\sum_{m \in M} p_m \cdot (t_{ij}^m + t_{espera}^m + t_{transbordo}^m)}{T_{\text{disponible}}}$$
* **Criterio de Pobreza:** Se diagnostica "Pobreza de Tiempo" si $IPT_{gap, i} \ge 1.0$. Implica invasión directa a horas reproductivas/descanso.

### 3.2. Índice Relativo de Fricción Temporal ($IPT_{rel}$)
Mide la penalización temporal de un trayecto considerando el hacinamiento.
$$IPT_{rel, i} = \frac{t_{obs, i}}{t_{norm}} \cdot \left(1 + \alpha \cdot \frac{A_i}{C_i}\right)$$
* **Interpretación:** Un índice de 4.0 indica que, ajustado por saturación ($A_i/C_i$), el viaje representa un costo equivalente a 4 veces el tiempo normativo ideal ($t_{norm}$).

### 3.3. Índice Compuesto de Accesibilidad y Vulnerabilidad ($IPT_{comp}$)
Integra accesibilidad gravitacional relativa con el Índice de Marginación (CONAPO).
$$IPT_{comp, i} = (1 - \text{AccesoRelativo}) \cdot (1 + \text{IM}_i)$$
* **Interpretación:** Penaliza doblemente a zonas desconectadas y vulnerables. Zonas céntricas con alto acceso y baja marginación tienden a 0.

## 4. Implementación Computacional (Avances Fase 1)
La calibración actual se realiza en entorno Jupyter Lab local leyendo la carpeta `backend/gtfs_limpio/`. 
* **Stack:** `pandas` y `numpy` para operaciones vectoriales sobre tiempos de espera y trayecto.
* **Sanity Check:** Las pruebas de consistencia arrojan que las zonas céntricas (Cuauhtémoc) retienen valores mínimos ($IPT_{gap} \approx 0.20$), mientras que los municipios periféricos (Ecatepec) superan el umbral crítico ($IPT_{gap} \ge 1.0$, confirmando la métrica como indicador booleano `True` para pobreza de tiempo).

## 5. Siguientes Pasos
El modelo seleccionado por el equipo será conectado al motor de grafos `NetworkX`. Se iterará sobre la matriz de adyacencia de `stop_times.csv` para sustituir los tiempos observados promediados por rutas más cortas exactas (Dijkstra) hacia nodos primarios de empleo, definiendo así el contrato de datos JSON para la API de FastAPI.
