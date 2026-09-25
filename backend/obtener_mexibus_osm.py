"""
Obtiene las paradas de Mexibús directamente de OpenStreetMap vía Overpass API,
en vez de geocodificar nombre por nombre (eso dio muy mala puntería porque
Nominatim busca direcciones/lugares, no paradas de transporte específicas).

Overpass consulta datos ya etiquetados por la comunidad de OSM como
paradas de transporte público

Uso:
    pip install requests
    python obtener_mexibus_osm.py
"""

import requests
import json
import csv
import unicodedata

# Caja delimitadora aproximada de la zona donde opera Mexibús
# (norte y oriente del Edomex + un poco de CDMX): sur, oeste, norte, este
BBOX = "19.15,-99.35,19.75,-98.85"

QUERY = f"""
[out:json][timeout:60];
(
  node["network"~"Mexibús|Mexibus",i]({BBOX});
  node["operator"~"Mexibús|Mexibus|Transmasivo|Transcomunicador",i]({BBOX});
  node["route_ref"~"Mexibús|Mexibus",i]({BBOX});
);
out body;
"""

print("Consultando Overpass API (puede tardar 10-30 segundos)...")
resp = requests.post(
    "https://overpass-api.de/api/interpreter",
    data={"data": QUERY},
    headers={"User-Agent": "CronoMX-SIGMA-proyecto-escolar-ESCOM-IPN"},
)
resp.raise_for_status()
data = resp.json()

elementos = data.get("elements", [])
print(f"\nOverpass devolvió {len(elementos)} nodos etiquetados como Mexibús.")

filas = []
for el in elementos:
    nombre = el.get("tags", {}).get("name", "(sin nombre)")
    filas.append({
        "nombre": nombre,
        "lat": el.get("lat"),
        "lon": el.get("lon"),
        "network": el.get("tags", {}).get("network", ""),
        "operator": el.get("tags", {}).get("operator", ""),
    })

with open("mexibus_estaciones_osm.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["nombre", "lat", "lon", "network", "operator"])
    writer.writeheader()
    writer.writerows(filas)

print(f"Guardado en 'mexibus_estaciones_osm.csv'")

# --- Comparación contra la lista oficial que sacamos de SITRAMyTEM ---

def normalizar(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.lower().strip()

ESTACIONES_OFICIALES = [
    "Ciudad Azteca", "Quinto Sol", "Josefa Ortíz", "Industrial", "Unitec",
    "Torres", "Zodiaco", "Adolfo López Mateos", "Vocacional 3",
    "Valle De Ecatepec", "Las Américas", "Primero De Mayo",
    "Hospital Las Américas", "Aquiles Serdán", "Jardines De Morelos",
    "Ojo De Agua", "Nezahualcóyotl", "Chimalhuacán", "Pantitlán",
    "Indios Verdes", "La Quebrada", "Lechería",
    # (lista recortada aquí solo para la comparación rápida; el CSV completo
    # de OSM puede tener nombres distintos a los oficiales — se revisa a mano)
]

nombres_osm_normalizados = {normalizar(f["nombre"]) for f in filas}
encontradas = [e for e in ESTACIONES_OFICIALES if normalizar(e) in nombres_osm_normalizados]

print(f"\nDe {len(ESTACIONES_OFICIALES)} estaciones clave revisadas, "
      f"{len(encontradas)} aparecen con el mismo nombre en OSM.")
print("Revisa 'mexibus_estaciones_osm.csv' completo, puede haber más estaciones")
print("con nombres ligeramente distintos a los oficiales, hay que cruzarlas a mano.")