# CronoMX
### SIGMA — Sistema de Índices Georreferenciados de Movilidad y Accesibilidad

**Cuantificando el costo real del transporte en la ZMVM**
**Un proyecto de IA/datos abiertos — ESCOM IPN**

> **CronoMX** es la marca pública del proyecto (web, redes, difusión).
> **SIGMA** es el nombre técnico del sistema/algoritmo detrás (repo, metodología, publicaciones).

---

## 1. El problema

Cruzar la Zona Metropolitana del Valle de México en transporte público toma en promedio entre **5h21min y 5h49min**, dependiendo de la dirección del trayecto, contra apenas 2.7–2.8 horas en auto particular (dato de ONU-Habitat). Ese costo recae de forma desproporcionada en los municipios conurbados del Estado de México (Ecatepec, Neza, Chalco, Cuautitlán, etc.), cuyos habitantes cruzan diariamente para trabajar o estudiar en la CDMX.

Este fenómeno tiene nombre en estudios urbanos: **pobreza de tiempo**. No es solo "el transporte es lento" — es tiempo de vida, descanso y convivencia que se pierde de forma sistemática, y que hoy **no está cuantificado, visualizado ni es accesible de forma actualizable**. La investigación académica existente sobre movilidad y desigualdad en la ZMVM depende de encuestas que se levantan cada varios años (la Encuesta Origen-Destino del INEGI es de 2017), no de herramientas vivas.

## 2. Qué resolvemos (y qué no)

**No vamos a:**
- Arreglar el transporte público ni influir en decisiones de concesionarios o gobierno.
- Construir un "Google Maps" competitivo para transporte.

**Sí vamos a:**
- Hacer visible y medible un costo social que hoy es difuso y anecdótico.
- Dar a los investigadores una fuente de datos y metodología reproducible que no existe actualmente.
- Dar a la gente una herramienta simple para comparar el costo real de tiempo entre rutas/municipios.

## 3. A quién le sirve

| Público | Qué obtiene |
|---|---|
| Habitantes de municipios conurbados | Comparar tiempo real estimado por ruta/combinación de transporte |
| Investigadores en movilidad urbana/geografía social (UAM, UNAM, COLMEX) | Metodología y dataset reproducible, actualizable, complementario a estudios basados en encuestas |
| Comunidad de datos abiertos/cívicos en México (Codeando México, Social TIC) | Un caso de uso ciudadano bien documentado y open source |
| Comunidad ESCOM/IPN | Un proyecto con narrativa fuerte para difusión (Gaceta Politécnica, ferias, concursos) |

## 4. El producto: 3 piezas

1. **Mapa interactivo de la ZMVM**: cada municipio/corredor coloreado según su índice de "pobreza de tiempo" (tiempo estimado de traslado en transporte público hacia zonas de empleo). Es la pieza más compartible y la que genera impacto visual inmediato.
2. **Comparador de rutas**: el usuario ingresa origen y destino; se muestra tiempo estimado en transporte público (con transbordos) vs. auto particular, usando datos de GTFS.
3. **Repositorio abierto y documentado**: código, metodología y fuentes de datos en GitHub, con licencia abierta, para que investigadores puedan auditar o extender el trabajo.

**Plus opcional (sube el nivel académico):** cruzar el índice de tiempo con el **índice de marginación por municipio del CONAPO** (dato público), para mostrar correlación entre pobreza económica y pobreza de tiempo.

## 5. Datos que usaremos

- **GTFS estático de la CDMX** (portal de datos abiertos): rutas, paradas y horarios de Metro, Metrobús, RTP, Trolebús, Tren Ligero, Cablebús, Pumabús.
- **GTFS estático de Mexibús** (Estado de México): rutas y horarios programados. No hay afluencia histórica pública para Mexibús, así que el proyecto se apoya en tiempos programados + una muestra propia (encuestas breves o reportes de usuarios) para validar contra la realidad.
- **Afluencia histórica del Metro y Metrobús** (datos abiertos CDMX, actualizados mensualmente desde 2010/2005), útil para el índice de saturación dentro de CDMX.
- **Índice de marginación CONAPO por municipio** (si se hace el cruce opcional).
- Posible apoyo del proyecto open source **Apimetro** (GitHub), que ya unifica varios de estos sistemas en GeoJSON — evita reprocesar todo desde cero.

## 6. Alcance de la primera versión (v1)

Para no perderse en ambición: la v1 debería limitarse a **un número reducido de municipios piloto** (ej. Ecatepec, Nezahualcóyotl, Chalco) comparados contra 2–3 destinos típicos de empleo en CDMX (Centro, Reforma/Polanco, Santa Fe), en vez de cubrir toda la ZMVM desde el día uno. Cubrir todo es la v2.

## 7. Equipo y roles

Se definen en el stack tecnológico

## 8. Próximos pasos como equipo

1. Repartir roles según fortalezas de cada quien (ej. procesamiento de datos/backend, frontend/mapa, investigación y redacción de metodología).
2. Definir el stack técnico concreto (a discutir juntos: Python para procesamiento, alguna librería de mapas para el frontend).
3. Bajar y explorar los datasets de GTFS + afluencia para validar qué tan limpios/usables están en la práctica.
4. Definir el índice de "pobreza de tiempo" con una fórmula simple y defendible.
5. Armar un prototipo mínimo del mapa con los municipios piloto antes de escalar.

---

*Este documento resume la definición del proyecto para su presentación al equipo. Es un punto de partida, no una decisión cerrada, el alcance técnico y el stack se afinan en equipo.*
