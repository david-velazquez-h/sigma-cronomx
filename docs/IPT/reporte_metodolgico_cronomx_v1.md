# Reporte Metodológico Actualizado: Modelado de Pobreza de Tiempo Híbrido (Primera Milla + GTFS + CONAPO)

**Proyecto:** CronoMX / SIGMA  
**Fase:** Iteración 4 — Integración Espacial Multimodal y Red de Fricción Real  
**Autor:** Max  
**Estado:** Modelo Integrado en Jupyter Lab (2,312 AGEBs)

---

## 1. Introducción y Reconceptualización del Modelo

La versión inicial del Índice de Pobreza de Tiempo (IPT Compuesto) asumía viajes "puerta a puerta" ideales partiendo directamente desde las estaciones terminales de la red masiva (Metro y Metrobús). Sin embargo, en la Zona Metropolitana del Valle de México (ZMVM), la pobreza de tiempo real se concentra en la "primera milla": el trayecto inicial que realizan los ciudadanos desde sus viviendas en la periferia para conectarse con la red estructurada.

En esta cuarta iteración, el modelo evoluciona de un grafo puro de transporte público masivo a una arquitectura híbrida de movilidad activa y concesionada, evaluada a una resolución microespacial sobre 2,312 Áreas Geoestadísticas Básicas (AGEBs) del INEGI en 10 municipios del Estado de México y 3 alcaldías centrales de la CDMX.

---

## 2. Formulación Oficial

El modelo calcula el Índice Compuesto de Accesibilidad y Vulnerabilidad (IPT Compuesto) multiplicando dos factores principales:
* La pérdida de accesibilidad por tiempo de traslado.
* El nivel de vulnerabilidad social de la zona.

Fórmula conceptual:
IPT Compuesto = (1 - Accesibilidad Relativa) * (1 + Índice de Marginación Normalizado)

### 2.1. Accesibilidad Relativa
Expresa el porcentaje de la ventana de tiempo tolerable (fijada en un umbral máximo de 120 minutos) que el usuario NO pierde viajando. Se calcula restando a 1 la fracción del tiempo total consumido respecto al límite de 120 minutos. 

El Tiempo Total es la suma de todas las etapas de fricción temporal del viaje:
Tiempo Total = Tiempo de Alimentación + Tiempo de Espera en Andén + Tiempo a Bordo (Red GTFS)

* Si el Tiempo Total es mayor o igual a 120 minutos, la Accesibilidad Relativa es 0% (Exclusión Temporal Absoluta).

### 2.2. Normalización Min-Max del Índice de Marginación de CONAPO
Para que el Índice de Marginación original de CONAPO (2020) no distorsione el cálculo, se aplicó una escala de normalización de 0 a 1. 

Esto garantiza que una zona con la máxima marginación observada adquiera un multiplicador de vulnerabilidad social de 2.0, mientras que una zona con mínima marginación conserve un multiplicador de 1.0.

---

## 3. Modelo de Primera Milla Híbrido (Caminata vs. Transporte Concesionado)

Para evitar la anomalía computacional de forzar caminatas irreales de más de 4 horas en la periferia, se implementó una regla de elección de modo alimentador basada en la distancia de la red vial calculada mediante rutas peatonales en OpenStreetMap.

Regla de decisión:
* Distancia menor o igual a 800 metros -> Caminata Peatonal (4.5 km/h)
* Distancia mayor a 800 metros -> Transporte Concesionado (15.0 km/h + Fricción de Abordaje)

### 3.1. Parámetros Operativos de Alimentación:
1. **Velocidad Peatonal:** 1.25 metros por segundo (4.5 km/h).
2. **Velocidad Vehicular Concesionada (Combi / Microbús):** 15.0 km/h. Incorpora las paradas continuas para el ascenso/descenso de pasaje y el tráfico en vialidades locales.
3. **Fricción de Abordaje:** 6.0 minutos. Representa la caminata a la base o esquina de la ruta alimentadora y el tiempo de espera y llenado de la unidad.

### 3.2. Cálculo del Tiempo de Alimentación:
* Si se camina: Distancia en metros / Velocidad peatonal.
* Si se usa combi: (Distancia en metros / Velocidad vehicular) + 6.0 minutos de fricción.

---

## 4. Integración Topológica de la Red Masiva (GTFS)

### 4.1. Tiempo de Espera por Frecuencia de Andén
En lugar de asumir un abordaje instantáneo, se extrajo el "Headway" (intervalo de tiempo entre salidas consecutivas de trenes o autobuses) procesando los horarios oficiales del archivo stop_times.csv.

El tiempo de espera promedio en el andén se calcula como la mitad de ese intervalo entre unidades. 
*(Si los datos en la estación son insuficientes, se aplica un estándar de 4.0 minutos).*

### 4.2. Penalizaciones de Transbordo Georreferenciadas
La correspondencia entre distintas líneas o sistemas masivos se modeló añadiendo conexiones bidireccionales entre estaciones que comparten el mismo nombre. 

* **Regla de Imputación Fija:** Se asignó un costo uniforme de 5.0 minutos por transbordo, simulando la caminata por pasillos internos, escaleras y la espera del cambio de tren.

---

## 5. Delimitación Espacial de AGEBs (INEGI)

El análisis integra la resolución microespacial concatenando las capas vectoriales urbanas del INEGI:
* CDMX — 16 Alcaldías
* Estado de México — Municipios Conurbados

### 5.1. Claves INEGI Integradas:
Para identificar de manera unívoca los barrios pertenecientes a las zonas de estudio, se construyó una clave unificada combinando el código de entidad y municipio:

| Clave | Municipio / Alcaldía | Rol en el Modelo |
| :---: | :--- | :--- |
| 15033 | Ecatepec de Morelos | Origen Periférico |
| 15058 | Nezahualcóyotl | Origen Periférico |
| 15031 | Chimalhuacán | Origen Periférico |
| 15081 | Tecámac | Origen Periférico |
| 15057 | Naucalpan de Juárez | Origen Periférico |
| 15104 | Tlalnepantla de Baz | Origen Periférico |
| 15070 | La Paz | Origen Periférico |
| 15025 | Chalco | Origen Periférico |
| 15013 | Atizapán de Zaragoza | Origen Periférico |
| 15121 | Cuautitlán Izcalli | Origen Periférico |
| 09015 | Cuauhtémoc | Destino (Centro CDMX) |
| 09016 | Miguel Hidalgo | Destino (Reforma / Polanco) |
| 09010 | Álvaro Obregón | Destino (Santa Fe / Observatorio) |

### 5.2. Centroides y Proyección Espacial
Los polígonos habitacionales fueron procesados para calcular el centroide geométrico exacto de cada comunidad en metros, y luego convertidos a coordenadas GPS estándar (Latitud/Longitud) para cruzar las rutas con el mapa de calles.

---

## 6. Resultados del Modelo Híbrido (Ranking Ajustado de Pobreza de Tiempo)

Procesando los 2,312 AGEBs urbanos con el modelo de alimentación concesionada, frecuencias de andén y red masiva, se obtuvo la siguiente matriz de resultados promediada a nivel municipal:

| Municipio / Alcaldía | Alimentación Combi | Espera Andén | Viaje GTFS | Tiempo Total | IM Norm | Accesibilidad Rel. | IPT Compuesto |
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

1. **Dominación de la Primera Milla:** En los municipios más alejados (Tecámac, Atizapán, Nezahualcóyotl), el tiempo invertido a bordo de la combi o microbús representa entre el 60% y el 80% del tiempo total de traslado.
2. **Colapso de Accesibilidad:** Tecámac y Chalco superan formalmente el umbral de las 2 horas (136.4 minutos y 124.0 minutos), anulando completamente su accesibilidad laboral (0.0%) e impulsando su índice de pobreza de tiempo cerca del máximo teórico.
3. **Sensibilidad del Indicador:** La integración de la normalización del Índice de Marginación de CONAPO permite diferenciar municipios con tiempos similares pero vulnerabilidades sociales opuestas, cumpliendo con el objetivo central del proyecto CronoMX de visibilizar la equidad espacial en la ZMVM.