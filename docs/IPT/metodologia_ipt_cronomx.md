# Reporte Metodológico: Modelado del Índice de Pobreza de Tiempo (IPT)
**Proyecto:** CronoMX / SIGMA
**Autor:** Max
**Estado:** Borrador (Fase de Validación con Municipios Piloto)

## 1. Objetivo
Formular matemáticamente el concepto de "Pobreza de Tiempo Relacionada con el Transporte" (Transport-Related Time Poverty) para la Zona Metropolitana del Valle de México (ZMVM). El índice busca cuantificar cómo la fricción espacial, las ineficiencias de la red de transporte masivo (tiempos de espera y transbordo) y las condiciones sociodemográficas merman sistemáticamente el tiempo libre de los usuarios, restringiendo su desarrollo personal y social.

## 2. Delimitación y Alcance
* **Datos Base:** El modelado asume la disponibilidad y limpieza previa de datos tabulares y espaciales provenientes de archivos GTFS estáticos (CDMX, Mexibús) y bases de afluencia histórica.
* **Fase de Prueba:** La validación empírica inicial se restringirá exclusivamente a **3 municipios piloto** para asegurar la viabilidad del cálculo antes de escalar el algoritmo a toda la ZMVM.
* **Limitación Teórica:** El índice mide una aproximación algorítmica y espacial de la pobreza de tiempo mediante *proxies* de accesibilidad y no mediante encuestas directas de uso del tiempo.

## 3. Marco Metodológico (Candidatos de Ecuación)

Para capturar la multidimensionalidad del problema, se proponen tres aproximaciones matemáticas:

### 3.1. Índice Relativo de Fricción Temporal ($IPT_{rel}$)
Mide la penalización temporal de un trayecto considerando factores de saturación de la infraestructura.
$$IPT_{rel, i} = \frac{t_{obs, i}}{t_{norm}} \cdot \left(1 + \alpha \cdot \frac{A_i}{C_i}\right)$$
* **$t_{obs, i}$**: Tiempo de traslado observado en la red modelada como grafo dirigido.
* **$t_{norm}$**: Umbral paramétrico del tiempo normativo de trayecto.
* **$A_i / C_i$**: Ratio de saturación (Afluencia vs. Capacidad).
* **$\alpha$**: Ponderador de castigo por hacinamiento.

### 3.2. Brecha Decompuesta de Tiempo Libre ($IPT_{gap}$)
Evalúa el porcentaje del "presupuesto temporal de movilidad" que es expropiado por el sistema.
$$IPT_{gap, i} = \frac{\sum_{m \in M} p_m \cdot (t_{ij}^m + t_{espera}^m + t_{transbordo}^m)}{T_{\text{disponible}}}$$
* **$T_{\text{disponible}}$**: Constante que representa el límite máximo de tolerancia de viaje diario.
* **$t_{ij}^m, t_{espera}^m, t_{transbordo}^m$**: Variables de costo extraídas directamente de las frecuencias y recorridos del GTFS.
* **$p_m$**: Distribución probabilística modal de la zona de origen $i$.

### 3.3. Índice Compuesto de Accesibilidad y Vulnerabilidad ($IPT_{comp}$)
Integra un modelo gravitacional con decaimiento espacial y factores sociodemográficos exógenos.
$$IPT_{comp, i} = \left[ 1 - \frac{\sum_j O_j e^{-\beta t_{ij}}}{\max_k (\sum_j O_j e^{-\beta t_{kj}})} \right] \cdot (1 + \text{IM}_i)$$
* **$O_j$**: Vector de oportunidades en nodos destino.
* **$e^{-\beta t_{ij}}$**: Función de impedancia exponencial, donde $\beta$ es el coeficiente de fricción empírica.
* **$\text{IM}_i$**: Índice de Marginación de CONAPO normalizado para la zona de origen.

## 4. Siguientes Pasos y Validación Computacional
La elección definitiva del modelo dependerá de una fase iterativa de prototipado. Se procesarán los grafos de transporte utilizando la matriz de adyacencia de los municipios piloto. Los resultados serán sometidos a evaluación estadística para determinar cuál ecuación presenta mayor varianza explicativa y coherencia geográfica antes de conectarse a la API de producción.
