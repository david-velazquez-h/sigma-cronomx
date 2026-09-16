# Casos de Uso y Ejemplos de Cálculo: Fórmulas IPT
**Proyecto:** CronoMX / SIGMA
**Autor:** Max

Este documento presenta ejemplos numéricos hipotéticos para demostrar el comportamiento de los tres candidatos de fórmula del Índice de Pobreza de Tiempo (IPT) bajo diferentes condiciones de movilidad.

---

## 1. Índice Relativo de Fricción Temporal ($IPT_{rel}$)
**Fórmula:** $IPT_{rel, i} = \frac{t_{obs, i}}{t_{norm}} \cdot \left(1 + \alpha \cdot \frac{A_i}{C_i}\right)$

**Ejemplo A: Zona Periférica con Alta Saturación (ej. Ecatepec a CDMX)**
* $t_{obs} = 90$ min (tiempo observado).
* $t_{norm} = 45$ min (tiempo normativo esperado).
* $A_i/C_i = 1.2$ (sistema operando al 120% de capacidad).
* $\alpha = 0.5$ (factor de sensibilidad).
* **Cálculo:** $(90 / 45) \cdot (1 + (0.5 \cdot 1.2)) = 2 \cdot 1.6 = \mathbf{3.2}$
* **Interpretación:** Fricción temporal severa; el viaje toma el doble de lo deseable y se agrava por el hacinamiento.

**Ejemplo B: Zona Céntrica (ej. Benito Juárez a Cuauhtémoc)**
* $t_{obs} = 30$ min, $t_{norm} = 45$ min.
* $A_i/C_i = 0.8$ (sistema al 80% de capacidad).
* $\alpha = 0.5$.
* **Cálculo:** $(30 / 45) \cdot (1 + (0.5 \cdot 0.8)) = 0.66 \cdot 1.4 = \mathbf{0.93}$
* **Interpretación:** Condiciones óptimas; el usuario viaja por debajo del tiempo normativo sin penalización crítica de saturación.

---

## 2. Brecha Decompuesta de Tiempo Libre ($IPT_{gap}$)
**Fórmula:** $IPT_{gap, i} = \frac{\sum (t_{ij} + t_{espera} + t_{transbordo})}{T_{\text{disponible}}}$

**Ejemplo A: Viaje Multimodal Ineficiente**
* $T_{\text{disponible}} = 120$ min (presupuesto diario de movilidad saludable).
* Tiempos GTFS ida y vuelta: $t_{ij} = 90$ min, $t_{espera} = 30$ min, $t_{transbordo} = 20$ min.
* **Cálculo:** $(90 + 30 + 20) / 120 = 140 / 120 = \mathbf{1.16}$
* **Interpretación:** El usuario gasta el 116% de su tiempo disponible, invadiendo su tiempo libre/descanso en un 16% (Pobreza de tiempo inducida).

**Ejemplo B: Viaje Directo Eficiente**
* $T_{\text{disponible}} = 120$ min.
* Tiempos GTFS ida y vuelta: $t_{ij} = 50$ min, $t_{espera} = 10$ min, $t_{transbordo} = 0$ min.
* **Cálculo:** $(50 + 10 + 0) / 120 = 60 / 120 = \mathbf{0.50}$
* **Interpretación:** El usuario solo consume el 50% de su margen, manteniendo intacto su tiempo reproductivo y de ocio.

---

## 3. Índice Compuesto de Accesibilidad y Vulnerabilidad ($IPT_{comp}$)
**Fórmula:** $IPT_{comp, i} = \left[ 1 - \frac{A_i}{A_{max}} \right] \cdot (1 + \text{IM}_i)$ *(Donde A es la suma gravitacional)*

**Ejemplo A: Asentamiento Marginado**
* $A_i / A_{max} = 0.2$ (Solo accede al 20% de las oportunidades en un radio de tiempo dado, comparado con el mejor municipio).
* $\text{IM}_i = 0.6$ (Índice de Marginación CONAPO moderado-alto).
* **Cálculo:** $[1 - 0.2] \cdot (1 + 0.6) = 0.8 \cdot 1.6 = \mathbf{1.28}$
* **Interpretación:** Alta exclusión espacial exacerbada por el rezago socioeconómico.

**Ejemplo B: Nodo Central de Empleo**
* $A_i / A_{max} = 0.9$ (Acceso al 90% de las oportunidades relativas).
* $\text{IM}_i = 0.1$ (Baja marginación).
* **Cálculo:** $[1 - 0.9] \cdot (1 + 0.1) = 0.1 \cdot 1.1 = \mathbf{0.11}$
* **Interpretación:** Alta accesibilidad y entorno resiliente.
