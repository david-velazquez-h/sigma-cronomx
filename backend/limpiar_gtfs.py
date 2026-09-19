"""
Script para explorar y filtrar el GTFS estático de la CDMX,
quedándonos solo con Metro y Metrobús para el piloto de CronoMX.

"""

import pandas as pd
import os

CARPETA_GTFS = "GTFS SEMOVI CDMX" 
CARPETA_SALIDA = "gtfs_limpio"

# ---------- PARTE 1: Exploración ----------

agency = pd.read_csv(os.path.join(CARPETA_GTFS, "agency.txt"))
routes = pd.read_csv(os.path.join(CARPETA_GTFS, "routes.txt"))

print("=== Agencias disponibles en tu GTFS ===")
print(agency[["agency_id", "agency_name"]].to_string(index=False))

print("\n=== Cuántas rutas tiene cada agencia ===")
print(routes["agency_id"].value_counts())

print("\nRevisa los nombres exactos arriba y ajusta AGENCIAS_A_CONSERVAR abajo")
print("antes de correr la Parte 2 (coméntala con # si aún no la vas a correr).")

# ---------- PARTE 2: Filtrado real ----------
AGENCIAS_A_CONSERVAR = ["METRO", "MB"]  # ej: [1, 3] 

if AGENCIAS_A_CONSERVAR:
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    stops = pd.read_csv(os.path.join(CARPETA_GTFS, "stops.txt"))
    trips = pd.read_csv(os.path.join(CARPETA_GTFS, "trips.txt"))
    stop_times = pd.read_csv(os.path.join(CARPETA_GTFS, "stop_times.txt"))

    routes_filtradas = routes[routes["agency_id"].isin(AGENCIAS_A_CONSERVAR)]
    trips_filtrados = trips[trips["route_id"].isin(routes_filtradas["route_id"])]
    stop_times_filtrados = stop_times[stop_times["trip_id"].isin(trips_filtrados["trip_id"])]
    stops_filtrados = stops[stops["stop_id"].isin(stop_times_filtrados["stop_id"])]

    routes_filtradas.to_csv(os.path.join(CARPETA_SALIDA, "routes.csv"), index=False)
    trips_filtrados.to_csv(os.path.join(CARPETA_SALIDA, "trips.csv"), index=False)
    stop_times_filtrados.to_csv(os.path.join(CARPETA_SALIDA, "stop_times.csv"), index=False)
    stops_filtrados.to_csv(os.path.join(CARPETA_SALIDA, "stops.csv"), index=False)

    print(f"\nListo. {len(routes_filtradas)} rutas, {len(stops_filtrados)} paradas guardadas en '{CARPETA_SALIDA}/'")
else:
    print("\n(Parte 2 no corrió todavía — falta rellenar AGENCIAS_A_CONSERVAR)")