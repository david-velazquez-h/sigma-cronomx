"""
Asigna cada parada (Metro/Metrobús + Mexibús) al municipio piloto más cercano,
usando distancia en línea recta desde el centro del municipio.

Esto es una aproximación simple (radio desde un centro), no polígonos oficiales
del municipio, suficiente para la v1. La versión precisa usaría los polígonos
reales del Marco Geoestadístico del INEGI, queda como mejora de v2.

Uso:
    python asignar_municipios.py
"""

import csv
import math

# Municipios piloto: nombre, lat centro, lng centro, radio en km a considerar
MUNICIPIOS = [
    {"nombre": "Ecatepec de Morelos", "lat": 19.6015, "lng": -99.0503, "radio_km": 8},
    {"nombre": "Nezahualcóyotl", "lat": 19.4003, "lng": -99.0148, "radio_km": 6},
    {"nombre": "Chimalhuacán", "lat": 19.4150, "lng": -98.9950, "radio_km": 7},
    {"nombre": "Tecámac", "lat": 19.7128, "lng": -98.9767, "radio_km": 8},
]


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def municipio_mas_cercano(lat, lon):
    mejor = None
    mejor_dist = None
    for m in MUNICIPIOS:
        d = haversine_km(lat, lon, m["lat"], m["lng"])
        if d <= m["radio_km"] and (mejor_dist is None or d < mejor_dist):
            mejor = m["nombre"]
            mejor_dist = d
    return mejor, mejor_dist


def cargar_paradas():
    paradas = []

    # Metro / Metrobús (GTFS oficial ya filtrado)
    try:
        with open("gtfs_limpio/stops.csv", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                paradas.append({
                    "nombre": row.get("stop_name", ""),
                    "lat": float(row["stop_lat"]),
                    "lon": float(row["stop_lon"]),
                    "sistema": "Metro/Metrobús",
                })
    except FileNotFoundError:
        print("Aviso: no se encontró gtfs_limpio/stops.csv, se omite Metro/Metrobús")

    # Mexibús (vía Overpass/OSM)
    try:
        with open("mexibus_estaciones_osm.csv", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("lat") and row.get("lon"):
                    paradas.append({
                        "nombre": row.get("nombre", ""),
                        "lat": float(row["lat"]),
                        "lon": float(row["lon"]),
                        "sistema": "Mexibús",
                    })
    except FileNotFoundError:
        print("Aviso: no se encontró mexibus_estaciones_osm.csv, se omite Mexibús")

    return paradas


paradas = cargar_paradas()
print(f"Total de paradas cargadas: {len(paradas)}")

resultado = []
conteo_por_municipio = {m["nombre"]: 0 for m in MUNICIPIOS}
sin_municipio = 0

for p in paradas:
    municipio, distancia = municipio_mas_cercano(p["lat"], p["lon"])
    if municipio:
        conteo_por_municipio[municipio] += 1
    else:
        sin_municipio += 1
    resultado.append({
        "nombre": p["nombre"],
        "lat": p["lat"],
        "lon": p["lon"],
        "sistema": p["sistema"],
        "municipio_asignado": municipio or "",
    })

with open("paradas_por_municipio.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["nombre", "lat", "lon", "sistema", "municipio_asignado"])
    writer.writeheader()
    writer.writerows(resultado)

print("\n=== Paradas asignadas por municipio piloto ===")
for nombre, count in conteo_por_municipio.items():
    print(f"  {nombre}: {count} paradas")
print(f"  (fuera de todos los radios): {sin_municipio} paradas")
print("\nGuardado en 'paradas_por_municipio.csv' — esto es lo que Max necesita")
print("para calcular el índice por municipio.")