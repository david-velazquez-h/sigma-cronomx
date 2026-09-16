# Candidatos de Fórmula para el Índice de Pobreza de Tiempo (IPT) - CronoMX

**Autor:** Max
**Objetivo:** Proponer formulaciones matemáticas para evaluar la "pobreza de tiempo" en la movilidad urbana de la ZMVM, integrando variables de transporte público (GTFS) y datos sociodemográficos. Estas fórmulas serán sometidas a pruebas con los datos de 3 municipios piloto.

---

## 1. Índice Relativo de Fricción Temporal ($IPT_{rel}$)
Este enfoque compara el tiempo de viaje observado ($t_{obs}$) hacia nodos principales frente a un tiempo normativo deseable ($t_{norm}$), castigando el resultado en función de la saturación del sistema de transporte.

**Fórmula:**
$$IPT_{rel, i} = \frac{t_{obs, i}}{t_{norm}} \cdot \left(1 + \alpha \cdot \frac{A_i}{C_i}\right)$$

**Variables:**
* $t_{obs, i}$: Tiempo promedio ponderado de traslado desde el municipio $i$ a nodos de empleo/servicios (calculado vía NetworkX).
* $t_{norm}$: Tiempo máximo deseable de traslado (ej. 45-60 minutos).
* $A_i / C_i$: Factor de saturación temporal (Afluencia histórica $A_i$ sobre Capacidad del sistema $C_i$).
* $\alpha$: Parámetro de ponderación ($0 < \alpha \le 1$).

---

## 2. Brecha Decompuesta de Tiempo Libre ($IPT_{gap}$)
Mide el porcentaje del "presupuesto de tiempo diario disponible" que es absorbido por las ineficiencias de la red de transporte público. 

**Fórmula:**
$$IPT_{gap, i} = \frac{\sum_{m \in M} p_m \cdot (t_{ij}^m + t_{espera}^m + t_{transbordo}^m)}{T_{\text{disponible}}}$$

**Variables:**
* $t_{ij}^m$: Tiempo neto en trayecto en el modo $m$ (Metro, Mexibús, etc.).
* $t_{espera}^m, t_{transbordo}^m$: Tiempos muertos extraídos de las frecuencias estáticas del GTFS.
* $p_m$: Proporción de uso por modo de transporte en la zona $i$.
* $T_{\text{disponible}}$: Tiempo diario máximo asignable a movilidad antes de impactar el bienestar (ej. 3 horas).

---

## 3. Índice Compuesto de Accesibilidad Específica y Vulnerabilidad ($IPT_{comp}$)
Combina un modelo gravitacional de accesibilidad con la vulnerabilidad socioeconómica, usando la tasa de marginación del CONAPO para ponderar la severidad del aislamiento.

**Fórmula:**
$$IPT_{comp, i} = \left[ 1 - \frac{\sum_j O_j e^{-\beta t_{ij}}}{\max_k (\sum_j O_j e^{-\beta t_{kj}})} \right] \cdot (1 + \text{IM}_i)$$

**Variables:**
* $O_j$: Oportunidades disponibles en la zona $j$.
* $e^{-\beta t_{ij}}$: Función de decaimiento espacial basada en el tiempo de viaje $t_{ij}$ sobre la red GTFS.
* $\text{IM}_i$: Índice de Marginación normalizado $[0,1]$ del municipio $i$ (datos CONAPO).

---

## Próximos pasos
El siguiente paso es procesar el archivo GTFS limpio del backend a través de scripts de Python/Jupyter y probar estas fórmulas evaluando exclusivamente los 3 municipios piloto para realizar un sanity check de los resultados.
