"""
Aviso importante (documentado en la propia API):
Los datos de Mexibús en Apimetro vienen de una fuente NO oficial (OSMAN MAPS)
y pueden no reflejar la operación actual con exactitud. Úsalos, pero
anótalo en la metodología cuando la escriban — no tienen el mismo nivel
de confianza que el GTFS oficial de Metro/Metrobús.

Uso:
    pip install requests
    python descargar_mexibus.py
"""

import requests
import json
import os

CARPETA_SALIDA = "gtfs_mexibus"
BASE_URL = "https://apimetro.dev/movilidad/mapas"

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# 1. Estaciones (puntos) de Mexibús
resp_estaciones = requests.get(f"{BASE_URL}/geojsonEstacion", params={"sistema": "MEXIBUS"})
resp_estaciones.raise_for_status()
estaciones = resp_estaciones.json()

with open(os.path.join(CARPETA_SALIDA, "estaciones.geojson"), "w", encoding="utf-8") as f:
    json.dump(estaciones, f, ensure_ascii=False, indent=2)

print(f"Estaciones de Mexibús guardadas: {len(estaciones.get('features', []))} paradas")

# 2. Líneas (trazos) de Mexibús
resp_lineas = requests.get(f"{BASE_URL}/geojsonLinea", params={"sistema": "MEXIBUS"})
resp_lineas.raise_for_status()
lineas = resp_lineas.json()

with open(os.path.join(CARPETA_SALIDA, "lineas.geojson"), "w", encoding="utf-8") as f:
    json.dump(lineas, f, ensure_ascii=False, indent=2)

print(f"Líneas de Mexibús guardadas: {len(lineas.get('features', []))} tramos")

print(f"\nListo. Archivos en '{CARPETA_SALIDA}/'. Recuerda documentar en la metodología")
print("que estos datos vienen de fuente no oficial (aviso de Apimetro).")