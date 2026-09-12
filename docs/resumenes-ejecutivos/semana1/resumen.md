# Resumen Ejecutivo — Investigación Semana 1
### CronoMX / SIGMA

**Preparado por:** Angel David Velazquez Herrera
**Para:** Equipo de trabajo

---

## 1. Magnitud del problema (el dato-gancho)

Un estudio de ONU-Habitat encontró que cruzar la Zona Metropolitana del Valle de México (ZMVM) en transporte público toma en promedio entre **5h21min y 5h49min**, dependiendo de si el trayecto es de este a oeste o de norte a sur. El mismo recorrido en vehículo particular toma **entre 2.7 y 2.8 horas**, es decir, poco más de la mitad. Este es el dato que ya usamos como gancho narrativo del proyecto (fuente: ONU-Habitat México).

## 2. Marco conceptual: "pobreza de tiempo"

El concepto que sostiene todo el proyecto no es solo "el transporte tarda mucho", es que las largas jornadas de traslado **reducen sistemáticamente el tiempo disponible para descansar, convivir en familia y cuidar la salud**, lo cual profundiza desigualdades sociales existentes en vez de ser un problema neutral que afecta a todos por igual.

Este concepto conecta con literatura internacional más amplia sobre **exclusión social relacionada con transporte** (Preston y Raje, 2007; Banister, 2002), que documenta cómo la falta de acceso eficiente a transporte no es solo un problema de comodidad, sino un mecanismo que perpetúa exclusión económica y social, especialmente para poblaciones de bajos ingresos que ya son las que más dependen de transporte público de baja capacidad.

## 3. El problema ya está parcialmente reconocido oficialmente

El diagnóstico técnico de movilidad de SEMOVI (CDMX) reconoce que la falta de integración del sistema de transporte genera desigualdad en el acceso a la ciudad: entre más lejos vive una persona, más viajes multimodales (transbordos) necesita para llegar a su destino. **Este mismo diagnóstico ya cruza el "Grado de Marginación Urbana" (GMU) con la infraestructura de transporte público masivo**, es decir, el enfoque de cruzar nuestro índice con datos de marginación (CONAPO) no es una idea nueva que estemos forzando, es una extensión de un cruce que la propia SEMOVI ya reconoce como relevante, pero que nosotros podemos hacer más granular, actualizable y con foco en tiempo (no solo en infraestructura).

## 4. Precedentes metodológicos para el índice (para Max)

Encontré tres familias de metodología usadas en la literatura para medir accesibilidad al transporte, de menor a mayor sofisticación:

1. **Índice simple de cobertura**: población servida por transporte público ÷ población total. Muy simple, pero no captura duración de trayecto, probablemente insuficiente para lo que queremos medir.
2. **Distancia de corte / accesibilidad peatonal**: mide qué proporción de la población está a una distancia caminable (ej. 300m) de una parada. Útil como componente parcial del índice, pero tampoco captura el trayecto completo.
3. **Modelo gravitacional / costo generalizado de viaje**: un estudio mexicano publicado en SciELO sobre accesibilidad en periferias metropolitanas usa este enfoque, y encuentra que refleja mejor la realidad de zonas periféricas, mostrando una relación directa entre accesibilidad e ingreso promedio de la población. **Esta es la familia metodológica más cercana a lo que necesitamos**, porque ya conecta accesibilidad con nivel socioeconómico, justo la correlación que queremos explorar con el cruce de marginación.

**Recomendación para Max:** partir de la lógica de "costo generalizado de viaje" (que incluye tiempo de espera, tiempo en vehículo, tiempo de transbordo, y posiblemente costo monetario) en vez del índice simple de cobertura, y usarlo como base para adaptar la fórmula del índice de "pobreza de tiempo".

## 5. Fuentes de datos existentes relevantes

- **Encuesta Origen-Destino (EOD)** del INEGI (última edición 2017), es la fuente que usa la mayoría de estudios académicos sobre movilidad en la ZMVM, aunque se actualiza con poca frecuencia. Útil como referencia/validación, no como fuente principal en tiempo real.
- **Diagnóstico Técnico de Movilidad (PIM)** de SEMOVI, ya incluye el cruce de Grado de Marginación Urbana con infraestructura de transporte; vale la pena revisarlo a fondo como referencia metodológica y para no duplicar lo que ya existe.

## 6. Preguntas abiertas para discutir el viernes

1. ¿Adoptamos la lógica de "costo generalizado de viaje" como base matemática del índice, o Max prefiere una fórmula más simple para la v1 y sofisticarla después?
2. ¿Qué tan disponible está el Grado de Marginación Urbana (GMU) de SEMOVI a nivel de municipio/colonia, y podemos cruzarlo directamente o necesitamos usar el índice de marginación de CONAPO como alternativa?
3. ¿Usamos la Encuesta Origen-Destino 2017 como validación de nuestros resultados calculados con GTFS, aunque esté desactualizada?

---

*Documento preparado como parte de las tareas de la Semana 1 del cronograma del proyecto.*
