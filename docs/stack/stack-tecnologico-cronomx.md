# Stack Tecnológico — CronoMX / SIGMA

**Sistema de Índices Georreferenciados de Movilidad y Accesibilidad**

Este documento define las tecnologías a utilizar, organizadas por rol/capa del proyecto. Prioriza herramientas gratuitas u open source, dado que el proyecto no maneja presupuesto propio.

---

## 1. Backend e Infraestructura de Datos (Miguel)

| Herramienta | Uso |
|---|---|
| **Python** | Lenguaje principal de procesamiento de datos |
| **pandas** | Limpieza y transformación de datasets (GTFS, afluencia) |
| **gtfs-kit / partridge** | Parseo de archivos GTFS sin reinventar el parser |
| **PostgreSQL + PostGIS** | Base de datos con soporte geoespacial nativo (distancias, intersecciones de rutas) |
| **FastAPI** | Exposición de datos procesados como API hacia el frontend; genera documentación automática |

## 2. Modelado Matemático del Índice y Rutas (Max)

| Herramienta | Uso |
|---|---|
| **Python + Jupyter Notebooks** | Prototipado iterativo de la fórmula del índice de "pobreza de tiempo" |
| **NetworkX** | Modelado de la red de transporte como grafo; algoritmos de ruta (Dijkstra/A*) |
| **NumPy / SciPy** | Cálculos estadísticos y validación del índice (ej. correlación con índice de marginación CONAPO) |

## 3. Frontend, Visualización y Dirección de IA (David)

| Herramienta | Uso |
|---|---|
| **React** | Framework de interfaz |
| **Leaflet** (o Mapbox GL JS si se acepta el límite de uso gratuito) | Mapa interactivo de la ZMVM |
| **Deck.gl** (opcional, futuro) | Visualización de grandes volúmenes de datos sobre el mapa, si se necesita más adelante |
| **scikit-learn (KMeans)** | Componente de IA: clustering de municipios con patrones de movilidad similares |

> **Nota sobre mapas:** Mapbox se ve más pulido pero tiene cuota gratuita limitada; Leaflet es gratuito sin techo de uso.

## 4. Compartido / Infraestructura

| Herramienta | Uso |
|---|---|
| **GitHub** | Repositorio del código, control de versiones, colaboración |
| **GitHub Actions** | Automatización de pruebas o actualización periódica de datos |
| **Vercel** o **Cloudflare Pages** | Hosting gratuito del frontend, con despliegue automático desde el repo |
| **Railway / Render** | Hosting gratuito (con límites) del backend y base de datos en fase inicial |

## 5. Dominio

| Opción | Qué es | Costo | Cuándo usarla |
|---|---|---|---|
| **is-a.dev** | Subdominio gratuito y permanente (ej. `cronomx.is-a.dev`), vía Pull Request a su repo comunitario en GitHub | Gratis, sin verificación | Fase inicial del proyecto |
| **GitHub Student Developer Pack** | Dominio **.me** (y opción de **.dev**) gratis por 1 año vía Namecheap, requiere verificación como estudiante (correo institucional del IPN) | Gratis 1 año | Alternativa si prefieren un dominio con TLD propio desde el inicio |
| **Dominio .mx o .com propio** | Registro estándar en cualquier registrador (ej. Cloudflare Registrar, a precio de costo sin margen) | Costo bajo (unos cuantos dólares/año) | Cuando el proyecto ya tenga tracción real (difusión, interés de investigadores) |

---

*Este documento complementa la definición general del proyecto (ver `proyecto-pobreza-de-tiempo.md`). El stack puede ajustarse conforme el equipo pruebe las herramientas en la práctica.*
*Documento redactado con ayuda de Inteligencia Artificial*
