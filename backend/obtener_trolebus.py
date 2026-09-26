"""
Este doc descarga las estaciones de Trolebús (sistema TROLE) desde Apimetro


Uso:
    python obtener_trolebus.py
"""

import requests
import json
import csv
import unicodedata

resp = requests.get(
    "https://apimetro.dev/movilidad/mapas/geojsonEstacion",
    params={"sistema": "TROLE"},
)
resp.raise_for_status()
data = resp.json()

features = data.get("features", [])
print(f"Total de estaciones de Trolebús en Apimetro: {len(features)}")

filas = []
for f in features:
    props = f.get("properties", {})
    coords = f.get("geometry", {}).get("coordinates", [None, None])
    filas.append({
        "nombre": props.get("nombre", ""),
        "lat": coords[1],
        "lon": coords[0],
        "alcaldia_municipio": props.get("alcaldia_municipio", ""),
        "num_comercial": props.get("num_comercial", ""),
    })

with open("trolebus_estaciones.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["nombre", "lat", "lon", "alcaldia_municipio", "num_comercial"])
    writer.writeheader()
    writer.writerows(filas)

print("Guardado en 'trolebus_estaciones.csv'")

# Buscar específicamente Chalco / Santa Marta
def normalizar(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return s.lower()

encontradas_chalco = [
    f for f in filas
    if "chalco" in normalizar(f["nombre"]) or "chalco" in normalizar(f["alcaldia_municipio"])
    or "santa marta" in normalizar(f["nombre"])
]

print(f"\n=== Búsqueda de Chalco / Santa Marta ===")
if encontradas_chalco:
    print(f"¡Sí encontrado! {len(encontradas_chalco)} estaciones relacionadas:")
    for e in encontradas_chalco:
        print(f"  - {e['nombre']} ({e['lat']}, {e['lon']}) — {e['alcaldia_municipio']}")
else:
    print("No se encontró ninguna estación de Chalco o Santa Marta en los datos de TROLE.")
    print("El corredor Chalco-Santa Marta, al ser tan reciente, probablemente aún no está cargado.")