# CronoMX
### SIGMA — Sistema de Índices Georreferenciados de Movilidad y Accesibilidad

**Cuantificando el costo real del transporte público en la Zona Metropolitana del Valle de México.**

---

##  El problema

Cruzar la Zona Metropolitana del Valle de México en transporte público toma en promedio entre **5h21min y 5h49min**, frente a apenas 2.7–2.8 horas en auto particular (ONU-Habitat). Este costo recae de forma desproporcionada en los municipios conurbados del Estado de México, cuyos habitantes cruzan diariamente para trabajar o estudiar en la CDMX.

A este fenómeno se le conoce en estudios urbanos como **pobreza de tiempo**: el tiempo de vida, descanso y convivencia que se pierde de forma sistemática por un transporte ineficiente y que hoy no está cuantificado, visualizado ni es accesible de forma actualizable.

##  Qué hace CronoMX

- **Mapa interactivo** de la ZMVM que muestra el índice de "pobreza de tiempo" por municipio/corredor.
- **Comparador de rutas**: tiempo estimado en transporte público (con transbordos) vs auto particular entre dos puntos.
- **Metodología abierta y reproducible**, documentada para que investigadores en movilidad urbana y estudios sociales puedan auditar, usar o extender el trabajo.

No buscamos "arreglar" el transporte público, buscamos hacer visible y medible un costo social que hoy es difuso y anecdótico.

##  Estado del proyecto

 En desarrollo activo, proyecto estudiantil de la Escuela Superior de Cómputo (ESCOM), Instituto Politécnico Nacional.

##  Stack tecnológico

- **Backend:** Python, FastAPI, PostgreSQL + PostGIS
- **Modelado:** Python, NetworkX, NumPy/SciPy
- **Frontend:** React, Leaflet
- **Datos:** GTFS (CDMX y Mexibús), afluencia histórica Metro/Metrobús (datos abiertos)

Ver detalle completo en [`docs/stack-tecnologico-cronomx.md`](./docs/stack-tecnologico-cronomx.md).

##  Equipo

| Integrante | Rol técnico | Rol de difusión |
|---|---|---|
| **Angel David Velazquez Herrera** | Líder del proyecto | Frontend, visualización y dirección de IA |
| **Miguel Angel Romero Rentería** | Backend e infraestructura de datos | Relaciones institucionales y académicas |
| **José Maximiliano Ramírez Monroy** | Modelado matemático del índice | Contenido, redes y storytelling | 

*TODOS DOCUMENTAN EL PROCESO*

##  Documentación

- [Definición del proyecto](./docs/proyecto-pobreza-de-tiempo.md)
- [Stack tecnológico](./docs/stack/stack-tecnologico-cronomx.md)
- [Cronograma del semestre](./docs/cronograma/cronograma-cronomx.md)
- [Notas y bitácora de decisiones](./docs/notas/notas.md)

## Licencia

Este proyecto es de código abierto bajo licencia MIT. ver [`LICENSE`](./LICENSE) para más detalles.

---

*Proyecto desarrollado por estudiantes de la Escuela Superior de Cómputo (ESCOM) del Instituto Politécnico Nacional.*
