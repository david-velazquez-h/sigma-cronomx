# CronoMX
### SIGMA — Sistema de Índices Georreferenciados de Movilidad y Accesibilidad

**Cuantificando el costo de tiempo del transporte público entre el Estado de México y la CDMX.**

---

## El problema

Cruzar la Zona Metropolitana del Valle de México en transporte público toma en promedio entre **5h21min y 5h49min**, frente a 2.7–2.8 horas en auto particular (ONU-Habitat). Ese costo recae de forma desproporcionada en los municipios conurbados del Estado de México, cuyos habitantes cruzan a diario para trabajar o estudiar en la CDMX.

En estudios urbanos se llama **pobreza de tiempo**: el tiempo de vida, descanso y convivencia que se pierde de forma sistemática por un transporte lento, y que hoy casi no se cuantifica ni se publica de forma abierta y reproducible.

## Qué hace CronoMX

- **Mapa** con el índice de pobreza de tiempo (IPT) de los municipios piloto.
- **Comparador** con buscador de municipio: tiempo mínimo estimado en transporte público a tres polos de empleo (Centro, Reforma/Polanco, Santa Fe).
- **Metodología abierta**: fórmula, supuestos y limitaciones documentados para que cualquiera pueda auditarlos.

CronoMX no pretende "arreglar" el transporte público: busca hacer visible y medible un costo social que hoy es difuso.

## Estado del proyecto: v1 piloto

Alcance actual: **Ecatepec de Morelos, Nezahualcóyotl, Chimalhuacán y Tecámac**, contra tres destinos en la CDMX.

Lo que el índice **sí** mide: tiempo programado mínimo en Metro y Metrobús (GTFS), tramo estimado de acceso a la estación, tramo estimado de Mexibús, y marginación municipal de CONAPO.

Lo que **no** mide todavía: tráfico, obras, manifestaciones, saturación, combis y colectivos, ni tiempos en auto. Es un **piso, no un techo**. Detalle completo en la página de Metodología del sitio y en [`docs/notas.md`](./docs/notas.md).

## Cómo se calcula

```
IPT = (1 − Acc_Relativa) × (1 + IM)
Acc_Relativa = máx(0, 1 − t / 120)
```

`t` es el tiempo mínimo (min) al polo de empleo más cercano; `IM` es el índice de marginación CONAPO 2020, invertido y normalizado de 0 a 1 sobre los 125 municipios del Edomex. Niveles: bajo (< 0.3), moderado (0.3–0.5), alto (0.5–0.8) y exclusión severa (≥ 0.8).

## Stack (v1)

- **Cálculo:** Python, pandas, NetworkX (grafo del GTFS + Dijkstra). Un script genera `indice.json`.
- **Frontend:** React + Vite, react-router, react-leaflet. Sin servidor: la web lee el JSON estático.
- **Datos:** GTFS de SEMOVI CDMX (Metro y Metrobús, versión oct-2022), estaciones de Mexibús desde OpenStreetMap (Overpass), índice de marginación 2020 de CONAPO.

API, base de datos y simulaciones quedan para v2. Ver [`docs/stack-tecnologico-cronomx.md`](./docs/stack-tecnologico-cronomx.md).

## Cómo correrlo

```bash
# 1. Regenerar el índice (desde la raíz del repo)
pip install pandas networkx numpy
python backend/sigma_indice.py        # escribe frontend/public/data/indice.json

# 2. Levantar la web
cd frontend
cp .env.example .env                  # agrega tu VITE_CARTO_API_KEY
npm install
npm run dev
```

Necesitas el GTFS limpio en `backend/gtfs_limpio/` (ver `backend/limpiar_gtfs.py`) y el CSV de CONAPO en `backend/datos/conapo_im_2020.csv`.

## Equipo

| Integrante | Aporte |
|---|---|
| **David Velazquez** | Frontend, cálculo del índice, datos, documentación y difusión |
| **Max Ramírez** | Diseño de la fórmula del IPT y validación matemática |


## Documentación

- [Definición del proyecto](./docs/proyecto-pobreza-de-tiempo.md)
- [Stack tecnológico](./docs/stack-tecnologico-cronomx.md)
- [Cronograma](./docs/cronograma-cronomx.md)
- [Notas y bitácora de decisiones](./docs/notas.md)

## Licencia

Código abierto bajo licencia MIT — ver [`LICENSE`](./LICENSE).

---

*Proyecto desarrollado por estudiantes de la Escuela Superior de Cómputo (ESCOM) del Instituto Politécnico Nacional.*