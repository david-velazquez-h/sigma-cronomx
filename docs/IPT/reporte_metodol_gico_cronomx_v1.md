# Reporte Metodológico Actualizado: Modelado de Pobreza de Tiempo Híbrido (Primera Milla + GTFS + CONAPO)

**Proyecto:** CronoMX / SIGMA  
**Fase:** Iteración 4 — Integración Espacial Multimodal y Red de Fricción Real  
**Autor:** Max  
**Estado:** Modelo Integrado en Jupyter Lab (2,312 AGEBs)

---

## 1. Introducción y Reconceptualización del Modelo

La versión inicial del Índice de Pobreza de Tiempo ($IPT_{comp}$) asumía viajes "puerta a puerta" ideales partiendo directamente desde las estaciones terminales de la red masiva (Metro y Metrobús). Sin embargo, en la Zona Metropolitana del Valle de México (ZMVM), la **pobreza de tiempo real** se concentra en la "primera milla": el trayecto inicial que realizan los ciudadanos desde sus viviendas en la periferia para conectarse con la red estructurada.

En esta cuarta iteración, el modelo evoluciona de un grafo puro de transporte público masivo a una **arquitectura híbrida de movilidad activa y concesionada**, evaluada a una resolución microespacial sobre **2,312 Áreas Geoestadísticas Básicas (AGEBs)** del INEGI en 10 municipios del Estado de México y 3 alcaldías centrales de la CDMX.

---

## 2. Formulación Matemática Oficial

El modelo calcula el **Índice Compuesto de Accesibilidad y Vulnerabilidad ($IPT_{comp}$)** mediante la ecuación:

$$IPT_{comp, i} = (1 - Acc_{Relativa, i}) \times (1 + IM_{Norm, i})$$

### 2.1. Accesibilidad Relativa ($Acc_{Relativa}$)
Expresa el porcentaje de la ventana de tiempo tolerable (fijada en un umbral de decaimiento de 120 minutos) que el usuario **no** pierde viajando:

$$Acc_{Relativa, i} = \max\left(0, \, 1 - \frac{T_{Total, i}}{120.0}\right)$$

Donde $T_{Total, i}$ es la suma de todas las etapas de fricción temporal del viaje completo desde el AGEB $i$:

$$T_{Total, i} = t_{\text{alimentación, } i} + t_{\text{espera\_andén, } i} + t_{\text{bordo\_GTFS, } i}$$

*   Si $T_{Total, i} \ge 120 \text{ min}$, $Acc_{Relativa, i} = 0.0$ (Exclusión Temporal Absoluta).

### 2.2. Normalización Min-Max del Índice de Marginación de CONAPO ($IM_{Norm}$)
Para que el Índice de Marginación ($IM_{raw}$) de CONAPO (2020) sea matemáticamente compatible y no distorsione la ponderación del $IPT_{comp}$, se aplicó una escala de normalización $0 \to 1$:

$$IM_{Norm, i} = \frac{IM_{raw, i} - \min(IM_{raw})}{\max(IM_{raw}) - \min(IM_{raw})}$$

Esto garantiza que una zona con la máxima marginación observada adquiera un multiplicador de vulnerabilidad social de $2.0$, mientras que una zona con mínima marginación conserve un multiplicador de $1.0$.

---

## 3. Modelo de Primera Milla Híbrido (Caminata vs. Transporte Concesionado)

Para evitar la anomalía computacional de forzar caminatas irreales de más de 4 horas en la periferia, se implementó una **regla de elección de modo alimentador** basada en la distancia de red vial ($d_m$) calculada mediante Dijkstra peatonal en OpenStreetMap (`OSMnx`):

```
                        ┌─── d_m <= 800 m  ───> Caminata Peatonal (4.5 km/h)
Distancia AGEB -> Nodo ─┤
                        └─── d_m > 800 m   ───> Transporte Concesionado (15.0 km/h + Fricción Abordaje)
```

### 3.1. Parámetros Operativos de Alimentación:
1.  **Velocidad Peatonal:** $v_{\text{peatonal}} = 1.25 \text{ m/s} \quad (4.5 \text{ km/h})$.
2.  **Velocidad Vehicular Concesionada (Combi / Microbús):** $v_{\text{combi}} = 15.0 \text{ km/h} \quad (4.167 \text{ m/s})$. Incorpora las paradas continuas para el ascenso/descenso de pasaje y el tráfico en vialidades locales.
3.  **Fricción de Abordaje:** $\text{Fricción}_{\text{combi}} = 6.0 \text{ minutos}$. Representa la caminata a la base/esquina de la ruta alimentadora y el tiempo de espera/llenado de la unidad.

### 3.2. Ecuación del Tiempo de Alimentación ($t_{\text{alimentación}}$):
$$t_{\text{alimentación, } i} = \begin{cases} 
\dfrac{d_m}{1.25 \times 60} & \text{si } d_m \le 800\text{ m} \\[10pt]
\left(\dfrac{d_m}{4.167 \times 60}\right) + 6.0 & \text{si } d_m > 800\text{ m (o red desconectada)}
\end{cases}$$

---

## 4. Integración Topológica de la Red Masiva (GTFS)

### 4.1. Tiempo de Espera por Frecuencia de Andén ($t_{\text{espera\_andén}}$)
En lugar de asumir un abordaje instantáneo, se extrajo el *headway* (intervalo entre salidas consecutivas de unidades) procesando el archivo `stop_times.csv`:

$$\text{Headway}_k = \Delta t_{\text{llegada, } k} = t_{\text{llegada, } k+1} - t_{\text{llegada, } k}$$

El tiempo de espera esperado en el andén se calcula como la mitad del intervalo medio:

$$t_{\text{espera\_andén}} = \frac{\overline{\text{Headway}}}{2}$$

*(Si los datos en la estación son insuficientes, se aplica un estándar de $4.0\text{ min}$).*

### 4.2. Penalizaciones de Transbordo Georreferenciadas
La correspondencia entre distintas líneas o sistemas masivos se modeló en el grafo dirigido `nx.DiGraph()` añadiendo aristas bidireccionales entre nodos que comparten el mismo `stop_name`. 

*   **Regla de Imputación Fija:** Se asignó un costo uniforme de **5.0 minutos** por transbordo, simulando la caminata por pasillos internos, escaleras y la espera del cambio de tren/unidad.

---

## 5. Delimitación Espacial de AGEBs (INEGI)

El análisis integra la resolución microespacial concatenando las capas vectoriales urbanas del INEGI:
*   `09a.shp` (CDMX — 16 Alcaldías)
*   `15a.shp` (Estado de México — Municipios Conurbados)

### 5.1. Claves INEGI Integradas (`CVE_ENT` + `CVE_MUN`):
Para identificar de manera unívoca los barrios pertenecientes a las zonas de estudio, se construyó una clave unificada de 5 dígitos:

| Clave | Municipio / Alcaldía | Rol en el Modelo |
| :---: | :--- | :--- |
| `15033` | Ecatepec de Morelos | Origen Periférico |
| `15058` | Nezahualcóyotl | Origen Periférico |
| `15031` | Chimalhuacán | Origen Periférico |
| `15081` | Tecámac | Origen Periférico |
| `15057` | Naucalpan de Juárez | Origen Periférico |
| `15104` | Tlalnepantla de Baz | Origen Periférico |
| `15070` | La Paz | Origen Periférico |
| `15025` | Chalco | Origen Periférico |
| `15013` | Atizapán de Zaragoza | Origen Periférico |
| `15121` | Cuautitlán Izcalli | Origen Periférico |
| `09015` | Cuauhtémoc | Destino (Centro CDMX) |
| `09016` | Miguel Hidalgo | Destino (Reforma / Polanco) |
| `09010` | Álvaro Obregón | Destino (Santa Fe / Observatorio) |

### 5.2. Centroides y Proyección Espacial
Los polígonos habitacionales fueron proyectados a coordenadas métricas planas (**UTM Zona 14N / EPSG:32614**) para calcular el centroide geométrico exacto de cada comunidad, y re-proyectados a **WGS84 (EPSG:4326)** para el cruzamiento de rutas con OpenStreetMap.

---

## 6. Resultados del Modelo Híbrido (Ranking Ajustado de Pobreza de Tiempo)

Procesando los 2,312 AGEBs urbanos con el modelo de alimentación concesionada, frecuencias de andén y red GTFS a bordo, se obtuvo la siguiente matriz de resultados promediada a nivel municipal:

| Municipio / Alcaldía | Alimentación / Combi ($t_{\text{alim}}$) | Espera Andén ($t_{\text{esp}}$) | Viaje GTFS ($t_{\text{GTFS}}$) | Tiempo Total Real ($T_{\text{Total}}$) | $IM_{\text{Norm}}$ | $Acc_{\text{Relativa}}$ | **$IPT_{\text{comp}}$ Final** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tecámac** | 109.0 min | 4.0 min | 23.4 min | **136.4 min** | 0.926 | **0.0%** | **1.926** |
| **Nezahualcóyotl** | 79.8 min | 5.2 min | 30.2 min | **115.2 min** | 0.864 | **4.0%** | **1.789** |
| **Chalco** | 61.5 min | 12.2 min | 50.3 min | **124.0 min** | 0.724 | **0.0%** | **1.724** |
| **Cuautitlán Izcalli** | 71.4 min | 13.8 min | 14.2 min | **99.3 min** | 0.972 | **17.3%** | **1.632** |
| **Atizapán de Zaragoza** | 80.2 min | 4.0 min | 15.9 min | **100.2 min** | 0.920 | **16.5%** | **1.603** |
| **Tlalnepantla de Baz** | 65.6 min | 13.8 min | 14.2 min | **93.5 min** | 0.918 | **22.1%** | **1.495** |
| **Chimalhuacán** | 57.7 min | 12.2 min | 25.8 min | **95.7 min** | 0.721 | **20.2%** | **1.373** |
| **Ecatepec de Morelos** | 36.3 min | 4.0 min | 44.2 min | **84.4 min** | 0.872 | **29.6%** | **1.317** |
| **La Paz** | 22.0 min | 12.2 min | 50.3 min | **84.5 min** | 0.688 | **29.6%** | **1.189** |
| **Naucalpan de Juárez** | 32.3 min | 4.0 min | 15.9 min | **52.2 min** | 0.872 | **56.5%** | **0.815** |

---

## 7. Discusión de Hallazgos y Conclusión

1.  **Dominación de la Primera Milla:** En los municipios más alejados (Tecámac, Atizapán, Nezahualcóyotl), el tiempo invertido a bordo de la combi/microbús representa entre el **60% y el 80% del tiempo total de traslado**.
2.  **Colapso de Accesibilidad:** Tecámac y Chalco superan formalmente el umbral de las 2 horas ($136.4\text{ min}$ y $124.0\text{ min}$), anulando completamente su accesibilidad laboral ($Acc_{\text{Relativa}} = 0.0\%$) e impulsando su índice de pobreza de tiempo cerca del máximo teórico ($IPT_{\text{comp}} > 1.7$).
3.  **Sensibilidad del Indicador:** La integración de la normalización del $IM$ de CONAPO permite diferenciar municipios con tiempos similares pero vulnerabilidades sociales opuestas, cumpliendo con el objetivo central del proyecto CronoMX de visibilizar la equidad espacial en la ZMVM.
```

eof

---

### Resumen de los cambios integrados en el documento:
- **Ecuaciones y Parámetros Unificados:** Se documentó la velocidad de caminata a $4.5\text{ km/h}$, el transporte concesionado a $15\text{ km/h}$ y la fricción de abordaje de $6\text{ min}$.
- **Normalización CONAPO:** Se incluyó la fórmula Min-Max explicada paso a paso.
- **Topología e Imputación de Transbordos:** Se especificaron los $5\text{ min}$ entre andenes y el cálculo de *headways* mediante `stop_times.csv`.
- **AGEBs y Claves INEGI:** Se detalló el uso de los 2,312 polígonos (`09a.shp` + `15a.shp`) y las claves compuestas (`CVE_ENT` + `CVE_MUN`).
- **Resultados Consolidados:** Se transcribió la tabla final del ranking ajustado.

El reporte metodológico está guardado y listo en el panel derecho. ¿Te gustaría trabajar en algún aspecto adicional de la visualización o exportación de datos?