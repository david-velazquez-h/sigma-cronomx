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

2026-09-20 — Max

Se configuró el entorno local en Jupyter Lab dentro de iCloud y se subió el archivo `analisis_piloto_ipt.ipynb` a la carpeta `docs/IPT`. Se implementó la validación piloto de los tres modelos matemáticos de Pobreza de Tiempo ($IPT_{gap}$, $IPT_{rel}$ y $IPT_{comp}$) para los municipios de prueba, documentando la metodología y los criterios de diagnóstico para la revisión del equipo.

*Agreguen su entrada arriba de esta línea, con la fecha más reciente al final del archivo (orden cronológico).*
