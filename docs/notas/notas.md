# Notas y bitácora de decisiones — CronoMX / SIGMA

Este archivo es una bitácora rápida, no un reporte formal. La idea es anotar en 3-5 líneas cualquier decisión importante o problema resuelto, el mismo día que pasa para no tener que reconstruirlo de memoria más adelante.

**Qué sí anotar aquí:**
- Una decisión técnica o de diseño que el equipo tomó y por qué (para no volver a discutirla desde cero).
- Un bug o problema que costó trabajo resolver, y cómo se resolvió.
- Cualquier cosa que "todos deberían saber" pero que no vive en ningún otro documento.

**Qué NO anotar aquí:**
- Documentación formal de cómo usar el código (eso va en el README de cada carpeta, `frontend/README.md`, `backend/README.md`, etc.).
- La narrativa para difusión/investigadores (eso ya vive en `proyecto-pobreza-de-tiempo.md`).

---

## Formato de cada entrada

```
### AAAA-MM-DD — Quién
Qué se decidió/resolvió, en 3-5 líneas. Por qué, si no es obvio.
```

---

### 2026-09-13 — David

Se corrigió un bug donde el Hero se veía "dividido en 3 columnas" con márgenes oscuros a los lados. Causa: el boilerplate default de Vite en `src/index.css` traía `#root { max-width: 1280px; margin: 0 auto; }` y `body { display: flex; place-items: center; }`, lo cual centraba todo en una columna angosta en vez de pantalla completa. Se limpió `index.css` quitando esas reglas.

También se recortó el logo `LOGO_1_CRONO-MX.png` y se camió el nombre a `logo-crono-sin-f.png` porque el archivo original traía mucho espacio negro alrededor del texto (pensado para verse como imagen independiente, no como asset de navbar), lo que lo hacía ilegible al usarlo en tamaño pequeño.

---

### 2026-09-18 — David

Se investigaron los GTFS iniciales sobre prácticamete toda la SEMOVI de la CDMX, se limpiaron los archivos GTFS para qu solo quedaran los del metro y metrobús para esta primer versión de CronoMX, y se eliminó `afluenciametrobus_simple_limpia.csv` archivo que era innecesario para esta primer versión.

---

### 2026-09-20 — Max

Se configuró el entorno local en Jupyter Lab dentro de iCloud y se subió el archivo `analisis_piloto_ipt.ipynb` a la carpeta `docs/IPT`. Se implementó la validación piloto de los tres modelos matemáticos de Pobreza de Tiempo ($IPT_{gap}$, $IPT_{rel}$ y $IPT_{comp}$) para los municipios de prueba, documentando la metodología y los criterios de diagnóstico para la revisión del equipo.

---

### 2026-09-22 — Max

Se actualizó la documentación del proyecto en la carpeta `docs/IPT` incorporando dos entregables clave: el archivo `actualizacion_metodologia.md` con el marco teórico y la justificación de la fórmula compuesta ($IPT_{comp}$), y `modelo_datos_reales_ipt.md` (o el respaldo analítico del modelo) junto con el grafo visual generado (`grafo_red_cronomx.png`). Se documentó la integración de la base de datos GTFS real mediante el motor de grafos en NetworkX y el algoritmo de Dijkstra para evaluar la accesibilidad multi-destino desde las zonas periféricas hacia los polos de empleo de la ZMVM.

---
### 2026-09-25 — David
 
Se descubrió que Chalco en realidad **no está servido por ninguna línea de Mexibús**, la Línea 3 llega hasta Chimalhuacán, municipio vecino pero distinto. Chalco tiene su propio sistema, el **Trolebús Chalco-Santa Marta** (100% eléctrico, recién inaugurado, 18.5 km, 13 estaciones), operado eventualmente por STE.
 
Se probó si Apimetro ya tenía este corredor cargado bajo su sistema `TROLE` (795 estaciones de trolebús en total), **no aparece ninguna estación de Chalco/Santa Marta**, probablemente por ser un corredor demasiado reciente para estar ya integrado.
 
**Decisión final de municipios piloto para la v1:** Chalco queda fuera por falta de datos. El piloto se conforma con **Ecatepec de Morelos, Nezahualcóyotl, Chimalhuacán y Tecámac** (los 4 ya tienen cobertura real de Mexibús vía OSM/Overpass), con Tlalnepantla como quinto municipio posible, pendiente de confirmar cobertura de Metro/Metrobús antes de agregarlo.
 
El corredor Chalco-Santa Marta queda anotado como candidato fuerte para v2 es un caso de uso perfecto para la narrativa de electromovilidad (Electro Hackatón, 8 de octubre), aunque no tengamos los datos listos todavía.
 
### 2026-10-17 — David (de datos de ejemplo a datos reales)
 
**Equipo.** Max pidió que David asumiera por esta vez el cálculo del índice. Se decidió no entrar al Electro Hackatón: exigía equipos de exactamente 5 personas y asistencia individual obligatoria a una capacitación a la que Max no podía conectarse.
 
**Script único.** Se creó `backend/sigma_indice.py`: construye el grafo del GTFS, calcula tiempos a 3 polos de empleo, aplica Mexibús, acceso y espera, cruza con CONAPO y escribe `frontend/public/data/indice.json`. Los tiempos de Ecatepec y Neza coincidieron con la matriz previa de Max (44.2 y 30.2 min) antes de añadir acceso y espera.
 
**Mexibús.** No hay GTFS público, así que para Chimalhuacán y Tecámac se suma un tramo estimado (distancia ÷ 20 km/h + 5 min de transbordo). Los 20 km/h son un supuesto, no una medición. Sin este parche ambos municipios salían con mejor acceso que Ecatepec, lo cual era un artefacto.
 
**Marginación (hallazgo importante).** En el IM 2020 de CONAPO un valor alto significa *menos* marginación. Los IM que se usaban antes (0.75, 0.85…) eran estimaciones sin respaldo y estaban en el sentido contrario. Los 4 municipios piloto son grado "Muy bajo" a nivel municipal, con valores muy cercanos. Se invierte y normaliza min-max sobre los 125 municipios del Edomex. Consecuencia: el IM pesa poco y el índice depende sobre todo del tiempo de viaje. Limitación: el promedio municipal oculta desigualdad interna; una v2 debería usar AGEB o localidad.
 
**Acceso y espera.** El primer cálculo (Ecatepec ≈ 44 min al Centro) era irreal porque arrancaba en la estación Ciudad Azteca, ya en el límite con la CDMX. Se añadió el tramo del centro del municipio a la estación (distancia × 1.3 a 15 km/h) y 7 min de espera. El resultado se presenta como **tiempo mínimo estimado** (piso, no techo): no incluye tráfico, obras, manifestaciones, saturación ni combis.
 
**Validación.** Comparación manual contra Google Maps (transporte público, lunes 07:00, mismo origen y destino). Resultado cualitativo: SIGMA queda a pocos minutos de Maps. Tabla en `docs/IPT/validacion.csv`. Pendiente: anotar aquí los números finales.
 
**Colores del mapa.** Los umbrales ahora usan el IPT directo: < 0.3 bajo, 0.3–0.5 moderado, 0.5–0.8 alto, ≥ 0.8 "exclusión severa" (umbral definido por Max).
 
**Alcance.** Buscador por municipio dentro del comparador (catálogo de los 125 municipios del Edomex; solo 4 con cálculo). Se decidió dejar fuera de la v1 un top de propuestas de nuevas rutas y un simulador: requieren backend, moderación y criterio urbanístico que el equipo no tiene; lo que sí es simulable (agregar una conexión al grafo y medir minutos ahorrados) queda como idea para v2.

---


*Agreguen su entrada arriba de esta línea, con la fecha más reciente al final del archivo (orden cronológico).*
